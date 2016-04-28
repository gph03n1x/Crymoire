#!/usr/bin/env python

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
        self.charTable = [ i for i in targets ]
        self.charTable.sort()
        """
        Dictionaries
        charNoise: noise level of every character
        targetChars: target char of each char
        originChars: origin char of each char
        """
        self.charNoise = dict.fromkeys((c for c in self.charTable), 0)
        self.targetChars = dict.fromkeys((c for c in self.charTable), None)
        self.originChars = dict.fromkeys((c for c in self.charTable), None)
        """
        remaining_key: part of the key that wasn't used for creating
        the character chain
        """
        self.remaining_key = ""

        
    def raw_chain(self):
        """
        returns the dictionaries of the of the targetChars and
        the noise of each char
        """
        return str(self.targetChars) + "\n" + str(self.charNoise)
    
    
    def dictate_noise(self, level, position):
        """
        Choose how many characters are going to get
        inserted after a certain character
        """
        if level <= NOISELEVELS.LOW:
            self.charNoise[position] = NOISELEVELS.LOW_NOISE
        elif level <= NOISELEVELS.MEDIUM:
            self.charNoise[position] = NOISELEVELS.MEDIUM_NOISE
        elif level <= NOISELEVELS.HIGH:
            self.charNoise[position] = NOISELEVELS.HIGH_NOISE
        else:
            self.charNoise[position] = NOISELEVELS.ULTRA_NOISE
    
    
    def decrypt(self, message):
        """
        decrypts the encrypted message
        skip: integer of the characters we are going to ignore
        """
        self.skip = 0
        return "".join(map(self.decryptChar, [i for i in message]))


    def decryptChar(self, char):
        """
        Decrypts each character . If skip is positive
        then ignores the character.
        """
        if self.skip > 0:
            self.skip -= 1
            return ""
        else:
            result = self.originChars[char]
            self.skip = self.charNoise[result]
            return result


    def encrypt(self, message):
        """
        creates the encrypted string of the message
        length: the true length of the encrypted output
        results: a list of the directly encrypted characters
        """
        self.length = 0
        self.results = []
        map(self.encryptChar, [i for i in message])
        return self.noise_insertion()
    
    
    def encryptChar(self, char):
        """
        Adds to the results list the directly encrypted character
        and increases the length by 1 and the noise that the char
        generates .
        """
        self.results.append(self.targetChars[char])
        self.length += 1+self.charNoise[char]
    
    def noise_insertion(self):
        """
        Adds the noise characters after each character in a way
        that every character will have a nearly equal chance of
        appearing in the final encrypted string
        """
        noise = statisticalentropy.occurance_fixed(self.results, self.length)
        max_value = f_div(1, len(noise.keys()))
        
        """Inserts noise based on the current character occurance"""
        res = ""
        for i in self.results:
            res += i
            for j in range(self.charNoise[self.originChars[i]]):
                """
                Adds a random character in the spaces between the legit character
                if a characters occurance is bigger than the max value then we are no longer
                going to add him . If every character's occurance is near the ma value then
                we are going to choose randomly
                """
                if len(noise.keys()) > 0:
                    max_key = random.choice(noise.keys())
                    while noise[max_key] >= max_value:
                        del noise[max_key]
                        if len(noise.keys()) == 0:
                            res += random.choice(self.results)
                            break
                        max_key = random.choice(noise.keys())
                        
                    else:
                        res += max_key
                        noise[max_key] += f_div(1,self.length)
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
        self.analyze()
        
    def analyze(self):
        """Analyse the key and create the targetChars, originChars and charNoise"""
        
        """Calculate the key entropy """
        self.swap_chars = round(statisticalentropy.sentence_entropy(self.key))
        """Swap some characters in the charTable"""
        for char in range(0, int(self.swap_chars), 2):
            self.charTable = swap_list_positions(
                self.charTable, ord(self.key[char]) % 10, ord(self.key[char+1]) % 10
                                                 )
        """Create the target and origin character dictionaries"""                                         
        for char in range(int(self.swap_chars), len(self.key), 2):
            if char+1 >= len(self.key):
                break
            if self.targetChars[self.charTable[charmod100(self.key[char])]] is None and self.originChars[self.charTable[charmod100(self.key[char+1])]] is None:
                self.targetChars[self.charTable[charmod100(self.key[char])]] = self.charTable[charmod100(self.key[char+1])]
                self.originChars[self.charTable[charmod100(self.key[char+1])]] = self.charTable[charmod100(self.key[char])]

            else:
                self.remaining_key += self.key[char]+self.key[char+1]
        
        for char in self.targetChars:
            if self.targetChars[char] is not None:
                continue

            for tar in self.originChars:
                if not self.originChars[tar] is not None:
                    self.targetChars[char] = tar
                    self.originChars[tar] = char
                    break
                
        """Calculate the noise for each character"""
        for part in range(0, len(self.remaining_key), 2):
            chances = statisticalentropy.get_chance(self.remaining_key[part]) + statisticalentropy.get_chance(self.remaining_key[part+1])
            if chances > 0.0:
                if part/2+part%2 > len(self.charTable)-1:
                    break
                self.dictate_noise(chances, self.charTable[part/2+part%2])


if __name__ == '__main__':
    import tests