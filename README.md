# pw-py - password generator

Password generator inspired by [ss64](https://ss64.com/pass/).

This command-line tool deterministically generates passwords.
You can provide a domain, a user and a key and the tool will always give the same password for the same domain, user and key combination.

## Usage

- Basic Usage

```
$ pw-py <domain> <user>
Encryption key: <key>
(password is now copied to clipboard for 5 seconds)
```

- Example

```
$ pw-py github.com aesncast
Encryption key: mykey
("Slide# Paso Hoop D#izzy alcoa" is now copied to clipboard for 5 seconds)
```

The clipboard is cleared after 5 seconds.

Domains and users are recorded in `<pw-py local data directory>/pwfile4` and can be listed (for e.g. shell completion) with `pw-py -l [domain]` (leave domain empty to list domains).

## Special Dependencies
Some systems might need non-Python libraries or executables for pw-py to work correctly.

### Linux

`xsel` might be needed for copy/paste to work.

## Building

Skip this step if only an installation is needed.
Python3 `pyinstaller` is required to build a standalone executable.
Execute the following command to build a standalone executable in `dist/`:

    $ make

## Installing

Python `setuptools` are required to properly resolve dependencies and install pw-py.
Execute the following command to install pw-py libraries and console script (`sudo` may be required):

    $ python3 ./setup.py install
    
