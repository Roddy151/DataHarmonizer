import streamlit as st
import sys
import os

# Ensure the project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.state import SessionManager
from ui.wizard import (
    render_upload_step,
    render_pivot_check,
    render_schema_selector,
    render_download
)

# Page Configuration
st.set_page_config(
    page_title="Data Harmonizer",
    page_icon="🧬",
    layout="centered"
)

def main():
    st.title("🧬 Data Harmonizer")
    st.caption("ETL Last Mile Assistant | Unify disparate data sources with ease.")
    st.divider()

    # Initialize Session
    session = SessionManager()
    
    # Global Error Handling
    try:
        # Step Progress Indicator
        step = session.current_step
        steps = {
            1: "Ingest",
            2: "Unify",
            3: "Curate",
            4: "Export"
        }
        
        # Simple text progress for cleanliness
        st.markdown(f"**Step {step}/4: {steps.get(step, 'Unknown')}**")
        st.progress(step / 4)
        
        # Wizard Flow Orchestration
        if step == 1:
            render_upload_step(session)
        elif step == 2:
            render_pivot_check(session)
        elif step == 3:
            render_schema_selector(session)
        elif step == 4:
            render_download(session)
        else:
            st.error("Invalid state. Resetting application.")
            session.reset()
            
    except Exception as e:
        st.error("An unexpected error occurred.")
        st.exception(e)
        if st.button("Reset Application"):
            session.reset()

if __name__ == "__main__":
    main()
