import pytest
import py
import os
import subprocess
import time
import threading
import textwrap
import contextlib

def command(*cmd, **kwargs):
    cwd = kwargs.pop('cwd', py.path.local())
    assert not kwargs
    print "command in ", cwd or ".", cmd
    with cwd.as_cwd():
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.wait():
        print "out", stdout
        print "err", stderr
        pytest.fail("Command failed %s" % " ".join(cmd))

class QuarkCompile(object):
    def __init__(self, tmpdir, path):
        self.outdir = "generated-sources"
        self.tmpdir = tmpdir
        self.path = path
        with open(path) as f:
            self.version = f.read()\
              .split("@version(",1)[1]\
              .split(")",1)[0]\
              .strip("'")\
              .strip('"')
        self.compiled = False

    def compile(self):
        if self.compiled:
            return
        print "Need to compile", self.path, " in ", self.tmpdir
        command("quark", "package", "--skip-doc",
                "--output", self.outdir,
                self.path,
                cwd = self.tmpdir
                )
        self.compiled = True

    @property
    def py_package(self):
        self.compile()
        return self.tmpdir / self.outdir / "py" / "dist" / (
            "interop-%s-py2-none-any.whl" % self.version)

    @property
    def js_package(self):
        self.compile()
        return self.tmpdir / self.outdir / "js" / "interop.tgz"

    @property
    def java_package(self):
        self.compile()
        return self.tmpdir / self.outdir / "java" / "target" / (
            "interop-%s.jar" % self.version)

    def __repr__(self):
        return "%scompiled %s in %s" % (
            (self.compiled and "Already " or "Un-"),
            self.path, self.tmpdir)

