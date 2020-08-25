import unittest
from retrieve_definition import text_wrangle, open_search, get_API_params, get_opensearch_params, retrieve_definition
from autogenerate_decks import batch_search, get_article_size, get_search_string, get_params_autogen, get_params_size
from leitner import leitner_dates
from comparative_metrics import get_session_length, get_cards_per_min, convert_to_datetime, best_session_length, \
    daily_cards_min_comparison, weekly_per_min_comparison, monthly_per_min_comparison, best_session_daily, \
    best_session_monthly, best_session_weekly, make_results_dict
import pandas as pd
import numpy as np


class TestComparativeMetrics(unittest.TestCase):
    def setUp(self):
        self.test_df_1 = pd.DataFrame(data=[[1, 40, 1583015220000, 1583015820000]],
                                      columns=['id', 'total_looked_at', 'session_start', 'session_end'])
        self.test_df_2 = convert_to_datetime(self.test_df_1)

    def test_convert_to_datetime(self):
        self.assertEqual(len(self.test_df_1), len(convert_to_datetime(self.test_df_1)))
        self.assertEqual(len(self.test_df_2), len(convert_to_datetime(self.test_df_1)))
        pd.testing.assert_frame_equal(self.test_df_2, convert_to_datetime(self.test_df_1))

    def test_get_session_length(self):
        self.assertIs(type(get_session_length(self.test_df_2.iloc[0])), float)
        self.assertEqual(get_session_length(self.test_df_2.iloc[0]), 600.0)

    def test_get_cards_per_min(self):
        self.assertIs(type(get_cards_per_min(self.test_df_2.iloc[0])), np.float64)
        self.assertEqual(get_cards_per_min(self.test_df_2.iloc[0]), 4.0)

    def test_best_session_length(self):
        self.assertIs(type(best_session_length(self.test_df_2)), np.float64)
        self.assertEqual(best_session_length(self.test_df_2), 10.0)

    def test_daily_cards_min_comparison(self):
        self.assertEqual(len(daily_cards_min_comparison(self.test_df_2)), 4)
        self.assertEqual(daily_cards_min_comparison(self.test_df_2)['daily_cards_min'], 0)
        self.assertEqual(daily_cards_min_comparison(self.test_df_2)['difference'], 100)
        self.assertEqual(daily_cards_min_comparison(self.test_df_2)['color_code'], '000000')
        self.assertEqual(daily_cards_min_comparison(self.test_df_2)['unicode'], u'\u003D')

    def test_weekly_per_min_comparison(self):
        self.assertEqual(len(weekly_per_min_comparison(self.test_df_2)), 4)
        self.assertEqual(weekly_per_min_comparison(self.test_df_2)['weekly_cards_min'], 0)
        self.assertEqual(weekly_per_min_comparison(self.test_df_2)['difference'], 100)
        self.assertEqual(weekly_per_min_comparison(self.test_df_2)['color_code'], '000000')
        self.assertEqual(weekly_per_min_comparison(self.test_df_2)['unicode'], u'\u003D')

    def test_monthly_per_min_comparison(self):
        self.assertEqual(len(monthly_per_min_comparison(self.test_df_2)), 4)
        self.assertEqual(monthly_per_min_comparison(self.test_df_2)['monthly_cards_min'], 0)
        self.assertEqual(monthly_per_min_comparison(self.test_df_2)['difference'], 100)
        self.assertEqual(monthly_per_min_comparison(self.test_df_2)['color_code'], '000000')
        self.assertEqual(monthly_per_min_comparison(self.test_df_2)['unicode'], u'\u003D')

    def test_best_session_daily(self):
        self.assertEqual(len(best_session_daily(self.test_df_2)), 4)
        self.assertEqual(best_session_daily(self.test_df_2)['best_session_daily'], 0)
        self.assertEqual(best_session_daily(self.test_df_2)['difference'], 100)
        self.assertEqual(best_session_daily(self.test_df_2)['color_code'], '000000')
        self.assertEqual(best_session_daily(self.test_df_2)['unicode'], u'\u003D')

    def test_best_session_weekly(self):
        self.assertEqual(len(best_session_daily(self.test_df_2)), 4)
        self.assertEqual(best_session_weekly(self.test_df_2)['best_session_weekly'], 0)
        self.assertEqual(best_session_weekly(self.test_df_2)['difference'], 100)
        self.assertEqual(best_session_weekly(self.test_df_2)['color_code'], '000000')
        self.assertEqual(best_session_weekly(self.test_df_2)['unicode'], u'\u003D')

    def test_best_session_monthly(self):
        self.assertEqual(len(best_session_monthly(self.test_df_2)), 4)
        self.assertEqual(best_session_monthly(self.test_df_2)['best_session_monthly'], 0)
        self.assertEqual(best_session_monthly(self.test_df_2)['difference'], 100)
        self.assertEqual(best_session_monthly(self.test_df_2)['color_code'], '000000')
        self.assertEqual(best_session_monthly(self.test_df_2)['unicode'], u'\u003D')

    def test_make_results_dict(self):
        metric = 1
        difference = 1
        color = 'blue'
        unicode = '='
        self.assertEqual(make_results_dict(metric, difference, color, unicode), {'metric': 1, 'difference': 1,
                                                                                 'color_code': 'blue', 'unicode': u'\u003D'})


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
        self.assertEqual(get_API_params('Cat'), {'action': 'query', 'prop': 'extracts', 'exchars': '190',
                                                 'titles': 'Cat', 'format': 'json', 'explaintext': 1, 'exlimit': 1})
        self.assertIs(type(get_API_params('Cat')), dict)

    def test_get_opensearch_params(self):
        self.assertEqual(get_opensearch_params('Cat'), {'action': 'opensearch', 'search': 'Cat', 'redirects': 'resolve',
                                                        'format': 'json'})
        self.assertIs(type(get_opensearch_params('Cat')), dict)

    def test_retrieve_definition(self):
        self.assertIs(type(retrieve_definition('Cat')), str)


class TestLeitner(unittest.TestCase):

    def test_leitner_dates(self):
        test_matrix = [(0, 0, 3, ''),
                       (1, 0, 3, ''),
                       (2, 1, 2, ''),
                       (3, 1, 5, ''),
                       (4, 0, 5, '')]

        test_df = pd.DataFrame(test_matrix,
                               columns=['card_id',
                                        'is_starred',
                                        'comfort_level',
                                        'next_due'])

        self.df = test_df.apply(leitner_dates, axis=1)

        # Expected values for comfort_level after test_df is run through
        # leitner
        comfort_level_series = pd.Series(data=[4, 4, 1, 1, 5], name='comfort_level')
        pd.testing.assert_series_equal(self.df['comfort_level'],
                                       comfort_level_series)
        self.assertIs(type(self.df['next_due'][0]), str)


if __name__ == '__main__':
    unittest.main()
