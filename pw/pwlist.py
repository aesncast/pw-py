#!/usr/bin/env python3
# pw_pwlist.py: pwlist2 and pwlist4 parsers and structures

import os
import appdirs

from pw.transform import transformations
from pw.sequence import Sequence, Segment, Param
from pw.config import PROG, AUTHOR
from pw.util import *

localdir = appdirs.user_data_dir()
datadir = appdirs.user_data_dir(PROG, AUTHOR)

pwlist2_legacy_path = os.path.join(localdir, ".pwlist2")
pwlist4_path = os.path.join(datadir, "pwlist4")

parent = os.path.dirname(pwlist4_path)
if not os.path.exists(parent):
    os.makedirs(parent)

builtin_sequence_names = ["LEGACY1", "LEGACY2", "DEFAULT"]
forbidden_name_symbols = [':', ';', ',', '<', '>', '[', ']']

# structures
class Pwfile():
    def __init__(self):
        self.domains = {}
        self.sequences = {}
        self.default = "" # default sequence
        
        legacy1 = Sequence()
        legacy1.name = "LEGACY1"
        
        legacy1seg = Segment()
        legacy1seg.function = "bad_legacy1"
        legacy1seg.parameters = [Param("field", "key"), Param("field", "domain")]
        legacy1.segments.append(legacy1seg)
        self.sequences["LEGACY1"] = legacy1
        
        legacy2 = Sequence()
        legacy2.name = "LEGACY2"
              
        legacy2seg = Segment()
        legacy2seg.function = "bad_legacy2"
        legacy2seg.parameters = [Param("field", "key"), Param("field", "domain"), Param("field", "user")]
        legacy2.segments.append(legacy2seg)
        self.sequences["LEGACY2"] = legacy2
        
    def get_sequence(self, name):
        if name == "DEFAULT":
            return self.sequences.get(self.default)
        else:
            return self.sequences.get(name)
        
    def rename_sequence(self, seqname, newname):
        seq = self.get_sequence(seqname)
        
        if not seq:
            return
        
        check_forbidden_symbol_in_name(newname)
        
        if self.get_sequence(newname):
            raise ValueError("sequence '%s' already exists" % (newname))
    
        seq.name = newname
        self.sequences[newname] = seq
        # del self.sequences[seqname]
        
        if self.default == seqname:
            self.default = newname
            
        for domain in self.domains.values():
            for user in domain.users.values():
                if user.sequence == seqname:
                    user.sequence = newname
        
        
class Domain():
    def __init__(self, name = ""):
        self.name = name
        self.users = {}
        
class User():
    def __init__(self, name = "", sequence = ""):
        self.name = name
        self.sequence = sequence
        

# functions
def readfile(path):
    """read entire file"""
    if not os.path.exists(path):
        return None
    
    with open(path, mode='r') as f:
        return f.readlines()

def load_pwlist2(path):
    """read a pwlist2 and returns a Pwfile structure"""
    ret = Pwfile()
    lines = readfile(path)
    
    if not lines:
        return None
    
    for line in lines:
        line = line.strip()
        
        if not line or line[0] == "#":
            continue
        
        i = line.find(":")
        
        if i < 1:
            warn("line '%s' in pwfile2 '%s' contains no domain", line, path)
            continue
        
        domain_name = line[0:i]
        line = line[(i+2):]
        
        domain = Domain(domain_name)
        
        if not line:
            u = User('')
            u.sequence = "LEGACY1"
            domain.users[''] = u
            ret.domains[domain_name] = domain
            continue
        
        users = [User(u.strip()) for u in line.split(',') if u.strip()]
        
        if not users:
            u = User('')
            u.sequence = "LEGACY1"
            domain.users[''] = u
            
        else:
            for user in users:
                user.sequence = "LEGACY2"
                domain.users[user.name] = user
        
        ret.domains[domain_name] = domain
        
    ret.default = "LEGACY2"
    
    return ret


def check_forbidden_symbol_in_name(name):
    for sb in forbidden_name_symbols:
        if sb in name:
            raise ValueError("illegal symbol '" + sb + "' in name " + name)


