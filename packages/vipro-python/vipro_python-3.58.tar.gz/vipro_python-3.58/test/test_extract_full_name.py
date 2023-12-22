# ability to import module from relative path
import sys; sys.path.insert(0,'./src'); sys.path.insert(0,'../src')

import unittest
import pandas as pd
from vipro_python.lacf.pii_headers import extract_full_name_from_df

class TestNoPostcode(unittest.TestCase):
    
    def testFixesFullName(self):
        df = pd.DataFrame([['Tom Medhurst'], ['Bob Jones'], ['Billy-Ray Cyrus']], columns=['full_name'])
        df = extract_full_name_from_df(df)
        self.assertIn('forename', df.columns)
        self.assertIn('surname', df.columns)
        self.assertNotIn('full_name', df.columns)

    def testSingleName(self):
        df = pd.DataFrame([['Tom'], ['Bob Jones'], ['Billy-Ray']], columns=['full_name'])
        df = extract_full_name_from_df(df).dropna(subset='surname')
        #print(df.to_csv())
        self.assertEqual(1, len(df), f'should have only kept Bob: {df.to_json()}')