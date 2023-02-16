import unittest as ut
from scrapper import CoinmarketcapScraper
import pandas as pd

class testCoinmarketcap(ut.TestCase):

    def setUp(self):
        self.scraper = CoinmarketcapScraper()

    def test_fetch_data(self):
        links, names = self.scraper.fetch_data()
        self.assertEqual(len(links), 10)
        self.assertEqual(len(names), 10)

    def test_process_data(self):
        links, names = self.scraper.fetch_data()
        df_final = self.scraper._process_data(links, names)
        self.assertIsInstance(df_final, pd.DataFrame)
        self.assertGreater(df_final.shape[0], 0)

    def tearDown(self):
        self.scraper.close_browser()


if __name__ == '__main__':
    ut.main()