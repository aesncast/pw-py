#!/usr/bin/env python3
# pw_transform.py: transformation functions
import base58 as b58
import base64 as b64
import hashlib
import random
import math
import inspect

from pw.wordlist import wordlist
from pw.util import *

def base58(s):
    """converts the input to base58"""
    if isinstance(s, str):
        s = s.encode()
    
    return b58.b58encode(s)

def base64(s):
    """converts the input to base64"""
    if isinstance(s, str):
        s = s.encode()
    
    return b64.b64encode(s)

def sha256(s):
    """gets the sha256 hash of the input"""
    if isinstance(s, str):
        s = s.encode()
        
    return hashlib.sha256(s).digest()

def sha512(s):
    """gets the sha512 hash of the input"""
    if isinstance(s, str):
        s = s.encode()
        
    return hashlib.sha512(s).digest()

def append(s, s2):
    """appends the parameter to the input at the end"""
    if not (isinstance(s, str)):
        s = s.decode()
    
    return s + str(s2)

def prepend(s, s2):
    """prepends the parameter to the input at the start"""
    if not (isinstance(s, str)):
        s = s.decode()
    
    return str(s2) + s

def init(s, key, domain, user):
    """appends key, domain and user to the input. generally used to initialize transformation sequences"""
    s = append(s, key)
    s = append(s, ":")
    s = append(s, user)
    s = append(s, "@")
    s = append(s, domain)
    return s

def cut(s, begin, end):
    """cuts the input from the beginning index to the end index, exclusive"""
    if not (isinstance(s, str)):
        s = s.decode()
        
    return s[begin:end]

def limit(s, n):
    """limits the input to n characters"""
    return cut(s, 0, n)

def replace(s, to_replace, replacement):
    """replaces a given string in the input with another string"""
    return s.replace(to_replace, replacement)

def to_int(s):
    """converts the bytes of the input to an integer"""
    if isinstance(s, str):
        s = s.encode()
    
    return int.from_bytes(s, "little")
    
def seed(s, min_int = 0, max_int = 2**32-1):
    """gets a deterministic seed in the given range from the input"""
    random.seed(s)
    return random.randint(min_int, max_int)
    
def make_unambiguous(s):
    """attempts to replace ambigous characters with not-so-ambiguous ones in the input"""
    # full list, don't implement: https://www.unicode.org/Public/security/latest/confusables.txt
    
    if not (isinstance(s, str)):
        s = s.decode()
        
    if len(s) == 0:
        return s
    
    #safe_characters = "abcdefghkmnpqrsuvwxyzABCDEFGHKMNPQRSUVWXY3456789"
    safe_characters = "abcdefghkmnpqrsuvwxyz"
    ls = len(safe_characters)-1
    unsafe_characters = "ZlLtTiIjJoO012"
    
    for unsafe in unsafe_characters:
        s = s.replace(unsafe, safe_characters[seed(s + unsafe, 0, ls)])
    
    return s

def add_special_characters(s, min_count, max_count, special_chars):
    """adds characters to the input"""
    if not (isinstance(s, str)):
        s = s.decode()
        
    ls = len(s)
    num_chars = min(seed(s, min_count, max_count), ls)
    
    if num_chars == 0:
        return s
    
    lsc = len(special_chars)-1
    
    dst = ls // num_chars
    pos = 0
    
    for i in range(0, num_chars):
        tmp = s + str(i)
        hsh = sha256(tmp)
        
        schar_seed = seed(hsh, 0, lsc)
        schar = special_chars[schar_seed]
        
        ipos = seed(tmp, pos, pos + dst)
        s = s[:ipos] + schar + s[ipos:]
        pos += dst + 1
        
    return s
        
        
def add_simple_special_characters(s, min_count, max_count):
    """adds a predefined set of special characters to the input"""
    return add_special_characters(s, min_count, max_count, "#+*%&[]=?_.:")

        
def add_some_special_characters(s, special_chars):
    """adds at most sqrt(len(s))/2 special characters to the input, but at least 1"""
    if not (isinstance(s, str)):
        s = s.decode()
    
    num_chars = math.floor(math.sqrt(len(s))/2)
    return add_special_characters(s, 1, num_chars, special_chars)


def add_some_simple_special_characters(s):
    """adds at most sqrt(len(s))/2 predefined special characters to the input, but at least 1"""
    if not (isinstance(s, str)):
        s = s.decode()
    
    num_chars = math.floor(math.sqrt(len(s))/2)
    return add_simple_special_characters(s, 1, num_chars)


def capitalize_some(s):
    """capitalizes some words found in the input, maybe all, but at least one"""
    if not (isinstance(s, str)):
        s = s.decode()
        
    words = multisplit(s, [" ", ".", "_"])
    words = list(filter(lambda w: w and w[0].isalpha(), words))
    lw = len(words)

    if lw == 0:
        # nothing to capitalize
        return s
    
    num_words = seed(s, 1, lw)
    
    rwords = random.sample(words, num_words)
    
    for rword in rwords:
        i = s.find(rword)
        
        if i < 0:
            continue
        
        s = s[:i] + str.upper(s[i]) + s[i+1:]
        
    return s


