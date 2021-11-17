#!/usr/bin/env python3
# pw_util.py: utility functions

import os
import pw.config

def printf(fmt, *args):
    """Printf"""
    if not pw.config._QUIET:
        print(fmt % args)

def vprintf(fmt, *args):
    """Verbose Printf"""
    if pw.config._VERBOSE and not pw.config._QUIET:
        print(fmt % args)

def info(fmt, *args):
    """Prints an info message"""
    if not pw.config._QUIET:
        print(("[ * ] %s" % fmt) % args)

def warn(fmt, *args):
    """Prints a warning message"""
    if not pw.config._QUIET:
        print(("[ ! ] %s" % fmt) % args)

def err(fmt, *args):
    """Prints an error message"""
    if not pw.config._QUIET:
        print(("[!!!] %s" % fmt) % args)
        

def multisplit(s, *args):
    """like str.split, but takes any number of arguments to split at."""
    if not args:
        return [s]
    
    if isinstance(args[0], list):
        return multisplit(s, *args[0], *args[1:])
    
    return [y for x in s.split(args[0]) for y in multisplit(x, *args[1:])]

        
def input_default(s, default=None):
    try:
        return input(s)
    except:
        return default
    
def case_insensitive_in(x, items):
    inside = False
    x = str.lower(x)
    
    for item in items:
        if x == str.lower(item):
            inside = True
            break
    
    return inside

def prompt(msg, options=['y', 'n'], default=-1, case_sensitive=False):
    """prompts user for a given option and returns option"""
    
    has_default = (default >= 0) and (default < len(options))
    default_choice = options[default] if has_default else None
    choices_str = "(" + str.join("/", options) + ")"
    
    if has_default:
        choices_str += " [" + default_choice + "]"
        
    choice = default_choice
        
    while True:
        choice = input_default(msg + " " + choices_str + ": ", default_choice)
        
        if choice == "" or choice == "\n" or choice == "\r\n":
            choice = default_choice
            
        inside = False
        
        if case_sensitive:
            inside = choice in options
        else:
            inside = case_insensitive_in(choice, options)
        
        if not inside:
            inside = choice == default_choice
        
        if not inside:
            warn("please select one of the choices")
            continue
        
        break

    return choice


def raise_namecount(oldname):
    s = oldname.split("_")
    
    if len(s) < 2:
        return oldname + "_2"
    
    i = 1
    try:
        i = int(s[-1])
    except:
        return oldname + "_2"
    
    return str.join('_', s[:-1] + [str(i + 1)])


def input_timeout(timeout=5):
    try:
        if os.name in ["nt", "win32"]:
            import msvcrt, sys, time
            start_time = time.time()
            input = ''
            while True:
                if msvcrt.kbhit():
                    chr = msvcrt.getche()
                    if ord(chr) == 13: # enter_key
                        break
                    elif ord(chr) >= 32: #space_char
                        input += chr
                if len(input) == 0 and (time.time() - start_time) > timeout:
                    break

            print()
            return input

        else:
            import select
            return select.select([sys.stdin], [], [], timeout)
    except:
        return ""
