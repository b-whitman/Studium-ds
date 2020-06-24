import unittest
import requests
from retrieve_definition import retrieve_definition


class TestWikiAPI(unittest.TestCase):

    def test_retrieve_definition(self):
        self.extract = retrieve_definition("cat")
        self.maxDiff = None
        self.assertEqual(self.extract, "The cat (Felis catus) is a domestic species of small carnivorous mammal. It is the only domesticated species in the family Felidae and is often referred to as the domestic cat to distinguish it from the wild members of the family. A cat can either be a house cat, a farm cat or a feral cat; the latter...")

def test_text_wrangle(self):
        self.term = text_wrangle("DOG")
        self.assertEqual(self.term, "dog")

        self.term = text_wrangle("the Dog")
        self.assertEqual(self.term, "dog")

        self.term = text_wrangle("a dog")
        self.assertEqual(self.term, "dog")

        self.term = text_wrangle("Dogs")
        self.assertEqual(self.term, "dog")


if __name__ == '__main__':
    unittest.main()
