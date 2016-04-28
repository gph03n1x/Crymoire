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
        
        self.charTable = [ i for i in targets ]
        self.charTable.sort()
        
        self.charNoise = dict.fromkeys((c for c in self.charTable), 0)
        self.targetChars = dict.fromkeys((c for c in self.charTable), None)
        self.originChars = dict.fromkeys((c for c in self.charTable), None)
        
        self.remaining_key = ""
        
        self.skip = 0
        self.results = []
        
        
        
    def raw_chain(self):
        return str(self.targetChars) + "\n" + str(self.charNoise)
    
    def dictate_noise(self, level, position):
        if level <= NOISELEVELS.LOW:
            self.charNoise[position] = NOISELEVELS.LOW_NOISE
        elif level <= NOISELEVELS.MEDIUM:
            self.charNoise[position] = NOISELEVELS.MEDIUM_NOISE
        elif level <= NOISELEVELS.HIGH:
            self.charNoise[position] = NOISELEVELS.HIGH_NOISE
        else:
            self.charNoise[position] = NOISELEVELS.DEFAULT_NOISE
        
    def encrypt(self, message):
        self.length = 0
        map(self.encryptChar, [i for i in message])
        return self.noise_insertion()
        
    
    def decrypt(self, message):
        return "".join(map(self.decryptChar, [i for i in message]))

    def encryptChar(self, char):
        result = self.targetChars[char]
        
        self.results.append(result)
        self.length += 1+self.charNoise[char]
    
    def noise_insertion(self):
        noise = statisticalentropy.occurance_fixed(self.results, self.length)
        max_value = f_div(1, len(noise.keys()))

        res = ""
        for i in self.results:
            res += i
            for j in range(self.charNoise[self.originChars[i]]):
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

    def decryptChar(self, char):
        if self.skip > 0:
            self.skip -= 1
            return ""
        else:
            result = self.originChars[char]
            self.skip = self.charNoise[result]
            return result

    def setKey(self, key):
        self.key = key
        self.analyze()
        
    def analyze(self):
        # Rest Digits in form (firstChar,lastChar,jump)
        self.swap_chars = round(statisticalentropy.sentence_entropy(self.key))
        
        for char in range(0, int(self.swap_chars), 2):
            self.charTable = swap_list_positions(
                self.charTable, ord(self.key[char]) % 10, ord(self.key[char+1]) % 10
                                                 )
                                                 
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
                
        
        for part in range(0, len(self.remaining_key), 2):
            chances = statisticalentropy.get_chance(self.remaining_key[part]) + statisticalentropy.get_chance(self.remaining_key[part+1])
            if chances > 0.0:
                if part/2+part%2 > len(self.charTable)-1:
                    break
                self.dictate_noise(chances, self.charTable[part/2+part%2])


if __name__ == '__main__':
    import tests