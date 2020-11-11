import unittest
import sys
sys.path.append('../')

from ponyCode import *

class ponyCodeTestCase(unittest.TestCase):

    def test_round_to_2(self):
        value=round_to_2(0.12345)
        self.assertEquals(value, 0.12)

    def test_round_to_2_(self):
        value=round_to_2(1)
        self.assertEquals(value,1.0)

    def test_verbosity_Upper(self):
        value=find_verbosity('Pinkie Pie')
        self.assertEquals(value, 3)

    def test_verbosity_lower(self):
        value=find_verbosity('pinkie pie')
        self.assertEquals(value,3)

    def test_verbosity_other(self):
        value=find_verbosity('Others')
        self.assertEquals(value,-1)

    def test_mentions_one(self):
        value=find_mentions("Hi my name is Pinkie and I like Applejack")
        self.assertEquals(value,[1,3])

    def test_mentions_lower(self):
        value=find_mentions("I like eating apple")
        self.assertEquals(value,[])

    def test_mentions_multiple(self):
        value=find_mentions("Sparle, I like Twilight Sparkle")
        self.assertEquals(value,[0])

    def test_non_dict_none(self):
        value=none_dic_words("I like apple")
        self.assertEquals(value,[])

    def test_none_dict(self):
        value=none_dic_words("I've been there")
        self.assertEquals(value,["ve"])


    