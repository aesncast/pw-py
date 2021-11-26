#!/usr/bin/env python3
# transform tests:
# use these as a reference for implementing pw

import pw.transform as pt

def assertEqual(expected, actual):
    if expected != actual:
        raise AssertionError("assertion failed: %s == %s" % (repr(expected), repr(actual)))

def to_int_test():
    assertEqual(0, pt.to_int(""));
    assertEqual(6513249, pt.to_int("abc"));
    assertEqual(3291835376408573590478209986637364656599265025014012802863049622424083630783948306431999498413285667939592978357630573418285899181951386474024455144309711, pt.to_int(pt.sha512("")))

def make_unambiguous_test():
    assertEqual("", pt.make_unambiguous(""));
    assertEqual("hewwf wfrwd", pt.make_unambiguous("hello world"));
    assertEqual("abcdefghcxknmncpqrssuvwxyz", pt.make_unambiguous("abcdefghijklmnopqrstuvwxyz"));
    assertEqual("5S4rnaxNWwnxssku8uzsagdEphkAghWUF4shwwaXKMsubyfAxg4ybUeuXVWS9HdNcEypmeXn8FeGwnD4wkrn9Dep", pt.make_unambiguous("5S4rnaTNWonxss1u8LzsaJdEph1AJhWUF4sh2waXKMsutyfAxg4ybUeuXVWS9HdNcEypmeXn8FZGonD4w1rj9DZp"));
    
def add_special_characters_test():
    assertEqual("", pt.add_some_simple_special_characters(""));
    assertEqual(":abc", pt.add_some_simple_special_characters("abc"));
    assertEqual("h:ello", pt.add_some_simple_special_characters("hello"));
    assertEqual("h#ello world", pt.add_some_simple_special_characters("hello world"));
    assertEqual("aspen spoon 567# scrap", pt.add_some_simple_special_characters("aspen spoon 567 scrap"));

def capitalize_some_test():
    assertEqual("", pt.capitalize_some(""));
    assertEqual("Abc", pt.capitalize_some("abc"));
    assertEqual("Hello", pt.capitalize_some("hello"));
    assertEqual("Hello World", pt.capitalize_some("hello world"));
    assertEqual("aspen Spoon 567 scrap", pt.capitalize_some("aspen spoon 567 scrap"));

def diceware_test():
    assertEqual("movie extra beat chap", pt.diceware("", 1, 4));
    assertEqual("solon cough vigil mew", pt.diceware("abc", 1, 4));
    assertEqual("spiro keel dow", pt.diceware("hello", 1, 4));
    assertEqual("aspen spoon 567 scrap", pt.diceware("hello world", 1, 4));
    assertEqual("ajax toss", pt.diceware("aspen spoon 567 scrap", 1, 4));

    assertEqual("movie extra beat chap", pt.diceware("", 4, 4));
    assertEqual("solon cough vigil mew", pt.diceware("abc", 4, 4));
    assertEqual("spiro keel dow curd", pt.diceware("hello", 4, 4));
    assertEqual("aspen spoon 567 scrap", pt.diceware("hello world", 4, 4));
    assertEqual("ajax toss gules filch", pt.diceware("aspen spoon 567 scrap", 4, 4));

def run_tests():
    to_int_test()
    make_unambiguous_test()
    add_special_characters_test()
    capitalize_some_test()
    diceware_test()

    print("%s: all tests passed" % __file__)

if __name__ == "__main__":
    run_tests()
