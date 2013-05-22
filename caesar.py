#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Messiah'
from sys import argv
import string


class Caesar:
    def __init__(self, lang):
        ABC = ["abcdefghijklmnopqrstuvwxyz",
               u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
               ]

        self.LANG = lang
        self.abc = ABC[self.LANG]

    def rot(self, text=None):
        if not text:
            print("Text is not presented")
            return
        text = text.lower()
        for i in range(len(self.abc)):
            key = self.abc[i:] + self.abc[:i]
            if self.LANG:
                trans = dict((ord(a), ord(b)) for a, b in zip(self.abc, key))
            else:
                trans = string.maketrans(self.abc, key)

            yield text.translate(trans)


def main():
    # LANG = 0 -> EN, 1 -> RUS
    LANG = 0
    if len(argv) > 1:
        LANG = int(argv[1])

    if LANG == 0:
        text = open('text.txt').read().lower()
    elif LANG == 1:
        text = (open('textR.txt').read()
                                 .decode("string_escape")
                                 .decode("utf-8")
                                 .lower())

    C = Caesar(LANG)
    for rot in C.rot(text):
        print rot.strip()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error: {}".format(e))