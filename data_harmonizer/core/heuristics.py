import pandas as pd
import re

def calculate_pivot_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates a 'pivot score' for each column in the DataFrame to identify potential primary keys.
    
    Score Formula:
    S(c) = (W_uniq * U(c)) + (W_name * N(c)) + (W_type * T(c))
    
    Where:
    - W_uniq = 0.5, U(c) = Uniqueness ratio (unique / total non-null)
    - W_name = 0.3, N(c) = 1.0 if name matches pattern, else 0.0
    - W_type = 0.2, T(c) = 1.0 if type is int or string, else 0.0
    """
    
    results = []
    
    # Weights
    W_UNIQ = 0.5
    W_NAME = 0.3
    W_TYPE = 0.2
    
    # Regex for high probability names
    NAME_PATTERN = re.compile(r'^(id|uuid|pk|key|task_id|_id)$', re.IGNORECASE)
    
    for col in df.columns:
        # 1. Uniqueness Score
        count = df[col].count()
        if count == 0:
            uniq_score = 0.0
        else:
            uniq_score = df[col].nunique() / count
            
        # 2. Name Score
        if NAME_PATTERN.match(str(col)):
            name_score = 1.0
            name_match = "Match"
        else:
            name_score = 0.0
            name_match = "No Match"
            
        # 3. Type Score
        dtype = df[col].dtype
        if pd.api.types.is_integer_dtype(dtype) or pd.api.types.is_string_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
            type_score = 1.0
            type_desc = "Str/Int"
        else:
            type_score = 0.0
            type_desc = "Other"
            
        # Total Score
        total_score = (W_UNIQ * uniq_score) + (W_NAME * name_score) + (W_TYPE * type_score)
        
        # Evidence String
        evidence = f"Uniq: {uniq_score:.2f}, Name: {name_match}, Type: {type_desc}"
        
        results.append({
            'Campo': col,
            'Puntaje': total_score,
            'Evidencia': evidence
        })
        
    # Create DataFrame and sort
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        results_df = results_df.sort_values(by='Puntaje', ascending=False)
        
    return results_df
