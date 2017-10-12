#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import time
import random
import string
import hashlib

from core.statistical import StatisticalEntropy
from core.constants import NOISELEVELS
from core.utils import *

statisticalentropy = StatisticalEntropy()


class Crymoire():
    def __init__(self, targets=string.printable):
        """
        Creates all the attributes
        charTable: a sorted list with every character
        """
        self.char_table = [i for i in targets]
        self.char_table.sort()
        self.table_length = len(self.char_table)
        """
        charNoise: noise level of every character
        """
        self.char_noise = dict.fromkeys((c for c in self.char_table), 0)


    def jump(self, character, key):
        key_index = self.char_table.index(key)
        char_index = self.char_table.index(character)
        mod = ( char_index + key_index ) % self.table_length
        return self.char_table[mod]

    def r_jump(self, character, key):
        key_index = self.char_table.index(key)
        char_index = self.char_table.index(character)
        mod = (char_index - key_index)
        if mod < 0:
            mod = self.table_length + mod
        return self.char_table[mod]

    def raw_chain(self):
        """
        returns the dictionaries of the of the targetChars and
        the noise of each char
        """
        return str(self.targetChars) + "\n" + str(self.char_noise)


    def dictate_noise(self, level, position):
        """
        Choose how many characters are going to get
        inserted after a certain character
        """
        if level <= NOISELEVELS.LOW:
            self.char_noise[position] = NOISELEVELS.LOW_NOISE
        elif level <= NOISELEVELS.MEDIUM:
            self.char_noise[position] = NOISELEVELS.MEDIUM_NOISE
        elif level <= NOISELEVELS.HIGH:
            self.char_noise[position] = NOISELEVELS.HIGH_NOISE
        else:
            self.char_noise[position] = NOISELEVELS.ULTRA_NOISE


    def decrypt(self, message):
        """
        decrypts the encrypted message
        skip: integer of the characters we are going to ignore
        """
        self.skip = 0
        self.length = 0
        return "".join(list(map(self.decryptChar, [i for i in message])))


    def decryptChar(self, char):
        """
        Decrypts each character . If skip is positive
        then ignores the character.
        """
        if self.skip > 0:
            self.skip -= 1
            return ""
        else:
            result = self.r_jump(char, self.key[self.length % self.key_length])
            self.skip = self.char_noise[result]
            self.length += self.skip + 1
            return result


    def encrypt(self, message):
        """
        creates the encrypted string of the message
        length: the true length of the encrypted output
        results: a list of the directly encrypted characters
        """
        self.length = 0
        self.results = []
        for i in message:
            self.encryptChar(i)

        return self.noise_insertion(message)


    def encryptChar(self, char):
        """
        Adds to the results list the directly encrypted character
        and increases the length by 1 and the noise that the char
        generates .
        """
        self.results.append(self.jump(char, self.key[self.length % self.key_length]))
        self.length += 1+self.char_noise[char]

    def noise_insertion(self, message):
        """
        Adds the noise characters after each character in a way
        that every character will have a nearly equal chance of
        appearing in the final encrypted string
        """
        noise = statisticalentropy.occurance_fixed(self.results, self.length)
        max_value = 1/ len(list(noise.keys()))

        """Inserts noise based on the current character occurance"""
        res = ""
        for p, i in enumerate(self.results):
            res += i
            for j in range(self.char_noise[message[p]]):
                """
                Adds a random character in the spaces between the legit character
                if a characters occurance is bigger than the max value then we are no longer
                going to add him . If every character's occurance is near the ma value then
                we are going to choose randomly
                """
                if len(noise.keys()) > 0:
                    max_key = random.choice(list(noise.keys()))
                    while noise[max_key] >= max_value:
                        del noise[max_key]
                        if len(noise.keys()) == 0:
                            res += random.choice(self.results)
                            break
                        max_key = random.choice(list(noise.keys()))

                    else:
                        res += max_key
                        noise[max_key] += 1/self.length
                else:
                    res += random.choice(self.results)
        return res

    def loadKey(self, filename="private.key"):
        """
        Loads the key from the specified file
        """
        fObj = open(filename, "r")
        self.setKey(fObj.read())
        fObj.close()

    def setKey(self, key):
        """
        Sets the key and analyzes it
        """
        self.key = key
        self.key_length = len(key)
        self.analyze()

    def analyze(self):
        """Analyse the key and create the charNoise"""

        """Calculate the key entropy """
        self.swap_chars = round(statisticalentropy.sentence_entropy(self.key))
        """Swap some characters in the charTable"""
        for char in range(0, int(self.swap_chars), 2):
            self.char_table = swap_list_positions(
                self.char_table, ord(self.key[char]) % 10, ord(self.key[char + 1]) % 10
                                                 )

        """Calculate the noise for each character"""
        for part in range(0, len(self.key), 2):
            chances = statisticalentropy.get_chance(self.key[part]) + statisticalentropy.get_chance(self.key[part+1])
            if chances > 0.0:
                if part//2+part%2 > len(self.char_table)-1:
                    break
                self.dictate_noise(chances, self.char_table[part // 2 + part % 2])


if __name__ == '__main__':
    import tests
