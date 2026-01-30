import streamlit as st
import pandas as pd
from io import BytesIO
from core.ingestion import CsvLoader, ExcelLoader, JsonLoader
from core.heuristics import calculate_pivot_score
from core.transformation import merge_datasets
from ui.state import SessionManager

def render_upload_step(session: SessionManager):
    """Step 1: Upload Files"""
    st.header("1. Data Ingestion")
    st.markdown("Upload multiple datasets (CSV, Excel, JSON). The system will normalize them automatically.")
    
    uploaded_files = st.file_uploader(
        "Choose files", 
        type=['csv', 'xlsx', 'xls', 'json'], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Analyze Files"):
            loaded_data = {}
            all_dfs = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                for i, file in enumerate(uploaded_files):
                    status_text.text(f"Processing {file.name}...")
                    
                    if file.name.endswith('.csv'):
                        loader = CsvLoader()
                    elif file.name.endswith(('.xlsx', '.xls')):
                        loader = ExcelLoader()
                    elif file.name.endswith('.json'):
                        loader = JsonLoader()
                    else:
                        st.error(f"Unsupported file type: {file.name}")
                        continue
                        
                    # Reset pointer just in case
                    file.seek(0)
                    df = loader.load(file, file.name)
                    loaded_data[file.name] = df
                    all_dfs.append(df)
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                if all_dfs:
                    session.set_dataframes(loaded_data)
                    
                    # Calculate heuristics on concatenated schema (or just the first/all depending on strategy)
                    # Strategy: Concatenate all columns to see the "Super Schema" for heuristic calculation is a bit tricky if they don't align.
                    # Better Strategy: Heuristics run on the dataset that "leads" or aggregated view. 
                    # Re-reading prompt: "The system aggregates all column headers... forms a single Super Schema... Heuristic Brain evaluates each column".
                    # Implementation: Create a dummy DF with all columns from all DFs (outer join of schemas essentially)
                    # Efficient way: Just get all unique column names, check if they exist in DFs and getting stats is complex if not merged.
                    # Simplified practical approach for now: Run heuristics on *each* DF and average scores OR assume common schema.
                    # *Correction per architecture*: "Super Schema". Let's concat all frames (outer) to get full column set and stats.
                    
                    status_text.text("Calculating automated pivot suggestions...")
                    # Concat for analysis only (might be heavy, but safe for small internal tool)
                    super_df = pd.concat(all_dfs, ignore_index=True, sort=False)
                    
                    candidates = calculate_pivot_score(super_df)
                    session.set_pivot_candidates(candidates)
                    session.next_step()
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error processing files: {str(e)}")
            finally:
                progress_bar.empty()
                status_text.empty()

def render_pivot_check(session: SessionManager):
    """Step 2: Pivot Validation"""
    st.header("2. Pivot Validation")
    st.markdown("Confirm the primary key to unify your datasets.")
    
    candidates = session.get_pivot_candidates()
    
    if candidates is not None and not candidates.empty:
        # Get top candidate
        top_candidate = candidates.iloc[0]['Campo']
        top_score = candidates.iloc[0]['Puntaje']
        
        st.info(f"Top Recommendation: **{top_candidate}** (Confidence: {top_score:.2f})")
        
        # Selection Box
        selected_col = st.selectbox(
            "Select Pivot Column", 
            options=candidates['Campo'].tolist(),
            index=0
        )
        
        # Show Evidence
        row = candidates[candidates['Campo'] == selected_col].iloc[0]
        st.caption(f"Reasoning: {row['Evidencia']}")
        
        # Validation for duplicates
        data_map = session.get_dataframes()
        has_dupes = False
        
        # Check specific duplicates in source files for the chosen pivot
        for name, df in data_map.items():
            if selected_col in df.columns:
                if df[selected_col].duplicated().any():
                    has_dupes = True
                    st.warning(f"⚠️ Duplicate values found for '{selected_col}' in file: {name}")
        
        if st.button("Confirm and Unify"):
            try:
                # Perform the Merge
                dfs = list(data_map.values())
                merged_df = merge_datasets(dfs, selected_col)
                
                session.set_merged_df(merged_df)
                session.set_selected_pivot(selected_col)
                session.next_step()
                st.rerun()
            except Exception as e:
                st.error(f"Merge failed: {str(e)}")

def render_schema_selector(session: SessionManager):
    """Step 3: Schema Curation"""
    st.header("3. Schema Selection")
    st.markdown("Select the columns you want to include in the final report.")
    
    merged_df = session.get_merged_df()
    
    if merged_df is not None:
        # Create a helper dataframe for the editor
        all_cols = merged_df.columns.tolist()
        
        # Default: Keep provided pivot, drop suffixes if redundant? Na, let user choose.
        # Initialize selection state if not exists in session (to keep checks between reloads)
        if 'column_config' not in st.session_state:
            st.session_state['column_config'] = pd.DataFrame({
                'Column Name': all_cols,
                'Include': [True] * len(all_cols)
            })
            
        edited_config = st.data_editor(
            st.session_state['column_config'],
            column_config={
                "Include": st.column_config.CheckboxColumn(
                    "Keep?",
                    help="Select to include in final output",
                    default=True,
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.session_state['column_config'] = edited_config
        
        if st.button("Generate Final Report"):
            # Filter columns
            selected_cols = edited_config[edited_config['Include']]['Column Name'].tolist()
            final_df = merged_df[selected_cols]
            
            # Store final result temporarily or just pass to next step?
            # We can just update the merged_df in session or create a new key.
            # Updating merged_df is cleaner for step 4.
            session.set_merged_df(final_df)
            session.next_step()
            st.rerun()

def render_download(session: SessionManager):
    """Step 4: Export"""
    st.header("4. Download Artifact")
    st.success("Data harmonization complete! Your consolidated report is ready.")
    
    final_df = session.get_merged_df()
    
    if final_df is not None:
        st.metric(label="Total Rows", value=len(final_df))
        st.metric(label="Total Columns", value=len(final_df.columns))
        
        st.dataframe(final_df.head())
        
        # Buffer for Excel
        buffer = BytesIO()
        try:
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                final_df.to_excel(writer, index=False, sheet_name='Clean Data')
            
            st.download_button(
                label="Download Excel Report (.xlsx)",
                data=buffer.getvalue(),
                file_name="harmonized_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error generating Excel: {str(e)}")
        
        if st.button("Start New Session"):
            session.reset()
