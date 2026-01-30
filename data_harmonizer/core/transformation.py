import pandas as pd
from typing import List

def merge_datasets(dataframes: List[pd.DataFrame], pivot_column: str) -> pd.DataFrame:
    """
    Merges a list of DataFrames into a single DataFrame using an iterative outer join.
    
    Args:
        dataframes: List of pd.DataFrame objects to merge.
        pivot_column: The common column name to join on.
        
    Returns:
        pd.DataFrame: The merged result.
    """
    if not dataframes:
        return pd.DataFrame()
    
    if len(dataframes) == 1:
        return dataframes[0]
    
    # Start with the first dataframe
    result = dataframes[0]
    
    # Iteratively merge subsequent dataframes
    for i, current_df in enumerate(dataframes[1:], start=1):
        # We assume the pivot column exists in all dataframes.
        # If not, pandas will raise a Key error, which is acceptable behavior as validation implies it should exist.
        
        if pivot_column not in result.columns:
             raise ValueError(f"Pivot column '{pivot_column}' missing in the base dataset.")
        if pivot_column not in current_df.columns:
             raise ValueError(f"Pivot column '{pivot_column}' missing in dataset #{i+1}.")

        # Perform Outer Join
        # Suffixes strategy:
        # - Left (result): No suffix (keep existing names or previously suffixed names)
        # - Right (current_df): '_file{i+1}' (e.g., _file2, _file3, etc.)
        suffix_right = f"_file{i+1}"
        
        result = pd.merge(
            result, 
            current_df, 
            on=pivot_column, 
            how='outer', 
            suffixes=(None, suffix_right)
        )
        
    return result
