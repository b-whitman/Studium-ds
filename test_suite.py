import unittest
from retrieve_definition import text_wrangle, open_search, get_API_params, get_opensearch_params
from autogenerate_decks import batch_search, get_article_size, get_search_string, get_params_autogen, get_params_size



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

    def test_get_search_string(self):
        self.assertEqual(get_search_string(["Tree", "Bush", "Cherry", "Dog"]), 'Tree|Bush|Cherry|Dog')
        self.assertIs(type(get_search_string(["Tree", "Bush", "Cherry", "Dog"])), str)

    def test_get_params_autogen(self):
        self.assertIs(type(get_params_autogen('Dog')), dict)

    def test_get_params_size(self):
        self.assertIs(type(get_params_size('Dog')), dict)


class TestWikiAPI(unittest.TestCase):

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

    def test_get_API_params(self):
        self.assertEqual(get_API_params('Cat'), {'action': 'query', 'prop': 'extracts', 'exchars': '300',
                                                 'titles': 'Cat', 'format': 'json', 'explaintext': 1, 'exlimit': 1})
        self.assertIs(type(get_API_params('Cat')), dict)

    def test_get_opensearch_params(self):
        self.assertEqual(get_opensearch_params('Cat'), {'action': 'opensearch', 'search': 'Cat', 'redirects': 'resolve',
                                                        'format': 'json'})
        self.assertIs(type(get_opensearch_params('Cat')), dict)


if __name__ == '__main__':
    unittest.main()
