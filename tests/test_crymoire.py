#!/usr/bin/env python
import unittest
import string
from crymoire import Crymoire
from core.statistical import StatisticalEntropy, occuranceGraph
from core.utils import generate_random_key

class TestCrymoire(unittest.TestCase):

    def setUp(self):
        self.se = occuranceGraph()
        self.crythem = Crymoire()
        """
        f = open("private.key", "r")
        
        self.crythem.setKey(f.read())
        f.close()"""
        self.crythem.setKey(generate_random_key(250, chars=string.ascii_letters))
    
    def test_enc_and_dec(self):
        message = "secret message :)"#generate_random_key(250, chars=string.ascii_letters)
        enc_ = self.crythem.encrypt(message)
        #self.se.create_occurance_figure(enc_)
        self.assertEqual(self.crythem.decrypt(enc_), message)
        print message
        print "\n"
        print "#", enc_, "#"
        print self.crythem.raw_chain()



suite = unittest.TestLoader().loadTestsFromTestCase(TestCrymoire)
unittest.TextTestRunner(verbosity=2).run(suite)