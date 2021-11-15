#!/usr/bin/env python3

# pw - python version

import sys
import os
import select
import getpass

import argparse
import clipboard

# local imports
from pw.sequence import execute_sequence
from pw.transform import *
from pw.pwlist import *
from pw.config import *
from pw.util import *

pws = None
fp = ""

def complete(args):
    if not args.domain:
        for domain in pws.domains.keys():
            print(domain)
    
    else:
        domain = pws.domains.get(args.domain)
        for user in domain.users.keys():
            print(user)
    
    return 0


def load_pws_from_default_paths():
    """searches the default paths for pwlist files"""
    global pws
    global fp
    
    vprintf("loading %s", pwlist4_path)
    pws = load_pwlist4(pwlist4_path)
    fp = pwlist4_path
    
    if not pws:
        vprintf("nothing found, trying to load legacy file %s", pwlist2_legacy_path)
        pws = load_pwlist2(pwlist2_legacy_path)
        
        if pws:
            c = prompt("legacy pwlist2 found but no pwlist4, convert?", default=0)
            
            if c == "y":
                save_pwlist4(pwlist4_path, pws)
                pws = load_pwlist4(pwlist4_path)
        else:
            vprintf("nothing found, creating empty pwlist4 file")
            pws = Pwfile()
            save_pwlist4(pwlist4_path, pws)
            pws = load_pwlist4(pwlist4_path)
    
    
def get_sequence_name(args):
    """gets the sequence name provided by command line arguments, or
    gets the sequence name of the specified user if no sequence
    was given in command line arguments.
    """
    if args.sequence:
        vprintf("using sequence name %s", args.sequence)
        return args.sequence
    
    if not pws:
        vprintf("using default sequence")
        return "DEFAULT"
    
    domain = pws.domains.get(args.domain)
    
    if not domain:
        vprintf("using default sequence")
        return "DEFAULT"
    
    usr = domain.users.get(args.user)
    
    if not usr:
        vprintf("using default sequence")
        return "DEFAULT"
    
    vprintf("using sequence %s of user %s", usr.sequence, args.user)
    
    return usr.sequence


def add_user(domain, user, seqname):
    """adds or modifies a user in the pwfile"""
    global pws
    
    dom = pws.domains.get(domain)
    
    if not dom:
        vprintf("adding new domain %s", domain)
        pws.domains[domain] = Domain(domain)
        dom = pws.domains[domain]
    
    usr = dom.users.get(user)
    
    if not usr:
        vprintf("adding new user %s to domain %s", user, domain)
        dom.users[user] = User(user)
        usr = dom.users[user]
    
    vprintf("setting sequence of user %s of domain %s to %s", user, domain, seqname)
    usr.sequence = seqname


# main
def main(args):
    """main function with parsed arguments from argparse"""
    global pws
    global fp
    
    if args.file:
        vprintf("loading %s", args.file)
        pws = load_pwlist(args.file)
        fp = args.file
    else:
        load_pws_from_default_paths()
    
    err = validate_pwfile(pws)
        
    if err:
        err("%s", err)
        return 1
        
    if not args.domain:
        args.domain = ""
    
    if not args.user:
        args.user = ""
        
    if args.list:
        return complete(args)
        
    seqname = get_sequence_name(args)
    seq = pws.get_sequence(seqname)
    
    if not seq:
        err("sequence '%s' not found", seqname)
        return 1
    
    key = None
    
    try:
        key = getpass.getpass("Encryption key: ")
    except EOFError:
        print("\naborted")
        return 0
    except KeyboardInterrupt:
        print("\naborted")
        return 0
    
    pw = execute_sequence(seq, key, args.domain, args.user)
    add_user(args.domain, args.user, seq.name)
    vprintf("saving changes")
    save_pwlist4(fp, pws)
    
    timeout = 5
    vprintf("password copied, clearing in %d seconds", timeout)
    clipboard.copy(pw)
    
    try:
        select.select([sys.stdin], [], [], timeout)
    finally:
        clipboard.copy("")
    
    return 0
    
def get_argument_parser():
    """creates and returns a parser for the command line arguments"""
    parser = argparse.ArgumentParser(prog=PROG, formatter_class=argparse.RawDescriptionHelpFormatter, description="""password generator v%s
by %s""" % (VERSION, AUTHOR))

    parser.add_argument('--version', action='version', version="%s v%s" % (PROG, VERSION))
    parser.add_argument('-v', '--verbose', help="display extra information", action="store_true")
    parser.add_argument('-q', '--quiet', help="display no messages", action="store_true")
    parser.add_argument('-l', '--list', help="list domains or users of a given domain", action="store_true")
    parser.add_argument('-s', '--sequence', help="generation sequence", default=None)
    parser.add_argument('-f', '--file', help="pwlist2 or pwlist4 file to use", default=None)
    # parser.add_argument('-i', '--import', help="pwlist2 or pwlist4 file to import", default=None)

    # these are optional because argparse is bad
    parser.add_argument('domain', help="""the domain""", nargs="?")
    parser.add_argument('user', help="""the user""", nargs="?")

    return parser


def __main__():
    args = get_argument_parser().parse_args()

    _VERBOSE = args.verbose
    _QUIET = args.quiet

    ret = 0
    try:
        ret = main(args)
    except Exception as e:
        if hasattr(e, "message"):
            err("%s", e.message)
        else:
            err("%s", e)
            
        ret = 1
        
    sys.exit(ret)
    
    
if __name__ == "__main__":
    __main__()
