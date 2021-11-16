#!/usr/bin/env python3
# pw_sequence 

from pw.transform import transformations
from pw.util import *

class Sequence():
    def __init__(self, name = ""):
        self.name = name
        self.segments = []
        self.default = False
    
    def __eq__(self, other):
        return self.segments == other.segments


class Segment():
    def __init__(self, function = ""):
        self.function = function
        self.parameters = []
        
    def __eq__(self, other):
        return (self.function == other.function) and (self.parameters == other.parameters)
        

# types: field, number, string
class Param():
    def __init__(self, typ="", value=None):
        self.typ = typ
        self.value = value
        
    def __eq__(self, other):
        return (self.typ == other.typ) and (self.value == other.value)
        
        
def param_value(param, key, domain, user):
    if param.typ == "field":
        if param.value == "key":
            return key
        elif param.value == "domain":
            return domain
        elif param.value == "user":
            return user
        else:
            raise ValueError("unknown field '$%s'" % param.value)
    else:
        return param.value


def execute_sequence(seq, key, domain, user):
    """executes the given sequence object with the parameters provided"""
    ret = ""
    
    for seg in seq.segments:
        func = transformations.get(seg.function)
        
        if not func:
            raise ValueError("function '%s' not recognized" % seg.function)
        
        if func.params != len(seg.parameters):
            raise ValueError("function %s expects %d parameters, %d given" % (seg.function, func.params, len(seg.parameters)))
        
        param_values = [param_value(p, key, domain, user) for p in seg.parameters]
        ret = func(ret, *param_values)
    
    if isinstance(ret, bytes):
        ret = ret.decode()
    elif isinstance(ret, int):
        ret = str(int)
    
    return ret
