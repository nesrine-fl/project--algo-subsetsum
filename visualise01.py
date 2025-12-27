import streamlit as st
import pandas as pd
import time
import plotly.express as px
from read_write_files import *
from subsetsum import *

# --- UI Configuration ---
st.set_page_config(page_title="SUBSETSUM Analyzer - M1 MIV", layout="wide")

# --- FIXED SECTION: Correct parameter name is unsafe_allow_html ---
# The previous error was caused by 'unsafe_allow_name_with_html'
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True) 

# --- Header Section ---
st.title("🧮 Subset Sum Problem Solver")
st.subheader("Algorithmique et Complexité (M1-MIV) - USTHB")
st.write("Analysis of Backtracking vs. Official Benchmarks")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Parameters")
    instance_id = st.selectbox("Select Benchmark Instance", 
                               options=[f"p{str(i).zfill(2)}" for i in range(1, 21)], 
                               index=3) 
    run_button = st.button("🚀 Run Analysis", type="primary")

# --- Logic & Processing ---
if run_button:
    with st.spinner(f'Fetching and solving {instance_id}...'):
        # 1. Load Data
        nums, target, known_solutions_01 = load_instance(instance_id)
        
        # 2. Solve Backtracking & Time
        
        start_time = time.perf_counter()
        found_subsets = subsets(nums, target)
        end_time = time.perf_counter()
        bt_time = end_time - start_time

        # 3. Solve DP (one solution) & Time
        dp_start = time.perf_counter()
        # Ensure your Solution class in backtracking.py has this method
        dp_solution = dp_subset_sum_one(nums, target)
        dp_end = time.perf_counter()
        dp_time = dp_end - dp_start

        # --- Dashboard Metrics ---
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Target Sum (T)", target)
        col2.metric("Set Size (n)", len(nums))
        col3.metric("Solutions Found", len(found_subsets))
        col4.metric("Backtracking Time", f"{bt_time:.4f}s")
        col5.metric("DP Time (one sol)", f"{dp_time:.4f}s")

        # --- Results Table Preparation ---
        rows = []
        
        for subset in found_subsets:
            binary_list = subset_to_binary(nums, subset)
            binary_str = "".join(str(b) for b in binary_list)
            is_official = binary_str in known_solutions_01
            
            rows.append({
                "Subset": str(subset),
                "Binary Vector": binary_str,
                "Sum": sum(subset),
                "Valid?": "✅" if sum(subset) == target else "❌",
                "Official?": "🌟 Yes" if is_official else "⚠️ Extra"
            })

        df_found = pd.DataFrame(rows)

        # --- Display Table ---
        st.write(f"### Results for Instance: `{instance_id}`")
        if not df_found.empty:
            st.dataframe(df_found, use_container_width=True)
        else:
            st.warning("No solutions found.")

        # --- DP solution display ---
        st.write("### DP (one solution)")
        if dp_solution:
            dp_binary = subset_to_binary(nums, dp_solution)
            dp_bits = "".join(str(b) for b in dp_binary)
            st.write(f"Values: {dp_solution}")
            st.write(f"Binary: {dp_bits}")
            st.write("Matches official? " + ("✅ Yes" if dp_bits in known_solutions_01 else "⚠️ No"))
        else:
            st.warning("DP found no solution.")

        # --- FIXED Plotly Chart ---
        # Fixed the variable mismatch: used bt_time and dp_time instead of the missing exec_time
        fig = px.bar(
            x=["Backtracking", "Dynamic Programming"], 
            y=[bt_time, dp_time], 
            labels={'x': 'Algorithm', 'y': 'Execution Time (Seconds)'}, 
            title="Performance Comparison: Backtracking vs DP"
        )
        st.plotly_chart(fig)

else:
    st.info("Select an instance and click 'Run Analysis'.")