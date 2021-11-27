#!/usr/bin/env python3
# transform tests:
# use these as a reference for implementing pw

import pw.transform as pt

def assertEqual(expected, actual):
    if expected != actual:
        raise AssertionError("assertion failed: %s == %s" % (repr(expected), repr(actual)))

def to_int_test():
    assertEqual(0, pt.to_int(""))
    assertEqual(6513249, pt.to_int("abc"))
    assertEqual(3291835376408573590478209986637364656599265025014012802863049622424083630783948306431999498413285667939592978357630573418285899181951386474024455144309711, pt.to_int(pt.sha512("")))

def seed_test():
    assertEqual(0, pt.seed(0, 0, 0))
    assertEqual(1, pt.seed(0, 0, 1))
    assertEqual(1, pt.seed(0, 0, 2))
    assertEqual(3, pt.seed(0, 0, 3))
    assertEqual(3, pt.seed(0, 0, 4))
    assertEqual(50494, pt.seed(0, 0, 65535))
    assertEqual(17611, pt.seed(1, 0, 65535))
    assertEqual(7412,  pt.seed(2, 0, 65535))
    assertEqual(31190, pt.seed(3, 0, 65535))
    assertEqual(30939, pt.seed(4, 0, 65535))
    assertEqual(59569, pt.seed("", 0, 65535))
    assertEqual(60319, pt.seed("abc", 0, 65535))
    assertEqual(46370, pt.seed("hello", 0, 65535))
    assertEqual(53137, pt.seed("hello world", 0, 65535))

def append_test():
    assertEqual("", pt.append("", ""))
    assertEqual("a", pt.append("a", ""))
    assertEqual("a", pt.append("", "a"))
    assertEqual("ab", pt.append("a", "b"))
    assertEqual("helloworld", pt.append("hello", "world"))

def prepend_test():
    assertEqual("", pt.prepend("", ""))
    assertEqual("a", pt.prepend("a", ""))
    assertEqual("a", pt.prepend("", "a"))
    assertEqual("ba", pt.prepend("a", "b"))
    assertEqual("worldhello", pt.prepend("hello", "world"))

def cut_test():
    assertEqual("", pt.cut("", 0, 0))
    assertEqual("", pt.cut("a", 0, 0))
    assertEqual("", pt.cut("hello world", 0, 0))
    assertEqual("hello", pt.cut("hello world", 0, 5))
    assertEqual("world", pt.cut("hello world", 6, 11))
    assertEqual("world", pt.cut("hello world", 6, 200))
    assertEqual("hello world", pt.cut("hello world", -200, 200))
    assertEqual("", pt.cut("hello world", 200, -200))

def replace_test():
    assertEqual("", pt.replace("", "", ""))
    assertEqual("", pt.replace("a", "a", ""))
    assertEqual("b", pt.replace("a", "a", "b"))
    assertEqual("hello", pt.replace("henno", "n", "l"))
    assertEqual("heabcabco worabcd", pt.replace("hello world", "l", "abc"))

def replace_at_test():
    # assertEqual("", pt.replace_at("", 0, ""))
    # assertEqual("", pt.replace_at("a", 0, ""))
    assertEqual("", pt.replace_at("", 0, "a"))
    assertEqual("b", pt.replace_at("a", 0, "b"))
    assertEqual("ab1", pt.replace_at("abc", 200, "1"))
    assertEqual("1bc", pt.replace_at("abc", -200, "1"))
    assertEqual("hello1world", pt.replace_at("hello world", 5, "1"))

def insert_test():
    assertEqual("", pt.insert("", 0, ""))
    assertEqual("a", pt.insert("", 0, "a"))
    assertEqual("a", pt.insert("a", 0, ""))
    assertEqual("ab", pt.insert("a", 1, "b"))
    assertEqual("ba", pt.insert("a", 0, "b"))
    assertEqual("ab", pt.insert("a", 200, "b"))
    assertEqual("ba", pt.insert("a", -200, "b"))
    assertEqual("hello", pt.insert("heo", 2, "ll"))
    assertEqual("hello world", pt.insert("helld", 3, "lo wor"))

def make_unambiguous_test():
    assertEqual("", pt.make_unambiguous(""))
    assertEqual("hewwf wfrwd", pt.make_unambiguous("hello world"))
    assertEqual("abcdefghcxknmncpqrssuvwxyz", pt.make_unambiguous("abcdefghijklmnopqrstuvwxyz"))
    assertEqual("5S4rnaxNWwnxssku8uzsagdEphkAghWUF4shwwaXKMsubyfAxg4ybUeuXVWS9HdNcEypmeXn8FeGwnD4wkrn9Dep", pt.make_unambiguous("5S4rnaTNWonxss1u8LzsaJdEph1AJhWUF4sh2waXKMsutyfAxg4ybUeuXVWS9HdNcEypmeXn8FZGonD4w1rj9DZp"))
    
def add_special_characters_test():
    assertEqual("", pt.add_some_simple_special_characters(""))
    assertEqual(":abc", pt.add_some_simple_special_characters("abc"))
    assertEqual("h:ello", pt.add_some_simple_special_characters("hello"))
    assertEqual("h#ello world", pt.add_some_simple_special_characters("hello world"))
    assertEqual("aspen spoon 567# scrap", pt.add_some_simple_special_characters("aspen spoon 567 scrap"))

def capitalize_some_test():
    assertEqual("", pt.capitalize_some(""))
    assertEqual("Abc", pt.capitalize_some("abc"))
    assertEqual("Hello", pt.capitalize_some("hello"))
    assertEqual("Hello World", pt.capitalize_some("hello world"))
    assertEqual("aspen Spoon 567 scrap", pt.capitalize_some("aspen spoon 567 scrap"))

def diceware_test():
    assertEqual("movie extra beat chap", pt.diceware("", 1, 4))
    assertEqual("solon cough vigil mew", pt.diceware("abc", 1, 4))
    assertEqual("spiro keel dow", pt.diceware("hello", 1, 4))
    assertEqual("aspen spoon 567 scrap", pt.diceware("hello world", 1, 4))
    assertEqual("ajax toss", pt.diceware("aspen spoon 567 scrap", 1, 4))

    assertEqual("movie extra beat chap", pt.diceware("", 4, 4))
    assertEqual("solon cough vigil mew", pt.diceware("abc", 4, 4))
    assertEqual("spiro keel dow curd", pt.diceware("hello", 4, 4))
    assertEqual("aspen spoon 567 scrap", pt.diceware("hello world", 4, 4))
    assertEqual("ajax toss gules filch", pt.diceware("aspen spoon 567 scrap", 4, 4))

def run_tests():
    to_int_test()
    seed_test()
    append_test()
    prepend_test()
    cut_test()
    replace_test()
    replace_at_test()
    insert_test()
    make_unambiguous_test()
    add_special_characters_test()
    capitalize_some_test()
    diceware_test()

    print("%s: all tests passed" % __file__)

if __name__ == "__main__":
    run_tests()
