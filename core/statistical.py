#!/usr/bin/env python
import math
import string
import operator
import core.constants as CONST
from core.utils import f_div

try:
    from bokeh.plotting import figure, output_file, show, hplot, output_notebook
except ImportError:
    print "[-] You are missing the bokeh package . Plotting is not available"


class StatisticalEntropy(object):
    def __init__(self):
        """
        Class for creating letter and chance of occuring dictionaries
        """
        self._occurances = CONST.DEFAULT_OCCURANCES
        self.occurances = sorted(self._occurances.items(),
                       key=operator.itemgetter(1), reverse=True)
        
    def get_chance(self, char):
        """
        Get the chance of a character occuring in a normal sentence
        """
        if char.upper() in self._occurances:
            return self._occurances[char.upper()]
        return 0.0


    def sentence_entropy(self, sentence):
        """
        Calculate the entropy of a sentence based on the characters included
        using https://en.wikipedia.org/wiki/Entropy_%28information_theory%29
        """
        sm = self.statistical_monograms(sentence)
        entropy = 0
        for i in sm:
            entropy -= f_div(sm[i],100) * math.log(f_div(sm[i],100), 2)
        return entropy


    def occurance_fixed(self, sentence, length):
        """
        Create a dictionary of letters with their occurance based
        on the true length of an encrypted string
        """
        stats = {i:0.0 for i in sentence}
        for letter in sentence:
            stats[letter] += f_div(1,length)
        return stats


    @staticmethod
    def statistical_monograms(sentence, sort_r=False):
        """
        Creates a dictionary which uses percentage of every
        character in a sentence
        """
        stats = {i:0.0 for i in sentence}
        for letter in sentence:
            stats[letter] += f_div(1,len(sentence)) * 100
    
        if not sort_r:
            return stats
        return sorted(stats.items(), key=operator.itemgetter(1), reverse=True)

    
class occuranceGraph(object):
    def __init__(self):
        self.se = StatisticalEntropy()


    def use_notebook(self):
        output_notebook() 


    def use_file(self, filename="graphs.html"):
        output_file(filename)


    def create_occurance_figure(self, sentence, open_plots=False):
        self.stm = self.se.statistical_monograms(sentence, sort_r=True)
        self.sa = self.se.occurances
        
        keys = [m[0] for m in self.stm ]
        items = [m[1] for m in self.stm ]
        
        keys_a = [m[0] for m in self.sa ]
        items_a = [m[1] for m in self.sa ]
        
        p = figure(x_range=keys, title="Encrypted Sentence letter occurance")
        p.square(keys, items)
        
        s = figure(x_range=keys_a, title="Normal letter occurance")
        s.square(keys_a, items_a)
        v = hplot(p, s)
        if open_plots:
            show(v)
    

if __name__ == '__main__':
    se = occuranceGraph()
    se.create_occurance_figure("w-ln0Fk0=lyn{;{~~0lkN0A", open_plots=True)
    