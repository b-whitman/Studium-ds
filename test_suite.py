import unittest
from retrieve_definition import retrieve_definition, text_wrangle, open_search
from autogenerate_decks import autogenerate, batch_search, get_article_size


class TestAutogeneration(unittest.TestCase):

    def test_batch_search(self):
        self.assertEqual(batch_search(["Photosynthesis"]), [['Photosynthesis']])
        test_list = []
        for _ in range(0, 49):
            test_list.append("Photosynthesis")
        for _ in range(0, 10):
            test_list.append("Ecology")
        self.assertIn(['Ecology'], batch_search(test_list))

    def test_get_article_size(self):
        self.assertNotIn('Hans Stubb', get_article_size("Photosynthesis|Geology|Hans Stubb"))

    def test_autogenerate(self):
        self.assertIs(type(autogenerate("Trail_Blazer_(train)")), dict)


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

    def test_open_search(self):
        self.assertEqual(open_search('fdsadsfasd'), "We can't find anything close to that :(")
        self.assertIs(type(open_search('Dog')), str)


if __name__ == '__main__':
    unittest.main()