def parse_pwlist4_domain_name(line):
    line = line.strip()
    
    if not line or not line.endswith(':'):
        raise ValueError("domain name must end with :")
    
    check_forbidden_symbol_in_name(line[:-1])
    
    return line[:-1]

    
def parse_pwlist4_domain(lines, i):
    ret = Domain()
    
    ret.name = parse_pwlist4_domain_name(lines[i])
    
    i += 1
    
    while i < len(lines):
        line = lines[i]
        
        if not line.strip():
            i += 1
            continue
        
        if line.startswith("\t") or line.startswith(" "):
            line = line.strip()
            
            if not line:
                i += 1
                continue
            
            if line.startswith('-'):
                line = " " + line
            parts = [p.strip() for p in line.split(" - ")]
            
            if len(parts) != 2:
                raise ValueError("invalid user entry '%s' in domain '%s'" % (line, ret.name))
            
            usr, seq = parts
            
            check_forbidden_symbol_in_name(usr)
            check_forbidden_symbol_in_name(seq)
            
            user = User()
            user.name = usr
            user.sequence = seq
            
            ret.users[usr] = user
            i += 1
            
        else:
            break
        
    return i, ret


def skip_whitespace(s, i):
    while i < len(s) and str.isspace(s[i]):
        i += 1
    
    return i

        
def parse_identifier(s, i):
    """parses a identifier (name)"""
    
    ret = ""
    ls = len(s)
    
    if i >= ls:
        raise ValueError("expected identifier in segment")

    c = s[i]
    
    if c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
        raise ValueError("unexpected symbol '%s' in identifier" % c)
    
    ret += c
    i += 1
    
    while i < ls:
        c = s[i]
        
        if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
            ret += c
            i += 1
            continue
        else:
            break
        
    return i, ret

        
def parse_string(s, i):
    """parses a string in quotation marks " " """
    
    ret = ""
    ls = len(s)
    
    if i >= ls:
        raise ValueError("expected identifier in segment")

    c = s[i]
    
    if c != "\"":
        raise ValueError("unexpected symbol '%s' in string" % c)
    
    i += 1
    
    while i < ls:
        c = s[i]
        
        if c == "\"":
            break
        else:
            ret += c
            i += 1
            continue
    
    if i >= ls or s[i] != "\"":
        raise ValueError("expected \" to terminate string")
    
    i += 1
        
    return i, ret

        
def parse_number(s, i):
    """parses an integer"""
    
    ret = ""
    ls = len(s)
    
    if i >= ls:
        raise ValueError("expected identifier in segment")

    c = s[i]
    
    if not str.isdigit(c):
        raise ValueError("unexpected symbol '%s' in number" % c)
    
    ret += c
    i += 1
    
    while i < ls:
        c = s[i]
        
        if str.isdigit(c):
            ret += c
            i += 1
            continue
        else:
            break
        
    return i, int(ret)


def parse_param(s, i):
    """parses a parameter"""
    
    ret = Param()
    i = skip_whitespace(s, i)
    ls = len(s)
    
    if i >= ls:
        raise ValueError("expected symbol, got EOF in segment parameter")
    
    c = s[i]
    
    if c == "$":
        i, ident = parse_identifier(s, i+1)
        ret.typ = "field"
        ret.value = ident
    elif str.isdigit(c):
        i, num = parse_number(s, i)
        ret.typ = "number"
        ret.value = num
    else:
        i, val = parse_string(s, i)
        ret.typ = "string"
        ret.value = val
    
    return i, ret

        
def parse_params(s, i):
    """parses arguments of a segment"""
    
    ret = []
    ls = len(s)
    
    i = skip_whitespace(s, i)
       
    if i >= ls:
        raise ValueError("expected symbol '(', got EOF in segment parameters")
    
    if s[i] != "(":
        raise ValueError("unexpected symbol '%s' in segment parameters" % (s[i]))
        
    i += 1

    while i < ls:
        c = s[i]
        
        if str.isspace(c):
            i += 1
            continue
        
        if c == ')':
            break
        
        i, param = parse_param(s, i)
        ret.append(param)
        
        j = skip_whitespace(s, i)
        
        if j < ls:
            if s[j] == ")":
                continue
            
            if s[j] == ",":
                i = j + 1
                continue
            
            raise ValueError("expected ')' or ',', got '%s' in segment parameters" % s[j])
        
    if i >= ls or s[i] != ")":
        raise ValueError("expected symbol ')', got EOF in segment parameters")
    
    i += 1
    
    return i, ret
        

