import streamlit as st
import pandas as pd
from typing import Dict, Optional

class SessionManager:
    """
    Wrapper around st.session_state to manage application state in a structured way.
    """
    
    # Keys for session state
    KEY_STEP = 'current_step'
    KEY_RAW_DATA = 'raw_dataframes'
    KEY_MERGED_DF = 'merged_df'
    KEY_PIVOT_CANDIDATES = 'pivot_candidates'
    KEY_SELECTED_PIVOT = 'selected_pivot'

    def __init__(self):
        """Initialize session state with defaults if not present."""
        if self.KEY_STEP not in st.session_state:
            st.session_state[self.KEY_STEP] = 1
        
        if self.KEY_RAW_DATA not in st.session_state:
            st.session_state[self.KEY_RAW_DATA] = {}
            
        if self.KEY_MERGED_DF not in st.session_state:
            st.session_state[self.KEY_MERGED_DF] = None

        if self.KEY_PIVOT_CANDIDATES not in st.session_state:
            st.session_state[self.KEY_PIVOT_CANDIDATES] = None
            
        if self.KEY_SELECTED_PIVOT not in st.session_state:
            st.session_state[self.KEY_SELECTED_PIVOT] = None

    @property
    def current_step(self) -> int:
        return st.session_state[self.KEY_STEP]

    def next_step(self):
        st.session_state[self.KEY_STEP] += 1

    def prev_step(self):
        if st.session_state[self.KEY_STEP] > 1:
            st.session_state[self.KEY_STEP] -= 1

    def reset(self):
        """Resets the wizard to the beginning."""
        st.session_state[self.KEY_STEP] = 1
        st.session_state[self.KEY_RAW_DATA] = {}
        st.session_state[self.KEY_MERGED_DF] = None
        st.session_state[self.KEY_PIVOT_CANDIDATES] = None
        st.session_state[self.KEY_SELECTED_PIVOT] = None
        st.rerun()

    def set_dataframes(self, dfs: Dict[str, pd.DataFrame]):
        st.session_state[self.KEY_RAW_DATA] = dfs

    def get_dataframes(self) -> Dict[str, pd.DataFrame]:
        return st.session_state[self.KEY_RAW_DATA]

    def set_merged_df(self, df: pd.DataFrame):
        st.session_state[self.KEY_MERGED_DF] = df

    def get_merged_df(self) -> Optional[pd.DataFrame]:
        return st.session_state[self.KEY_MERGED_DF]
    
    def set_pivot_candidates(self, df: pd.DataFrame):
        st.session_state[self.KEY_PIVOT_CANDIDATES] = df
        
    def get_pivot_candidates(self) -> Optional[pd.DataFrame]:
        return st.session_state[self.KEY_PIVOT_CANDIDATES]
    
    def set_selected_pivot(self, pivot: str):
        st.session_state[self.KEY_SELECTED_PIVOT] = pivot
        
    def get_selected_pivot(self) -> Optional[str]:
        return st.session_state[self.KEY_SELECTED_PIVOT]
