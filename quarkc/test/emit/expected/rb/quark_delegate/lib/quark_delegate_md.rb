module Quark
def self.quark_delegate_md; MODULE_quark_delegate_md; end
module MODULE_quark_delegate_md
require 'quark' # .../reflect
# for ('quark_delegate_md',): require_relative 'quark_delegate' # 0 () ()

def self.quark_delegate_Message_encode_Method; CLASS_quark_delegate_Message_encode_Method; end
class CLASS_quark_delegate_Message_encode_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark.String", "encode", ::DatawireQuarkCore::List.new([]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        return obj.encode()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Message; CLASS_quark_delegate_Message; end
class CLASS_quark_delegate_Message < ::Quark.quark.reflect.QuarkClass
    extend ::DatawireQuarkCore::Static

    static singleton: -> { ::Quark.quark_delegate_md.quark_delegate_Message.new() }



    def initialize()
        
        super("quark_delegate.Message")
        (self).name = "quark_delegate.Message"
        (self).parameters = ::DatawireQuarkCore::List.new([])
        (self).fields = ::DatawireQuarkCore::List.new([])
        (self).methods = ::DatawireQuarkCore::List.new([::Quark.quark_delegate_md.quark_delegate_Message_encode_Method.new()])

        nil
    end




    def construct(args)
        
        return ::Quark.quark_delegate.Message.new()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end
CLASS_quark_delegate_Message.unlazy_statics

def self.quark_delegate_Ping_encode_Method; CLASS_quark_delegate_Ping_encode_Method; end
class CLASS_quark_delegate_Ping_encode_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark.String", "encode", ::DatawireQuarkCore::List.new([]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        return obj.encode()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Ping; CLASS_quark_delegate_Ping; end
class CLASS_quark_delegate_Ping < ::Quark.quark.reflect.QuarkClass
    extend ::DatawireQuarkCore::Static

    static singleton: -> { ::Quark.quark_delegate_md.quark_delegate_Ping.new() }



    def initialize()
        
        super("quark_delegate.Ping")
        (self).name = "quark_delegate.Ping"
        (self).parameters = ::DatawireQuarkCore::List.new([])
        (self).fields = ::DatawireQuarkCore::List.new([])
        (self).methods = ::DatawireQuarkCore::List.new([::Quark.quark_delegate_md.quark_delegate_Ping_encode_Method.new()])

        nil
    end




    def construct(args)
        
        return ::Quark.quark_delegate.Ping.new()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end
CLASS_quark_delegate_Ping.unlazy_statics

def self.quark_delegate_Pong_toString_Method; CLASS_quark_delegate_Pong_toString_Method; end
class CLASS_quark_delegate_Pong_toString_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark.String", "toString", ::DatawireQuarkCore::List.new([]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        return obj.toString()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Pong_encode_Method; CLASS_quark_delegate_Pong_encode_Method; end
class CLASS_quark_delegate_Pong_encode_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark.String", "encode", ::DatawireQuarkCore::List.new([]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        return obj.encode()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Pong; CLASS_quark_delegate_Pong; end
class CLASS_quark_delegate_Pong < ::Quark.quark.reflect.QuarkClass
    extend ::DatawireQuarkCore::Static

    static singleton: -> { ::Quark.quark_delegate_md.quark_delegate_Pong.new() }



    def initialize()
        
        super("quark_delegate.Pong")
        (self).name = "quark_delegate.Pong"
        (self).parameters = ::DatawireQuarkCore::List.new([])
        (self).fields = ::DatawireQuarkCore::List.new([])
        (self).methods = ::DatawireQuarkCore::List.new([::Quark.quark_delegate_md.quark_delegate_Pong_toString_Method.new(), ::Quark.quark_delegate_md.quark_delegate_Pong_encode_Method.new()])

        nil
    end




    def construct(args)
        
        return ::Quark.quark_delegate.Pong.new()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end
CLASS_quark_delegate_Pong.unlazy_statics

