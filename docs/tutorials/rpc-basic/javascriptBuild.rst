Compiling and Installing the Library in Javascript
==================================================

The next step is compiling the service contract and installing the resulting library in Javascript:

``{{{compiler_command}}} package --javascript hello.q``

This command will generate a hello directory at the current location with a js subdirectory. The build artifacts are within the subdirectory. Information on other build options and the behavior of the default options including the location of all of the generated artifacts is available on the `Compilation page <http://datawire.github.io/{{{doc-directory}}}/install/index.html>`_ of the {{{product}}} Installation and Configuration Guide.

To install the resulting library in Javascript, do the following:

``npm install hello/js/hello.tgz``
