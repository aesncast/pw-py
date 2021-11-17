#!/usr/bin/env python3

# pw - python version

import sys
import os
import getpass
import copy

import argparse
import clipboard

# local imports
from pw.sequence import execute_sequence
from pw.transform import *
from pw.pwlist import *
from pw.util import *
import pw.config

pws = None # the loaded domain / user / sequence db
fp = "" # the filepath to use to store / load from

def complete(args):
    if not args.domain:
        for domain in pws.domains.keys():
            print(domain)
    
    else:
        domain = pws.domains.get(args.domain)
        for user in domain.users.keys():
            print(user)
    
    return 0


def show_transformations():
    for t in transformations.values():
        print(t.get_doc(), "\n")


def load_pws_from_default_paths():
    """searches the default paths for pwlist files"""
    global pws
    global fp
    
    vprintf("loading from path: '%s'", pwlist4_path)
    pws = load_pwlist4(pwlist4_path)
    fp = pwlist4_path
    
    if not pws:
        vprintf("nothing found, trying to load legacy file '%s'", pwlist2_legacy_path)
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
            

def import_pwfile4(path, force=False):
    """import domains, users and sequences from a given path"""
    global pws
    global fp
    
    backup_path = fp + ".old"
    vprintf("backing up current pwlist4 to %s", backup_path)
    save_pwlist4(backup_path, pws)
    
    vprintf("importing %s", path)
    pws2 = load_pwlist(path)
    
    if not pws2:
        err("could not import from '%s'", path)
        return 1
    
    er = validate_pwfile(pws2)
    
    if er:
        err("%s", er)
        return 1
    
    to_rename = []
    
    for seq in pws2.sequences.values():
        vprintf("importing sequence %s", seq.name)
        lseq = pws.sequences.get(seq.name)
        
        if not lseq:
            pws.sequences[seq.name] = copy.deepcopy(seq)
            continue
        
        if seq == lseq:
            # nothing to be done, local and imported sequences are identical
            # in name and structure
            continue
        
        nname = raise_namecount(seq.name)
        warn("imported sequence %s differs from local sequence %s, renaming imported sequence to %s", seq.name, lseq.name, nname)
        
        to_rename.append((seq.name, nname))
        # cant rename during iteration because keys will change, causing errors
    
    for old, new in to_rename:
        pws2.rename_sequence(old, new)
        pws.sequences[new] = pws2.sequences.get(new)
        
    
    for domain in pws2.domains.values():
        vprintf("importing domain %s", domain.name)
        ldomain = pws.domains.get(domain.name)
        
        if ldomain:
            if not force:
                a = prompt("domain %s found locally, merge?" % domain.name, default=0)
                if a == 'n':
                    vprintf("skipping domain %s", domain.name)
                    continue
        else:
            pws.domains[domain.name] = Domain(domain.name)
            ldomain = pws.domains.get(domain.name)
            
        for user in domain.users.values():
            vprintf("importing user %s", user.name)
            luser = ldomain.users.get(user.name)
            
            if not luser:
                ldomain.users[user.name] = User(user.name, user.sequence)
                continue
                
            seq = pws2.sequences.get(user.sequence)
            lseq = pws.sequences.get(luser.sequence)
            
            # special case:
            # local pws has a sequence named user.sequence
            # but it differs from imported sequence seq.
            # this case is not possible if those sequences are renamed
            # before we come here (see above for importing sequences).
            
            if seq == lseq:
                continue
            
            if force:
                pws.domains[domain.name].users[user.name].sequence = user.sequence
            else:
                # same domain, same user, different sequence
                a = prompt("imported user %s of domain %s uses a different sequence (%s) than the one the local user uses (%s). overwrite sequence of local user with the one of the imported user? (sequence will not be erased)" % (user.name, domain.name, seq.name, lseq.name), default=1)
                
                if a == 'y':
                    pws.domains[domain.name].users[user.name].sequence = user.sequence
                
    
    defa = pws2.get_sequence('DEFAULT')
    ldefa = pws.get_sequence('DEFAULT')
    if defa != ldefa:
        if force:
            pws.default = defa.name
        else:
            a = prompt("imported default sequence (%s) differs from local default sequence (%s). use imported sequence (%s) as new default?" % (defa.name, ldefa.name, defa.name), default=1)
            
            if a == 'y':
                pws.default = defa.name
    
    er = validate_pwfile(pws)
    
    if er:
        err("%s", er)
        return 1
    
    printf("import successful, saving changes to %s", fp)
    save_pwlist4(fp, pws)
    return 0
    
    
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
        vprintf("loading from file: '%s'", args.file)
        pws = load_pwlist(args.file)
        fp = args.file
    else:
        load_pws_from_default_paths()
    
    err = validate_pwfile(pws)
        
    if err:
        err("%s", err)
        return 1
    
    if getattr(args, 'import'):
        return import_pwfile4(getattr(args, 'import'), args.force)
        
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
    vprintf("saving changes to '%s'", fp)
    save_pwlist4(fp, pws)
    
    timeout = 5
    vprintf("password copied, clearing in %d seconds", timeout)
    clipboard.copy(pw)
    
    input_timeout(5)
    clipboard.copy("")
    
    return 0

    
def get_argument_parser():
    """creates and returns a parser for the command line arguments"""
    parser = argparse.ArgumentParser(prog=PROG, formatter_class=argparse.RawDescriptionHelpFormatter, description="""password generator v%s
by %s""" % (pw.config.VERSION, pw.config.AUTHOR))

    parser.add_argument('--version', action='version', version="%s v%s" % (pw.config.PROG, pw.config.VERSION))
    parser.add_argument('-v', '--verbose', help="display extra information", action="store_true")
    parser.add_argument('-q', '--quiet', help="display no messages", action="store_true")
    parser.add_argument('-l', '--list', help="list domains or users of a given domain", action="store_true")
    parser.add_argument('-s', '--sequence', help="generation sequence", default=None)
    parser.add_argument('-f', '--file', help="pwlist2 or pwlist4 file to use", default=None)
    parser.add_argument('-i', '--import', help="pwlist4 file to import", default=None)
    parser.add_argument('--force', help="used with -i to force overwrite of local pwfile", action="store_true")
    parser.add_argument('--transformations', help="view available transformation functions", action="store_true")
    # parser.add_argument('-i', '--import', help="pwlist2 or pwlist4 file to import", default=None)

    # these are optional because argparse is bad
    parser.add_argument('domain', help="""the domain""", nargs="?")
    parser.add_argument('user', help="""the user""", nargs="?")

    return parser


def __main__():
    args = get_argument_parser().parse_args()

    pw.config._VERBOSE = args.verbose
    pw.config._QUIET = args.quiet
    
    if args.transformations:
        show_transformations()
        sys.exit(0)

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
