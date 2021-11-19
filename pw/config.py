#!/usr/bin/env python3
# pw_config.py: constants

PROG = "pw-py"
AUTHOR = "aesncast"
VERSION = "2021.11.19"

_VERBOSE = False
_QUIET = False


if __name__ == "__main__":
    # self-update
    from datetime import date
    today = date.today()
    todays = "%s.%s.%s" % (today.year, today.month, today.day)
    
    lines = []
    
    with open(__file__, 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        if lines[i].startswith("VERSION"):
            lines[i] = "VERSION = \"%s\"\n" % todays
            break
        
    newcode = str.join('', lines)
    try:
        with open(__file__, 'w') as f:
            f.write(newcode)
    except:
        print(newcode)
    