def self.quark_delegate_Test_bar_Method; CLASS_quark_delegate_Test_bar_Method; end
class CLASS_quark_delegate_Test_bar_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark.Object", "bar", ::DatawireQuarkCore::List.new(["quark.String", "quark.List<quark.Object>", "quark.List<quark.Object>"]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        return obj.bar((args)[0], (args)[1], (args)[2])

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Test_foo_Method; CLASS_quark_delegate_Test_foo_Method; end
class CLASS_quark_delegate_Test_foo_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark.void", "foo", ::DatawireQuarkCore::List.new(["quark.String", "quark.String", "quark.int"]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        obj.foo((args)[0], (args)[1], (args)[2])
        return nil

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Test_rpc_Method; CLASS_quark_delegate_Test_rpc_Method; end
class CLASS_quark_delegate_Test_rpc_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark_delegate.Message", "rpc", ::DatawireQuarkCore::List.new(["quark.String", "quark_delegate.Message", "quark.List<quark.Object>"]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        return obj.rpc((args)[0], (args)[1], (args)[2])

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Test_hello_Method; CLASS_quark_delegate_Test_hello_Method; end
class CLASS_quark_delegate_Test_hello_Method < ::Quark.quark.reflect.Method



    def initialize()
        
        super("quark_delegate.Pong", "hello", ::DatawireQuarkCore::List.new(["quark_delegate.Ping"]))

        nil
    end




    def invoke(object, args)
        
        obj = object
        return obj.hello((args)[0])

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end

def self.quark_delegate_Test; CLASS_quark_delegate_Test; end
class CLASS_quark_delegate_Test < ::Quark.quark.reflect.QuarkClass
    extend ::DatawireQuarkCore::Static

    static singleton: -> { ::Quark.quark_delegate_md.quark_delegate_Test.new() }



    def initialize()
        
        super("quark_delegate.Test")
        (self).name = "quark_delegate.Test"
        (self).parameters = ::DatawireQuarkCore::List.new([])
        (self).fields = ::DatawireQuarkCore::List.new([])
        (self).methods = ::DatawireQuarkCore::List.new([::Quark.quark_delegate_md.quark_delegate_Test_bar_Method.new(), ::Quark.quark_delegate_md.quark_delegate_Test_foo_Method.new(), ::Quark.quark_delegate_md.quark_delegate_Test_rpc_Method.new(), ::Quark.quark_delegate_md.quark_delegate_Test_hello_Method.new()])

        nil
    end




    def construct(args)
        
        return ::Quark.quark_delegate.Test.new()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end
CLASS_quark_delegate_Test.unlazy_statics

def self.quark_List_quark_Object_; CLASS_quark_List_quark_Object_; end
class CLASS_quark_List_quark_Object_ < ::Quark.quark.reflect.QuarkClass
    extend ::DatawireQuarkCore::Static

    static singleton: -> { ::Quark.quark_delegate_md.quark_List_quark_Object_.new() }



    def initialize()
        
        super("quark.List<quark.Object>")
        (self).name = "quark.List"
        (self).parameters = ::DatawireQuarkCore::List.new(["quark.Object"])
        (self).fields = ::DatawireQuarkCore::List.new([])
        (self).methods = ::DatawireQuarkCore::List.new([])

        nil
    end




    def construct(args)
        
        return ::DatawireQuarkCore::List.new()

        nil
    end

    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end
CLASS_quark_List_quark_Object_.unlazy_statics

def self.Root; CLASS_Root; end
class CLASS_Root < ::DatawireQuarkCore::QuarkObject
    extend ::DatawireQuarkCore::Static

    static quark_delegate_Message_md: -> { ::Quark.quark_delegate_md.quark_delegate_Message.singleton }
    static quark_delegate_Ping_md: -> { ::Quark.quark_delegate_md.quark_delegate_Ping.singleton }
    static quark_delegate_Pong_md: -> { ::Quark.quark_delegate_md.quark_delegate_Pong.singleton }
    static quark_delegate_Test_md: -> { ::Quark.quark_delegate_md.quark_delegate_Test.singleton }
    static quark_List_quark_Object__md: -> { ::Quark.quark_delegate_md.quark_List_quark_Object_.singleton }



    def initialize()
        self.__init_fields__

        nil
    end




    def _getClass()
        
        return nil

        nil
    end

    def _getField(name)
        
        return nil

        nil
    end

    def _setField(name, value)
        
        nil

        nil
    end

    def __init_fields__()
        

        nil
    end


end
CLASS_Root.unlazy_statics
end # module MODULE_quark_delegate_md
end # module Quark