def diceware_list(s, min_count, max_count, words = wordlist):
    """generate word sequences of the given wordlist using the input as seed"""
    if not (isinstance(s, str)):
        s = s.decode()
        
    num_words = seed(s, min_count, max_count)
    
    l = []
    lwl = len(words)-1
    
    for i in range(0, num_words):
        hsh = sha256(s + str(i))
        l.append(words[seed(hsh, 0, lwl)])
        
    return str.join(' ', l)


def diceware(s, min_count, max_count):
    """generate word sequences of the default wordlist using the input as seed"""
    return diceware_list(s, min_count, max_count, wordlist)

def diceware_short(s):
    """generates 3 to 4 diceware words from the input"""
    return diceware(s, 3, 4)
    
def diceware_long(s):
    """generates 4 to 5 diceware words from the input"""
    return diceware(s, 4, 5)
        
        
####################
#      LEGACY      #
####################
def bad_make_easy_to_read(s):
    """DO NOT USE. arbitrary bad replacement"""
    if not (isinstance(s, str)):
        s = s.decode()
        
    s = replace(s, "i", "u")
    s = replace(s, "I", "P")
    s = replace(s, "l", "h")
    s = replace(s, "1", "T")
    s = replace(s, "0", "4")
    s = replace(s, "O", "r")
    s = replace(s, "o", "y")
    s = replace(s, "vv", "nW")
    s = replace(s, "VV", "K3")
    return s

def bad_seed_from_str(s):
    """DO NOT USE. arbitrary integer from a string"""
    if not (isinstance(s, str)):
        s = s.decode()
        
    b64_bytes = base64(s)[0:5]
    b64_bytes += b'\n'
    
    seedstr = "%0d" % int.from_bytes(b64_bytes[0:4], "little")
    if len(b64_bytes) > 4:
        seedstr += "%0d" % int.from_bytes(b64_bytes[4:], "little")
    
    return int(seedstr)

def bad_add_special_characters(s):
    """DO NOT USE. add deterministic special characters to a string"""
    
    seed = bad_seed_from_str(s)
    seps = seed % 5
    
    if seps > 0:
        i = int(len(s) / seps)
        nxt = i
        sepchars = ['_', '.', ',', ';', '!', '?', ' ']

        for x in range(0, seps):
            ws = sepchars[(seps + x) % len(sepchars)]

            s = s[:nxt] + ws + s[nxt:]
            nxt += i
    
    return str.strip(s)


def bad_legacy1(ret, key, domain):
    """DO NOT USE. the original"""
    ret = append(ret, key)
    ret = append(ret, ":")
    ret = append(ret, domain)
    ret = sha256(ret)
    ret = base64(ret)
    ret = ret.decode()
    ret = replace(ret, "+", "E")
    ret = replace(ret, "/", "a")
    ret = limit(ret, 20)
    ret = append(ret, "\n")
    
    return ret


def bad_legacy2(ret, key, domain, user):
    """DO NOT USE. pw version 2 to 3.1"""
    if len(user) == 0:
        ret = append(ret, key)
        ret = append(ret, "@")
        ret = append(ret, domain)
    else:
        ret = append(ret, key)
        ret = append(ret, ":")
        ret = append(ret, user)
        ret = append(ret, "@")
        ret = append(ret, domain)
        
    ret = sha512(ret)
    ret = base64(ret)
    ret = ret.decode()
    ret = replace(ret, "+", "E")
    ret = replace(ret, "/", "a")
    ret = limit(ret, 20)
    ret = bad_make_easy_to_read(ret)
    ret = limit(ret, 20)
    ret = bad_add_special_characters(ret)
    ret = limit(ret, 20)
    ret = append(ret, "\n")
    
    return ret

# transform segment functions
# name: param count
class Transformation():
    def __init__(self, func):
        self.params = len(inspect.signature(func).parameters) - 1
        self.function = func
        
    def __call__(self, *args):
        return self.function(*args)
    
    def get_doc(self):
        prms_ = inspect.signature(self.function).parameters
        prms = []
        
        i = False
        for p in prms_:
            if not i:
                i = True
                continue
            
            prms.append(p)
            
        doc = self.function.__name__
        
        doc += "("
        doc += str.join(", ", prms)
        doc += "):\n  "
        
        doc += self.function.__doc__
        
        return doc
        
        
transformations = {}

for func in [base58, base64, sha256, sha512, append, prepend, init, cut, limit, replace, to_int, seed, make_unambiguous, add_special_characters, add_simple_special_characters, add_some_special_characters, add_some_simple_special_characters, capitalize_some, diceware, diceware_short, diceware_long, bad_legacy1, bad_legacy2]:
    transformations[func.__name__] = Transformation(func)
