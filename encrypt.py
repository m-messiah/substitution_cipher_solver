#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from sys import argv
import string

# ROT?
ROT = True
# LANG = 0 -> EN, 1 -> RUS
LANG = 1

if len(argv) > 1:
    LANG = int(argv[1])


def main():
    """
    If ROT is True - encode to random ROT.
    If ROT is False - encode to random shuffle.
    """
    if LANG:
        abc = u"абвгдежзиклмнопрстуфхцчшщъыьэюя"
    else:
        abc = "abcdefghijklmnopqrstuvwxyz"

    if ROT:
        rot = random.randint(0, len(abc))
        key = abc[rot:] + abc[:rot]
        print("ROT{}".format(rot))

    else:
        key = list(abc)
        random.shuffle(key)
        key = ''.join(key)
        print("Shuffle: {}".format(key.encode("utf-8")))

    if LANG:
        trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
        text = (open('textR.txt').read()
                                 .decode("string_escape")
                                 .decode("utf-8")
                                 .lower())

    else:
        trans = string.maketrans(abc, key)
        text = open('text.txt').read().lower()

    print(text.translate(trans))

if __name__ == "__main__":
    main()
