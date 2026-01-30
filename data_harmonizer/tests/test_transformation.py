import unittest
import pandas as pd
import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.transformation import merge_datasets

class TestTransformation(unittest.TestCase):
    
    def test_merge_two_simple(self):
        """Test merging two dataframes with complete overlap."""
        df1 = pd.DataFrame({'id': [1, 2], 'val': ['a', 'b']})
        df2 = pd.DataFrame({'id': [1, 2], 'score': [10, 20]})
        
        result = merge_datasets([df1, df2], 'id')
        
        self.assertEqual(len(result), 2)
        self.assertIn('val', result.columns)
        self.assertIn('score', result.columns)

    def test_merge_outer_join_behavior(self):
        """Test that rows are preserved (outer join)."""
        df1 = pd.DataFrame({'id': [1, 2], 'val': ['a', 'b']})
        df2 = pd.DataFrame({'id': [2, 3], 'score': [20, 30]})
        
        result = merge_datasets([df1, df2], 'id')
        
        self.assertEqual(len(result), 3) # IDs: 1, 2, 3
        # ID 3 should have NaN for 'val'
        row_3 = result[result['id'] == 3].iloc[0]
        self.assertTrue(pd.isna(row_3['val']))
        self.assertEqual(row_3['score'], 30)

    def test_suffix_handling(self):
        """Test column name collision handling with 3 files."""
        # File 1
        df1 = pd.DataFrame({'id': [1], 'status': ['active']})
        # File 2 (Collides 'status')
        df2 = pd.DataFrame({'id': [1], 'status': ['pending']})
        # File 3 (Collides 'status' again)
        df3 = pd.DataFrame({'id': [1], 'status': ['closed']})
        
        result = merge_datasets([df1, df2, df3], 'id')
        
        self.assertIn('status', result.columns)         # From File 1
        self.assertIn('status_file2', result.columns)   # From File 2
        self.assertIn('status_file3', result.columns)   # From File 3
        
        row = result.iloc[0]
        self.assertEqual(row['status'], 'active')
        self.assertEqual(row['status_file2'], 'pending')
        self.assertEqual(row['status_file3'], 'closed')

    def test_empty_input(self):
        result = merge_datasets([], 'id')
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()
