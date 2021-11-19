#!/usr/bin/env python3
# compability_tests:
# contains tests to make sure compatible passwords for
# old pw versions can be generated.

import os
import sys
import inspect

from pw.sequence import Sequence, execute_sequence
from pw.pwlist import parse_pwlist4_sequence
from pw.transform import Transformation, transformations

class Test():
    def __init__(self, to_test, cases):
        self.to_test = to_test
        self.cases = cases

class Testcase():
    def __init__(self, key, domain, user, value):
        self.key = key
        self.domain = domain
        self.user = user
        self.value = value

sequences = {}
tests = []


def execute_function(f, k, d, u):
    param_count = len(inspect.signature(f).parameters)
    params = ["", k, d, u][:param_count]

    return f(*params)

def run_tests():
    global tests
    
    if not tests:
        raise ValueError("no tests")
    
    for test in tests:
        if not test.cases:
            raise ValueError("test has no test cases")
        
        f = None
        name = ""
        
        if isinstance(test.to_test, Sequence):
            f = lambda k, d, u: execute_sequence(test.to_test, k, d, u)
            name = test.to_test.name
        elif isinstance(test.to_test, Transformation):
            f = lambda k, d, u: execute_function(test.to_test.function, k, d, u)
            name = test.to_test.function.__name__
        else:
            raise ValueError("invalid testing object")
        
        for case in test.cases:
            val = f(case.key, case.domain, case.user)
            if val != case.value:
                raise AssertionError("assertion failed: %s(%s, %s, %s) == %s, got %s" % (name, repr(case.key), repr(case.domain), repr(case.user), repr(case.value), repr(val)))


def parse_function_name(line):
    line = line.strip()
    
    if not line or not line.endswith(':'):
        raise ValueError("function name to test must end with :")
    
    return line[:-1]


def parse_sequence_name(line):
    begin = line.find("(")
    end = line.find("):")
    
    if begin < 0:
        raise ValueError("couldnt find symbol ( in sequence name")
    
    if end < 0:
        raise ValueError("couldnt find symbol ( in sequence name")
    
    if end < begin:
        raise ValueError(") must come after ( in sequence name")
    
    ret = line[begin+1:end]
    
    return ret


def parse_string(line, j):
    ls = len(line)
    ret = ""
    
    while j < ls and line[j].isspace():
        j += 1
        
    if j >= ls:
        raise ValueError("expecting \" in string, got EOL")

    if line[j] != "\"":
        raise ValueError("expecting \" in string, got %s" % line[j])
    
    j += 1
    
    while j < ls and line[j] != "\"":
        c = line[j]
        
        if c == "\\":
            k = j + 1
            
            if k >= ls:
                raise ValueError("cannot break EOL")
            
            c2 = line[k]
            
            if c2 == 'n':
                ret += '\n'
            elif c2 == 't':
                ret += '\t'
            elif c2 == 'r':
                ret += '\r'
            else:
                ret += c2
                
            j += 2
            continue
        
        ret += line[j]
        j += 1
        continue
        
    if j >= ls:
        raise ValueError("expecting \" in string, got EOL")
    
    j += 1
    
    return j, ret


def parse_test_cases(lines, i):
    ls = len(lines)
    
    tstc = []
    while i < ls and lines[i].strip():
        line = lines[i].strip()
        
        j = 0
        j, key = parse_string(line, j)
        j, domain = parse_string(line, j)
        j, user = parse_string(line, j)
        j = line.find(" - ") + 3
        j, val = parse_string(line, j)
        
        tstc.append(Testcase(key, domain, user, val))
        
        i += 1
        
    i += 1
        
    return i, tstc
        

def parse_tests(fp):
    global tests
    tests = []
    
    lines = []
    
    with open(fp, 'r') as f:
        lines = f.readlines()

    if not lines:
        print("no tests found in %s" % fp)
        return 0

    i = 0
    ls = len(lines)
    
    while i < ls:
        line = lines[i]
        
        if not line.strip():
            i += 1
            continue
        
        c = line[0]
        
        if c == '#':
            # comment
            i += 1
            continue
        
        if c == '[':
            # sequence
            i, seq = parse_pwlist4_sequence(lines, i)
            sequences[seq.name] = seq
            
            continue
        
        if c == '(':
            # transform sequence test
            seqname = parse_sequence_name(line)
            seq = sequences.get(seqname)
            
            if not seq:
                raise ValueError("sequence '%s' not found in testdata" % seqname)
            
            i += 1
            
            i, testcases = parse_test_cases(lines, i)
            tests.append(Test(seq, testcases))
                
            continue
        
        else:
            # transform function test
            funcname = parse_function_name(line)
            func = transformations.get(funcname)
            
            if not func:
                raise ValueError("function '%s' not found" % funcname)
            
            i += 1
                
            i, testcases = parse_test_cases(lines, i)
            tests.append(Test(func, testcases))
                
            continue


if __name__ == "__main__":
    fp = os.path.dirname(__file__) + "/test_data.txt"
    parse_tests(fp)
    run_tests()
    print("all tests passed")
