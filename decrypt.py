#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import re
from itertools import combinations
from sys import argv

# LANG = 0 -> EN, 1 -> RUS
LANG = 1
if len(argv) > 1:
    LANG = int(argv[1])

try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

MAX_GOODNESS_LEVEL = 2  # 1-7
MAX_BAD_WORDS_RATE = 0.06

if LANG:
    ABC = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
else:
    ABC = "abcdefghijklmnopqrstuvwxyz"


class WordList:
    MAX_WORD_LENGTH_TO_CACHE = 8

    def __init__(self):
        # words struct is
        # {(length,different_chars)}=[words] if len > MAX_WORD_LENGTH_TO_CACHE
        # {(length,different_chars)}=set([words and templates]) else

        self.words = {}
        for goodness in range(MAX_GOODNESS_LEVEL):
            print u"Loaded {}{}.txt dictionary".format("r" if LANG else "",
                                                       goodness)
            if LANG:
                goodness = "r{}".format(goodness)
            try:
                for word in open("words/" + str(goodness) + ".txt"):
                    word = word.strip()
                    if LANG:
                        word = word.decode("utf-8")
                    word_len = len(word)
                    properties = (word_len, len(set(word)))
                    if word_len > WordList.MAX_WORD_LENGTH_TO_CACHE:
                        words = self.words.get(properties, [])
                        words.append(word)
                        self.words[properties] = words
                    else:
                        # add all possible combinations of the word and dots
                        words = self.words.get(properties, set([]))
                        for i in range(word_len + 1):
                            for dots_positions in combinations(range(word_len),
                                                               i):
                                adding_word = list(word)
                                for j in dots_positions:
                                    adding_word[j] = '.'

                                words.add(''.join(adding_word))
                        self.words[properties] = words
            except IOError:
                continue

    def find_word_by_template(self, template, different_chars):
        """ Finds the word in the dict by template. Template can contain
        alpha characters and dots only """

        properties = (len(template), different_chars)
        if properties not in self.words:
            return False

        words = self.words[properties]

        if properties[0] > WordList.MAX_WORD_LENGTH_TO_CACHE:
            if LANG:
                template = re.compile(template, re.UNICODE)
            else:
                template = re.compile(template)

            for word in words:
                if LANG:
                    if template.match(word, re.UNICODE):
                        return True
                else:
                    if template.match(word):
                        return True
        else:
            if template in words:
                return True
        return False


class KeyFinder:
    def __init__(self, enc_words):
        self.points_threshhold = int(len(enc_words) * MAX_BAD_WORDS_RATE)
        self.dict_wordlist = WordList()
        self.enc_words = enc_words
        self.different_chars = {}
        self.found_keys = {}  # key => bad words
        for enc_word in enc_words:
            self.different_chars[enc_word] = len(set(enc_word))

    def get_key_points(self, key):
        """ The key is alpha string with dots on unknown places """
        if LANG:
            trans = dict((ord(a), ord(b)) for a, b in zip(ABC, key))
        else:
            trans = maketrans(ABC, key)
        points = 0

        for enc_word in self.enc_words:
            different_chars = self.different_chars[enc_word]
            translated_word = enc_word.translate(trans)
            if not self.dict_wordlist.find_word_by_template(translated_word,
                                                            different_chars):
                points += 1
        return points

    def recursive_calc_key(self, key, possible_letters, level):
        """ Tries to place a possible letters on places with dots """
        print(u"Level: {:3}, key: {}".format(level, key))

        if '.' not in key:
            points = self.get_key_points(key)
            print(u"Found: {}, bad words: {}".format(key, points))
            self.found_keys[key] = points
            return

        nextpos = -1  # a pos with a minimum length of possible letters
        minlen = len(ABC) + 1

        for pos in range(len(ABC)):
            if key[pos] == ".":
                for letter in list(possible_letters[pos]):
                    new_key = key[:pos] + letter + key[pos + 1:]

                    if self.get_key_points(new_key) > self.points_threshhold:
                        possible_letters[pos].remove(letter)
                        if not possible_letters[pos]:
                            return

                if len(possible_letters[pos]) < minlen:
                    minlen = len(possible_letters[pos])
                    nextpos = pos

        while possible_letters[nextpos]:
            letter = possible_letters[nextpos].pop()
            new_possible_letters = copy.deepcopy(possible_letters)
            for pos in range(len(ABC)):
                new_possible_letters[pos] -= set([letter])
            new_possible_letters[nextpos] = set([letter])
            new_key = key[:nextpos] + letter + key[nextpos + 1:]
            self.recursive_calc_key(new_key, new_possible_letters, level + 1)

    def find(self):
        if not self.found_keys:
            # Caesar firstly.
            for i in range(len(ABC)):
                key = ABC[i:] + ABC[:i]
                self.found_keys[key] = self.get_key_points(key)

            possible_letters = [set(ABC) for _ in range(len(ABC))]
            self.recursive_calc_key("." * len(ABC), possible_letters, 1)
        return self.found_keys


def main():
    print(u"Selected {} language".format("RUS" if LANG else "EN"))
    if LANG:
        enc_text = (open("encryptedR.txt").read()
                    .decode("string_escape")
                    .decode("utf-8")
                    .lower())
        enc_words = re.findall(ur"[а-я']+", enc_text, re.UNICODE)

    else:
        enc_text = open("encrypted.txt").read().lower()
        enc_words = re.findall(r"[a-z']+", enc_text)

    # skip the words with apostrophes
    enc_words = [word for word in enc_words
                 if "'" not in word and
                    len(word) <= WordList.MAX_WORD_LENGTH_TO_CACHE
                 ]
    enc_words = enc_words[:500]

    print(u"Loaded {} words in encrypted{}.txt, loading dicts"
          .format(len(enc_words), "R" if LANG else ""))

    keys = KeyFinder(enc_words).find()
    if not keys:
        print(u"Key not founded, try to increase MAX_BAD_WORDS_RATE")
    for key, bad_words in keys.items():
        print(u"Possible key: {}, bad words:{}".format(key, bad_words))
    best_key = min(keys, key=keys.get)
    print(u"{0}\nBest key: {1}, bad_words {2}\n{0}".format("-" * 10,
                                                           best_key,
                                                           keys[best_key]))
    if LANG:
        trans = dict((ord(a), ord(b)) for a, b in zip(ABC, best_key))
        decrypted = (open("encryptedR.txt").read()
                     .decode("string_escape")
                     .decode("utf-8")
                     .translate(trans)
                     .encode("utf-8"))
    else:
        trans = maketrans(ABC, best_key)
        decrypted = open("encrypted.txt").read().translate(trans)

    with open("decrypted.txt", "w") as decryptedFile:
        decryptedFile.write(decrypted)

    print(u"Text:\n\n")
    print(decrypted)


if __name__ == "__main__":
    try:
        #import cProfile
        #cProfile.run('main()')
        main()
    except Exception as E:
        print("Error: %s" % E)