def parse_segment(s, i):
    """parses a single segment"""
    
    ret = Segment()
    params = []
    
    i = skip_whitespace(s, i)
    i, func = parse_identifier(s, i)
    i, params = parse_params(s, i)
    
    ret.function = func
    ret.parameters = params
    
    return i, ret
    

def parse_segments(s):
    """parses sequence segments from a string"""
    ret = []
    
    i = 0
    while i < len(s):
        c = s[i]
        
        if str.isspace(c):
            i += 1
            continue
    
        i, seg = parse_segment(s, i)
        
        ret.append(seg)
        
    return ret


def parse_pwlist4_sequence_name(line):
    begin = line.find("[")
    end = line.find("]")
    
    if begin < 0:
        raise ValueError("couldnt find symbol [ in sequence name")
    
    if end < 0:
        raise ValueError("couldnt find symbol ] in sequence name")
    
    if end < begin:
        raise ValueError("] must come after [ in sequence name")
    
    ret = line[begin+1:end]
    check_forbidden_symbol_in_name(ret)
    
    return ret
    
    
def parse_pwlist4_sequence(lines, i):
    ret = Sequence()
    
    ret.name = parse_pwlist4_sequence_name(lines[i])
    
    if ret.name.startswith("+"):
        ret.default = True
        ret.name = ret.name[1:]
        
        if not ret.name:
            raise ValueError("sequence name cannot be empty")
    
    i += 1
    j = i
    
    while lines[i] != "\n" and i < len(lines):
        i += 1
        
    segstr = str.join(" ", [l.strip() for l in lines[j:i]])
    ret.segments = parse_segments(segstr)
    
    return i, ret
                

def load_pwlist4(path):
    """loads a pwlist4 file and returns a Pwfile structure"""
    ret = Pwfile()
    lines = readfile(path)
    
    if not lines:
        return None
    
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        if not line.strip():
            i += 1
            continue
        
        if line[0] == '#':
            # comment
            i += 1
            continue
        
        try:
            if line[0] == '[':
                # sequence
                i, seq = parse_pwlist4_sequence(lines, i)
                
                if seq.name in ret.sequences.keys():
                    raise ValueError("duplicate sequence name '%s' in line %d" % (seq.name, i))
                
                if seq.default:
                    if ret.default != "":
                        raise ValueError("multiple default sequences not allowed: '%s' and '%s' are both marked default with '+'" % (seq.name, ret.default))
                    else:
                        ret.default = seq.name
                
                ret.sequences[seq.name] = seq
                
            elif line[0] != ' ' and line[0] != '\t':
                i, domain = parse_pwlist4_domain(lines, i)
                
                if domain.name in ret.domains.keys():
                    raise ValueError("duplicate domain name '%s' in line %d" % (domain.name, i))
                
                ret.domains[domain.name] = domain
            
            else:
                raise ValueError("unexpected symbol '%s' in line %d" % (line[0], i))
            
        except ValueError as e:
            if hasattr(e, "message"):
                warn("%s", e.message)
            else:
                warn("%s", e)
                
            i += 1
    
    # fallback, decent generator
    # technically not "built-in"
    if not ret.sequences.get("good_password"):
        gpw = Sequence()
        gpw.name = "good_password"
        
        gpwseg1 = Segment()
        gpwseg1.function = "init"
        gpwseg1.parameters = [Param("field", "key"), Param("field", "domain"), Param("field", "user")]
        gpw.segments.append(gpwseg1)
        
        gpwseg2 = Segment()
        gpwseg2.function = "diceware_short"
        gpwseg2.parameters = []
        gpw.segments.append(gpwseg2)
        
        gpwseg3 = Segment()
        gpwseg3.function = "capitalize_some"
        gpwseg3.parameters = []
        gpw.segments.append(gpwseg3)
        
        gpwseg4 = Segment()
        gpwseg4.function = "add_some_simple_special_characters"
        gpwseg4.parameters = []
        gpw.segments.append(gpwseg4)
        ret.sequences["good_password"] = gpw
        
    if not ret.default:
        ret.default = "good_password"
        
    return ret


