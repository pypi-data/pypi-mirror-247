from zrcl3.hackthon.caller import get_caller_func, get_caller_name, get_caller_trace, get_self_name

def t_func():
    return get_self_name(), get_caller_name()

class dummy:
    def run(self):
        w = t_func()
        b = get_caller_trace()
        c =  get_caller_func()
        
        assert w == ("t_func", "dummy.run")
        assert len(b) > 0
        assert c == test_caller_func
        
def test_caller_func():
    assert t_func() == ("t_func", "test_caller_func")
    
    d = dummy()
    d.run()