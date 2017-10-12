#!/usr/bin/env python
import unittest
import string
import random
from crymoire import Crymoire
from core.statistical import StatisticalEntropy, occuranceGraph
from core.utils import generate_random_key


class TestCrymoire(unittest.TestCase):
    def setUp(self):
        self.se = occuranceGraph()
        self.crymoire = Crymoire()
        self.crymoire.setKey(generate_random_key(size=1024, chars=string.ascii_letters))
        #self.crymoire.loadKey("secret.key")
    

    def test_enc_and_dec(self):
        message = "secret message :)"#generate_random_key(250, chars=string.ascii_letters)
        enc_ = self.crymoire.encrypt(message)
        #self.se.create_occurance_figure(enc_)
        self.assertEqual(self.crymoire.decrypt(enc_), message)
        
    def test_random(self):
        number_of_tests = 10
        
        for test in range(number_of_tests):
            
            message = generate_random_key(size=250, chars=string.ascii_letters)
            enc_ = self.crymoire.encrypt(message)
            self.assertEqual(self.crymoire.decrypt(enc_), message)
    


suite = unittest.TestLoader().loadTestsFromTestCase(TestCrymoire)
unittest.TextTestRunner(verbosity=2).run(suite)