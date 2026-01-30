import unittest
import pandas as pd
import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.heuristics import calculate_pivot_score

class TestHeuristics(unittest.TestCase):
    
    def test_perfect_pivot(self):
        """Test a column that should get a perfect score (Unique + Name + Type)."""
        df = pd.DataFrame({
            'task_id': ['1', '2', '3', '4'],
            'value': ['a', 'b', 'a', 'b']
        })
        
        scores = calculate_pivot_score(df)
        
        # task_id check
        # Uniq: 1.0 (0.5), Name: Match (0.3), Type: Str (0.2) -> Total: 1.0
        task_id_row = scores[scores['Campo'] == 'task_id'].iloc[0]
        self.assertAlmostEqual(task_id_row['Puntaje'], 1.0)
        
    def test_partial_scores(self):
        """Test columns with mixed characteristics."""
        df = pd.DataFrame({
            'id': [1, 2, 3, 4],          # Perfect: 1.0
            'category': ['A', 'A', 'B', 'B'], # Low Uniq (0.5), No Name (0), Type (0.2) -> 0.25 + 0.2 = 0.45
            'price': [10.5, 20.0, 10.5, 5.0],  # Low Uniq, No Name, Bad Type -> Low score
            'uuid': ['a', 'b', 'c', 'd']       # Perfect: 1.0
        })
        
        scores = calculate_pivot_score(df)
        
        # Check ordering
        top_cols = scores.iloc[:2]['Campo'].tolist()
        self.assertIn('id', top_cols)
        self.assertIn('uuid', top_cols)
        
        cat_score = scores[scores['Campo'] == 'category'].iloc[0]['Puntaje']
        # Uniq = 2/4 = 0.5 * 0.5 = 0.25
        # Name = 0
        # Type = 1 * 0.2 = 0.2
        # Total = 0.45
        self.assertAlmostEqual(cat_score, 0.45)

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame()
        scores = calculate_pivot_score(df)
        self.assertTrue(scores.empty)

if __name__ == '__main__':
    unittest.main()
