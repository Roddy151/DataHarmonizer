import pandas as pd
import json
from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict, Any
from io import BytesIO

class BaseLoader(ABC):
    """Abstract base class for data loaders."""

    @abstractmethod
    def load(self, file_content: BytesIO, filename: str) -> pd.DataFrame:
        """
        Loads data from file content into a Pandas DataFrame.
        
        Args:
            file_content: The file content as bytes.
            filename: The name of the file (useful for debugging/logging).
            
        Returns:
            pd.DataFrame: The loaded data.
        """
        pass

class CsvLoader(BaseLoader):
    """Loader for CSV files."""

    def load(self, file_content: BytesIO, filename: str) -> pd.DataFrame:
        try:
            # Simple loading for now, can be enhanced with sniffing later
            return pd.read_csv(file_content)
        except Exception as e:
            raise ValueError(f"Error loading CSV {filename}: {str(e)}")

class ExcelLoader(BaseLoader):
    """Loader for Excel files."""

    def load(self, file_content: BytesIO, filename: str) -> pd.DataFrame:
        try:
            return pd.read_excel(file_content)
        except Exception as e:
            raise ValueError(f"Error loading Excel {filename}: {str(e)}")

class JsonLoader(BaseLoader):
    """Loader for JSON files with automatic flattening of nested structures."""
    
    # Common keys used in Scale AI and other tools to wrap the list of records
    RECORD_PATH_CANDIDATES = ['tasks', 'items', 'annotations', 'response', 'records', 'data']

    def load(self, file_content: BytesIO, filename: str) -> pd.DataFrame:
        try:
            data = json.load(file_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filename}: {str(e)}")

        record_path = self._detect_record_path(data)
        
        if record_path:
            # If a record path is found, use json_normalize to flatten and propagate metadata
            # meta parameter is set to common top-level keys excluding complex objects to avoid errors
            meta_keys = [k for k, v in data.items() if k != record_path and isinstance(v, (str, int, float, bool, type(None)))]
            df = pd.json_normalize(data, record_path=record_path, meta=meta_keys)
        else:
            # If no specific record path, assume the root is the list or it's a flat dict
            if isinstance(data, list):
                df = pd.json_normalize(data)
            else:
                # Wrap single object in list
                df = pd.json_normalize([data])
                
        return df

    def _detect_record_path(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Heuristically detects the key containing the main list of records.
        """
        if not isinstance(data, dict):
            return None
            
        # 1. Check for specific candidates
        for candidate in self.RECORD_PATH_CANDIDATES:
            if candidate in data and isinstance(data[candidate], list):
                if len(data[candidate]) > 0: # Prefer non-empty lists
                    return candidate

        # 2. If no candidate found, look for ANY key that holds a list
        # Heuristic: The key with the longest list is likely the data
        longest_list_key = None
        max_len = -1
        
        for key, value in data.items():
            if isinstance(value, list):
                if len(value) > max_len:
                    max_len = len(value)
                    longest_list_key = key
        
        return longest_list_key
