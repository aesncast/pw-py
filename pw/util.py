#!/usr/bin/env python3
# pw_util.py: utility functions

_VERBOSE = False
_QUIET = False

def printf(fmt, *args):
    """Printf"""
    global _QUIET
    if not _QUIET:
        print(fmt % args)

def vprintf(fmt, *args):
    """Verbose Printf"""
    global _VERBOSE
    global _QUIET
    if _VERBOSE and not _QUIET:
        print(fmt % args)

def info(fmt, *args):
    """Prints an info message"""
    global _QUIET
    if not _QUIET:
        print(("[ * ] %s" % fmt) % args)

def warn(fmt, *args):
    """Prints a warning message"""
    global _QUIET
    if not _QUIET:
        print(("[ ! ] %s" % fmt) % args)

def err(fmt, *args):
    """Prints an error message"""
    global _QUIET
    if not _QUIET:
        print(("[!!!] %s" % fmt) % args)
        

def multisplit(s, *args):
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
