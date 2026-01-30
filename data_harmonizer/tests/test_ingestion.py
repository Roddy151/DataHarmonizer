import unittest
import json
import pandas as pd
from io import BytesIO
import sys
import os

# Add the project root to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ingestion import JsonLoader

class TestJsonLoader(unittest.TestCase):
    
    def test_load_scale_ai_style_json(self):
        """Test loading a JSON with a 'tasks' list and root metadata."""
        json_content = {
            "project_id": "proj_123",
            "batch_id": "batch_456",
            "tasks": [
                {
                    "task_id": "t1", 
                    "data": {"image_url": "http://example.com/1.jpg"},
                    "annotations": [{"label": "cat"}]
                },
                {
                    "task_id": "t2", 
                    "data": {"image_url": "http://example.com/2.jpg"},
                    "annotations": [{"label": "dog"}]
                }
            ]
        }
        
        content_bytes = BytesIO(json.dumps(json_content).encode('utf-8'))
        loader = JsonLoader()
        df = loader.load(content_bytes, "test.json")
        
        # Verify flattening
        self.assertIn('task_id', df.columns)
        self.assertIn('data.image_url', df.columns)
        
        # Verify metadata propagation
        self.assertIn('project_id', df.columns)
        self.assertEqual(df.iloc[0]['project_id'], 'proj_123')
        
        # Verify number of rows
        self.assertEqual(len(df), 2)

    def test_load_flat_list(self):
        """Test loading a simple list of objects."""
        json_content = [
            {"id": 1, "val": "a"},
            {"id": 2, "val": "b"}
        ]
        content_bytes = BytesIO(json.dumps(json_content).encode('utf-8'))
        loader = JsonLoader()
        df = loader.load(content_bytes, "simple.json")
        
        self.assertEqual(len(df), 2)
        self.assertIn('id', df.columns)

    def test_load_unknown_list_key(self):
        """Test loading where the list key is not in the common candidate list."""
        json_content = {
            "meta_info": "irrelevant",
            "obscure_list_name": [
                {"id": 1},
                {"id": 2}
            ]
        }
        content_bytes = BytesIO(json.dumps(json_content).encode('utf-8'))
        
        loader = JsonLoader()
        # It should heuristically find 'obscure_list_name' as it's the only list
        df = loader.load(content_bytes, "unknown.json")
        
        self.assertEqual(len(df), 2)
        self.assertIn('id', df.columns)
        # Verify metadata propagation works even for heuristic detection
        self.assertIn('meta_info', df.columns)

if __name__ == '__main__':
    unittest.main()
