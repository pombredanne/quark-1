from .dispatch import (overload, dispatch)

# Problem areas from the current backend:
#  - scoping of names (if nested in while nested in function, sometimes introduces scopes, sometimes not)
#  - mapping of names into target language (dumb languages that use captialization to mean things)
#  - importing between namespaces and/or packages
#  - testing backend in isolation

# Potential ordering that this could proceed.
#
#  1. Flesh out this sketch to skeletaly solve the problem areas
#     described above, e.g. make it just capable of correctly
#     compiling an if nested in a while nested in a function that is
#     imported into another namespace and another package.
#
#  2. Hook up skeletal version into each target language (including
#     go) and make sure the methodology for testing this is
#     satisfactory.
#
#  3. Fill in the extra bits needed to make the skeletal version
#     turing complete.
#
#  4. Wire this into a frontend. This might be the existing frontend,
#     or it might be a scope reduced frontend if the other work
#     streams have eliminated dependencies on frontend features like
#     inheritence. Hypothetically it could even be an alternative
#     frontend.


# should pull in stuff from types base class here... would enable
# comparisons and stuff for testing, should possibly use pyrsistent or
# something like that for this stuff, although I want to see how
# pattern matching would work

class IR(object):

    def repr(self, *args, **kwargs):
        sargs = [repr(a) for a in args]
        sargs += ["%s=%r" % (k, v) for k, v in kwargs.items() if v is not None]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(sargs))

def namesplit(name):
    if ':' in name:
        package, path = name.split(':')
        path = tuple(path.split('.'))
        return package, path
    else:
        return name, ()

# A fully qualified name. This knows how to import itself both across
# packages and from other namespaces within the same package. Does
# this need to know what type it is importing, e.g. might
# functions/interfaces/classes be imported differently?

class Name(IR):

    def __init__(self, package, *path):
        package, pfx = namesplit(package)
        self.package = package
        self.path = pfx
        for n in path:
            self.path += tuple(n.split('.'))

    def __repr__(self):
        return self.repr(self.package, *self.path)

class Declaration(IR):

    @overload(Name, basestring)
    def __init__(self, type, name):
        self.type = type
        self.name = name

    @overload(basestring, basestring)
    def __init__(self, type, name):
        self.type = Name(type)
        self.name = name

    def __repr__(self):
        return self.repr(self.type, self.name)

class Param(Declaration):
    pass
    
class Local(Declaration):
    pass

class Field(Declaration):
    pass

# Contains definitions. Renders to a buildable distribution unit.
class Package(IR):

    def __init__(self, definitions):
        self.definitions = definitions

    def __repr__(self):
        if self.definitions:
            return "Package(\n  %s)" % "\n  ".join([repr(d) for d in self.definitions])
        else:
            return "Package()"

# A class, interface, or function.
class Definition(IR):
    pass

# knows how to render inside a dfn, this has to account for imports
# needed by rendered code
class Code(IR):

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return self.code

class Function(Definition):

    @overload(Name, Name, tuple, Code)
    def __init__(self, name, type, params, body):
        self.name = name
        self.type = type
        self.params = params
        self.body = body

    def __repr__(self):
        return self.repr(self.name, self.type, self.params, self.body)

# Note that there is no concept of inheritence here, just
# implementation of interfaces. This implies that the quark FFI cannot
# accomodate subclassing, i.e. quark types cannot be subclassed from
# outside of quark, the only types quark really exports are
# interfaces, and the only external types quark allows to pass across
# its surface are interfaces.
class Class(Definition):

    @overload(Name, tuple, tuple, tuple)
    def __init__(self, name, implements, methods, fields):
        self.name = name
        self.implements = implements
        self.methods = methods
        self.fields = fields

# basically the same as a class but no fields
class Interface(Definition):

    @overload(Name, tuple, tuple)
    def __init__(self, name, implements, methods):
        self.name = name
        self.implements = implements
        self.methods = methods

class Method(IR):

    @overload(basestring, Name, tuple)
    def __init__(self, name, type, params, body):
        self.name = name
        self.type = type
        self.params = params
        self.body = body

    def __repr__(self):
        return self.repr(self.name, self.type, self.params, self.body)

# code

class Expression(Code):
    pass

class This(Expression):
    pass

class Var(Expression):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.repr(self.name)

class Get(Expression):

    @overload(Expression, basestring)
    def __init__(self, expr, attr):
        self.expr = expr
        self.attr = attr

class Set(Expression):

    @overload(Expression, basestring, Expression)
    def __init__(self, expr, attr, value):
        self.expr = expr
        self.attr = attr
        self.value = value

# Invokes a function given the fully qualified name and arguments
class Invoke(Expression):

    @overload(Name, tuple)
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return self.repr(self.name, self.args)

# Invokes a method on an object
class Send(Expression):

    @overload(Expression, basestring, tuple)
    def __init__(self, obj, name, args):
        self.obj = obj
        self.name = name
        self.args = args

    def __repr__(self):
        return self.repr(self.obj, self.name, self.args)

# Constructs an instance of a class.
class Construct(Expression):

    @overload(Name, tuple)
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return self.repr(self.name, self.args)

# Invokes a callable expression.
class Call(Expression):

    @overload(Expression, tuple)
    def __init__(self, expr, args):
        self.expr = expr
        self.args = args

    def __repr__(self):
        return self.repr(self.expr, self.args)

class Cast(Expression):

    @overload(Name, Expression)
    def __init__(self, type, expr):
        self.type = type
        self.expr = expr

# literals

# ...

# statements

class Statement(Code):
    pass

class Return(Statement):

    @overload(Expression)
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return self.repr(self.expr)

class If(Statement):
    pass

class While(Statement):
    pass

class Break(Statement):
    pass

class Continue(Statement):
    pass
