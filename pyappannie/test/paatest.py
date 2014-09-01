import sys
import unittest
import pyappannie

class pAATest(unittest.TestCase):
    def __init__(self, testname, api_key):
        super(pAATest, self).__init__(testname)
        self.api_key = api_key
        
    def setUp(self):
        self.API = pyappannie.API(self.api_key)

    def meta_test(self):
        meta1 = self.API.meta_regions()
        meta1_keys = ['code', 'country_list', 'region_list']
        self.assertTrue(set(meta1_keys) == set(meta1.keys()))

if __name__ == '__main__':
    key = sys.argv[1]
    appAnnieTestSuite = unittest.TestSuite()
    appAnnieTestSuite.addTest(pAATest('meta_test', key))
    unittest.TextTestRunner().run(appAnnieTestSuite)