class IntegrationMeta(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            cls.registry = []
        else:
            cls.registry.append(cls)
            cls.name = name
        super(IntegrationMeta, cls).__init__(name, bases, dct)

class BackgroundProcess(object):
    def __init__(self, cwd, cmd):
        self.cwd = cwd
        self.cmd = cmd
        self.stdout = None
        self.stderr = None
        self.p = None
        self.w = None

    def start(self):
        print "background process", self.cwd, self.cmd
        with self.cwd.as_cwd():
            self.p = subprocess.Popen(self.cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        def comm():
            o, e = self.p.communicate()
            print self.cmd, "produced", o, "and", e
            self.stdout, self.stderr = o, e

        self.w = threading.Thread(target=comm)
        self.w.start()

    def stop(self, timeout=0.1):
        while timeout > 0 and self.p.poll() is None:
            time.sleep(0.1)
            timeout -= 0.1
        if self.p.poll() is None:
            self.p.terminate()
            time.sleep(0.1)
        if self.p.poll() is None:
            self.p.kill()
            time.sleep(0.1)
        ret = self.p.wait()
        self.w.join()
        print "out", self.stdout
        print "err", self.stderr
        return ret

    @contextlib.contextmanager
    def wait(self, timeout=0.1):
        self.start()
        yield
        self.stop(timeout)


class Integration(object):
    __metaclass__ = IntegrationMeta
    def __init__(self, compile):
        self.tmpdir = compile.tmpdir
        self.compile = compile
        self.built = False

    def __str__(self):
        return self.name + "@" + str(id(self))

    def check_build(self):
        if self.built:
            return
        print "need to build integration", self
        self.rundir.ensure(dir=1)
        self.build()
        self.built = True

    def __repr__(self):
        return "%s %s integration of %s" % ((self.built and "Built" or "Unbuilt"),
                                            self.name, self.compile)

    @property
    def rundir(self):
        return self.tmpdir / "run" / self.name

    def client(self, port):
        self.check_build()
        return BackgroundProcess(cwd=self.rundir,
                                 cmd=self.invoke_client(port))

    def server(self, port):
        self.check_build()
        return BackgroundProcess(cwd=self.rundir,
                                 cmd=self.invoke_server(port))

    @property
    def runtimes(self):
        return py.path.local(__file__).dirpath("..")

    def build(self):
        pytest.fail("Need to implement build")

    def invoke_server(self, port):
        pytest.fail("Need to implement invoke_server")

    def invoke_client(self, port):
        pytest.fail("Need to implement invoke_client")

class Node(Integration):
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)

    def build(self):
        self.npm_install(self.js_core_package)
        self.npm_install(self.compile.js_package)
        self.npm_install(self.js_node_package)
        self.rundir.join("run-client.js").write(textwrap.dedent("""\
            "use strict";
            var runtime = require("datawire-quark-node");
            var runtime_core = require("datawire-quark-core");
            var interop = require("interop");
            var process = require("process");
            console.log("Node client harness is started")
            new interop.Entrypoint().client(runtime, process.argv[2]);
        """))
        self.rundir.join("run-server.js").write(textwrap.dedent("""\
            "use strict";
            var runtime = require("datawire-quark-node");
            var runtime_core = require("datawire-quark-core");
            var interop = require("interop");
            var process = require("process");
            console.log("Node server harness is started")
            new interop.Entrypoint().server(runtime, process.argv[2]);
        """))

    def npm_install(self, package):
        command("npm", "install", package.strpath, cwd=self.rundir)

    @property
    def js_core_package(self):
        return self.runtimes / "js-core"

    @property
    def js_node_package(self):
        return self.runtimes / "js-node"

    def invoke_server(self, port):
        return ["node", "run-server.js", str(port)]

    def invoke_client(self, port):
        return ["node", "run-client.js", str(port)]

class Twisted(Integration):
    def __init__(self, **kwargs):
        super(Twisted, self).__init__(**kwargs)

    def build(self):
        command("virtualenv", "x", cwd=self.rundir)
        self.pip_install(self.py_core_package)
        self.pip_install(self.compile.py_package)
        self.pip_install(self.py_twisted_package)
        self.rundir.join("run-client.py").write(textwrap.dedent("""\
            import interop
            import quark_twisted_runtime
            import quark_runtime
            import sys
            print "Twisted client harness is started"
            runtime = quark_twisted_runtime.get_twisted_runtime()
            interop.Entrypoint().client(runtime, int(sys.argv[1]))
            runtime.launch()
        """))
        self.rundir.join("run-server.py").write(textwrap.dedent("""\
            import interop
            import quark_twisted_runtime
            import quark_runtime
            import sys
            print "Twisted server harness is started"
            runtime = quark_twisted_runtime.get_twisted_runtime()
            interop.Entrypoint().server(runtime, int(sys.argv[1]))
            runtime.launch()
        """))

    @property
    def pip(self):
        return self.rundir / "x" / "bin" / "pip"

    @property
    def python(self):
        return self.rundir / "x" / "bin" / "python"

    def pip_install(self, package):
        assert package.check()
        command(self.pip.strpath, "install", package.strpath, cwd=self.rundir)

    @property
    def py_core_package(self):
        return self.runtimes / "python-core"

    @property
    def py_twisted_package(self):
        return self.runtimes / "twisted"

    def invoke_server(self, port):
        return [self.python.strpath, "run-server.py", str(port)]

    def invoke_client(self, port):
        return [self.python.strpath, "run-client.py", str(port)]

class Netty(Integration):
    def __init__(self, **kwargs):
        super(Netty, self).__init__(**kwargs)

    def build(self):
        self.m2_repo.ensure(dir=1)
        self.rundir.join("pom.xml").write(textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
              <modelVersion>4.0.0</modelVersion>
              <groupId>io.datawire.quark.interop-test</groupId>
              <artifactId>interop-harness</artifactId>
              <version>0.0.1-SNAPSHOT</version>
              <name>interop harness</name>
              <build>
                <plugins>
                  <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.3</version>
                    <configuration>
                      <source>1.7</source>
                      <target>1.7</target>
                    </configuration>
                  </plugin>
                </plugins>
              </build>
              <repositories>
               <repository>
                <id>test repo</id>
                <url>file://%(m2_repo)s</url>
               </repository>
              </repositories>
              <dependencies>
                <dependency>
                  <groupId>io.datawire.quark</groupId>
                  <artifactId>quark-netty</artifactId>
                  <version>%(quark_netty_version)s</version>
                  <scope>compile</scope>
                </dependency>
                <dependency>
                  <groupId>io.datawire.quark.interop-test</groupId>
                  <artifactId>interop-quark</artifactId>
                  <version>%(compile_version)s</version>
                </dependency>
              </dependencies>
            </project>
        """ % dict(quark_netty_version = self.quark_netty_version,
                   m2_repo = self.m2_repo.strpath,
                   compile_version = self.compile.version,
                   ))
        )
        harness = self.rundir / "src" / "main" / "java" / "interop"/ "harness"
        harness.ensure(dir=1)
        harness.join("Client.java").write(textwrap.dedent("""\
            package interop.harness;
            import io.datawire.quark.netty.QuarkNettyRuntime;
            public class Client {
                public static void main(String[] args) {
                    System.out.println("Netty client harness is started");
                    QuarkNettyRuntime runtime = new QuarkNettyRuntime();
                    new interop.Entrypoint().client(runtime, Integer.parseInt(args[0]));
                }
            }
        """)
        )
        harness.join("Server.java").write(textwrap.dedent("""\
            package interop.harness;
            import io.datawire.quark.netty.QuarkNettyRuntime;
            public class Server {
                public static void main(String[] args) {
                    System.out.println("Netty server harness is started");
                    QuarkNettyRuntime runtime = new QuarkNettyRuntime();
                    new interop.Entrypoint().server(runtime, Integer.parseInt(args[0]));
                }
            }
        """)
        )
        command("mvn", "install::install-file",
                "-Dfile=%s" % self.compile.java_package.strpath,
                "-DgroupId=io.datawire.quark.interop-test",
                "-DartifactId=interop-quark",
                "-Dversion=%s" % self.compile.version,
                "-Dpackaging=jar",
                "-DlocalRepositoryPath=%s" % self.m2_repo.strpath,
                cwd=self.rundir)
        command("mvn", "compile", cwd=self.rundir)

    @property
    def quark_netty_version(self):
        pom = self.quark_netty_package.join("pom.xml").read()
        version = pom.split("<version>",1)[1].split("</version>",1)[0]
        return version

    @property
    def quark_netty_package(self):
        return self.runtimes / "netty"

    @property
    def m2_repo(self):
        return self.rundir / "m2repo"

    def invoke_client(self, port):
        return ["mvn", "exec:java",
                "-Dexec.mainClass=interop.harness.Client",
                "-Dexec.args=%s" % port,
                "-q"]

    def invoke_server(self, port):
        return ["mvn", "exec:java",
                "-Dexec.mainClass=interop.harness.Server",
                "-Dexec.args=%s" % port,
                "-q"]


directory = os.path.join(os.path.dirname(__file__), "interop")

files = [name for name in os.listdir(directory) if name.endswith(".q")]
paths = [os.path.join(directory, name) for name in files]

class CompileCache(object):
    def __init__(self):
        self.compiles = {}

    def get(self, path, tmpdir):
        if path not in self.compiles:
            self.compiles[path] = QuarkCompile(tmpdir, path)
        return self.compiles[path]

class IntegrationCache(object):
    def __init__(self):
        self.integrations = {}

    def get(self, cls, compile):
        key = (cls, compile)
        if key not in self.integrations:
            self.integrations[key] = cls(compile=compile)
        return self.integrations[key]

class PortGenerator(object):
    def __init__(self):
        self.port = 9876

    def next(self):
        self.port += 1
        return self.port

@pytest.fixture(scope='module')
def port_generator():
    return PortGenerator()

@pytest.fixture
def port(port_generator):
    return port_generator.next()

@pytest.fixture(params=paths)
def path(request):
    return request.param

@pytest.fixture(scope='module')
def compile_cache():
    return CompileCache()

@pytest.fixture
def compile(path, tmpdir, compile_cache):
    return compile_cache.get(path, tmpdir)

@pytest.fixture(scope='module')
def integration_cache():
    return IntegrationCache()

@pytest.fixture(params=Integration.registry)
def client_integration(request, compile, integration_cache):
    return integration_cache.get(request.param, compile)

@pytest.fixture(params=Integration.registry)
def server_integration(request, compile, integration_cache):
    return integration_cache.get(request.param, compile)

def test_interop(client_integration, server_integration, port):
    client = client_integration.client(port)
    server = server_integration.server(port)
    with server.wait(0):
        time.sleep(1)
        with client.wait(1):
            print "server and client started"
            time.sleep(1)
    print "server and client stopped"
    c = client.stdout
    assert "FAIL" not in c
    assert "onHTTPInit" in c
    assert "onHTTPFinal" in c
    assert "onHTTPError" not in c
    s = server.stdout
    assert "Hello Registered on" in s
    assert "Hello Trouble" not in s
    assert client.stderr == ""
    assert server.stderr == ""
