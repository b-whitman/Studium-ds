import unittest
import requests
from retrieve_definition import retrieve_definition, text_wrangle


class TestWikiAPI(unittest.TestCase):

    def test_retrieve_definition(self):
        self.extract = retrieve_definition("cat")
        self.maxDiff = None
        self.assertEqual(len(self.extract), 304)
        
    def test_text_wrangle(self):
        self.term = text_wrangle("DOG")
        self.assertEqual(self.term, "dog")

        self.term = text_wrangle("the Dog")
        self.assertEqual(self.term, "dog")

        self.term = text_wrangle("The Dog")
        self.assertEqual(self.term, "dog")

        self.term = text_wrangle("a dog")
        self.assertEqual(self.term, "dog")

        self.term = text_wrangle("Dogs")
        self.assertEqual(self.term, "dog")

if __name__ == '__main__':
    unittest.main()
