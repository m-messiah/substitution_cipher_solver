#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import string

# LANG = 0 -> EN, 1 -> RUS
LANG = 1

if LANG:
    abc = u'абвгдежзиклмнопрстуфхцчшщъыьэюя'
else:
    abc = "abcdefghijklmnopqrstuvwxyz"


key = list(abc)
random.shuffle(key)
key = ''.join(key)

if LANG:
    trantab = dict((ord(a), ord(b)) for a, b in zip(abc, key))
    text = (open('textR.txt').read()
                            .decode("string_escape")
                            .decode("utf-8")
                            .lower())
    print text.translate(trantab).encode('utf-8')

else:
    trantab = string.maketrans(abc, key)
    text = open('text.txt').read().lower()
    print text.translate(trantab)