def load_pwlist(path):
    """loads a pwlist2 or pwlist4 file from a given path"""
    if path.endswith(".pwlist2"):
        return load_pwlist2(path)
    
    if path.endswith(".pwlist4"):
        return load_pwlist4(path)
    
    pws = load_pwlist4(path)
    
    if not pws:
        pws = load_pwlist2(path)
        
    return pws


def segment_param_to_string(param):
    if param.typ == "field":
        return "$" + param.value
    elif param.typ == "number":
        return str(param.value)
    else:
        return "\"" + param.value + "\""


def pwfile_to_string(pws):
    """converts a Pwfile to pwlist4"""
    s = ""
    
    for domain in pws.domains.values():
        s += "\n\n" + domain.name + ":"
        
        for usr in domain.users.values():
            s += "\n    " + usr.name + " - " + usr.sequence


    if pws.sequences:
        s += "\n\n# Sequences"
        s += "\n# don't change, only copy & make new ones to be safe,"
        s += "\n# otherwise you risk losing passwords if you forget"
        s += "\n# the sequences."
        
    for seq in pws.sequences.values():
        if seq.name in builtin_sequence_names:
            continue
        
        s += "\n["
        
        if pws.default == seq.name:
            s += "+"
            
        s += seq.name + "]"
        
        for seg in seq.segments:
            s += "\n    " + seg.function
            s += "("
            
            params = [segment_param_to_string(p) for p in seg.parameters]
            
            s += str.join(", ", params)
            s += ")"
        
        s += "\n"
        
    s += "\n"
    
    return s


def save_pwlist4(path, pws):
    """saves a Pwfile structure to a given path as a pwlist4 file"""
    if not pws or not pws.domains:
        vprintf("nothing to export")
        
    parent = os.path.dirname(path)
    if parent and parent != "." and not os.path.exists(parent):
        os.makedirs(parent)
    
    # domains
    s = """# auto generated pwlist4 file containing sequences, domains and users.
# feel free to edit / add but formatting and comments will be lost."""

    s += pwfile_to_string(pws)
            
    with open(path, mode='w') as f:
        f.write(s)


def validate_pwfile(pws):
    """returns an error message if pws is invalid or None if it's valid"""
    if not pws:
        return "file is empty"
    
    seq_names = [*pws.sequences.keys()]
    seq_names.append("DEFAULT")
    
    for domain in pws.domains.values():
        for fs in forbidden_name_symbols:
            if fs in domain.name:
                return "domain " + domain.name + " contains forbidden symbol '" + fs + "'"
        
        usrnames = domain.users.keys()
        
        if len(set(usrnames)) != len(usrnames):
            return "domain " + domain.name + " contains duplicate users"
        
        for usr in domain.users.values():
            for fs in forbidden_name_symbols:
                if fs in usr.name:
                    return "user " + usr.name + " of domain " + domain.name + " contains forbidden symbol '" + fs + "'"
            
            if not (usr.sequence in seq_names):
                return "user " + usr.name + " of domain " + domain + " uses unknown sequence " + usr.sequence
    
    for seq in pws.sequences.values():
        for fs in forbidden_name_symbols:
            if fs in seq.name:
                return "sequence name " + seq.name + " contains forbidden symbol '" + fs + "'"
            
        if not seq.segments:
            return "sequence " + seq.name + " contains no segments"
        
        for seg in seq.segments:
            func = transformations.get(seg.function)
            
            if not func:
                return "function '%s' not recognized in sequence %s" % (seg.function, seq.name)
            
            if func.params != len(seg.parameters):
                return "function '%s' expects %d parameters, %d given" % (seg.function, func.params, len(seg.parameters))
            
    return None
