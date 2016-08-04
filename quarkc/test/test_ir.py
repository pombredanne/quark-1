# Copyright 2015 datawire. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from quarkc.ir import *

def test_name():
    n = Name("foo")
    print n
    n = Name("pkg:foo")
    print n
    n = Name("pkg:foo.bar")
    print n
    n = Name("pkg", "foo.bar")
    print n

def test_local():
    l = Local(Name("pkg:foo"), "bar")
    print l
    l = Local("pkg:foo.bar", "bar")
    print l

def test_package():
    p1 = Package((Function(Name("p1:fun"),
                           Name("p1:int"),
                           (Param("p1:int", "a"),
                            Param("p1:int", "b")),
                           Return(Invoke(Name("q:add"), (Var("a"), Var("b"))))),
                  Function(Name("p1:f2"),
                           Name("q:int"),
                           (Param("q:int", "a"),
                            Param("q:int", "b")),
                           Return(Invoke(Name("q:mul"), (Var("a"), Var("b")))))))
    print p1
    p = Python()
    emit(p1, p)
    print p.files

def test_nesting():
    l = Local(Name("q:int"), "foo")
    l2 = Local(Name("q:int"), "foo")
    stmt = While(Var("x"), (l, If(Var("y"), (l2,), (l2,))))
    b = Block((stmt,))
    print b
    names = set()
    for c in b.collisions(names):
        print "collision:", c


from quarkc.emit import *

def test_emit():
    stmt = If(Var("x"),
              Call(Var("y"), ()),
              Call(Var("z"), ()))
    print code(stmt, Python())
    print code(stmt, Java())

    print

    stmt = If(Var("x"),
              (Call(Var("y"), ()),),
              (stmt,))
    print "======"
    print code(stmt, Python())
    print code(stmt, Java())
    print "======"

    stmt = While(Invoke(Name("pkg:asdf"), (Send(Var("x"), "y", ()),)), (stmt,))
    print code(stmt, Java())
    print header(stmt, Python())
    print code(stmt, Python())
    print footer(stmt, Python())
