#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import string
from sys import argv

# LANG = 0 -> EN, 1 -> RUS
LANG = 1
if len(argv) > 1:
    LANG = int(argv[1])

if LANG:
    abc = u'абвгдежзиклмнопрстуфхцчшщъыьэюя'
else:
    abc = "abcdefghijklmnopqrstuvwxyz"


key = list(abc)
random.shuffle(key)
key = ''.join(key)

if LANG:
    trans = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    text = (open('textR.txt').read()
                             .decode("string_escape")
                             .decode("utf-8")
                             .lower())

else:
    trans = string.maketrans(abc, key)
    text = open('text.txt').read().lower()

print text.translate(trans)

