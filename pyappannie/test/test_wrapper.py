import sys
import unittest
import pyappannie

class MetaTest(unittest.TestCase):
    def __init__(self, testname, api_key):
        super(MetaTest, self).__init__(testname)
        self.api_key = api_key
        
    def setUp(self):
        self.API = pyappannie.API(self.api_key)

    def meta_countries(self):
        response = self.API.meta_regions()
        keys = ['code', 'country_list', 'region_list']
        self.assertTrue(set(keys) == set(response.keys()))
        self.assertEqual(response['code'], 200)

    def meta_categories(self):
        response = self.API.meta_categories(market = 'ios')
        keys = ['code', 'categories', 'appannie_categories']
        self.assertTrue(set(keys) == set(response.keys()))
        self.assertEqual(response['code'], 200)
    
    def meta_platforms(self):
        response = self.API.meta_platforms()
        keys = ['code', 'platforms']
        self.assertTrue(set(keys) == set(response.keys()))
        self.assertEqual(response['code'], 200)
        
        names = [x['platform_name'] for x in response['platforms']]
        self.assertTrue('iTunes Connect' in names)
        self.assertTrue('Google Play' in names)

    def meta_currencies(self):
        response = self.API.meta_currencies()
        keys = ['code', 'currency_list']
        self.assertTrue(set(keys) == set(response.keys()))
        self.assertEqual(response['code'], 200)
        
        dollar = [x for x in response['currency_list'] if x['currency_code'] == 'USD'][0]
        self.assertEqual(dollar['symbol'], '$')

if __name__ == '__main__':
    key = sys.argv[1]
    appAnnieTestSuite = unittest.TestSuite()
    appAnnieTestSuite.addTest(MetaTest('meta_countries', key))
    appAnnieTestSuite.addTest(MetaTest('meta_categories', key))
    appAnnieTestSuite.addTest(MetaTest('meta_platforms', key))
    appAnnieTestSuite.addTest(MetaTest('meta_currencies', key))
    unittest.TextTestRunner().run(appAnnieTestSuite)