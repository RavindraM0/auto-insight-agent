import streamlit as st
import pandas as pd
from agents.cleaner_agent import clean_data
from agents.query_agent import nl_to_sql, execute_sql
from agents.visualize_agent import auto_visualize_from_df
from agents.auto_agent import autonomous_analysis
from utils.dashboard_generator import save_dashboard_html
from utils.report_generator import generate_pdf_report

st.set_page_config(page_title="Auto-Insight Agent Pro", layout="wide")
st.title("Auto-Insight Agent Pro")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if st.button("Load sample dataset"):
    uploaded = "sample_data/retail_sales.csv"  

if uploaded:
    if isinstance(uploaded, str):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv(uploaded)

    st.subheader("Raw data (first 10 rows)")
    st.dataframe(df.head(10))

    st.subheader("Cleaning")
    cleaned_df, corrections = clean_data(df.copy())
    st.success("Data cleaned.")
    st.dataframe(cleaned_df.head(10))
    if corrections:
        st.markdown("**Corrections performed**")
        for c in corrections:
            st.markdown(f"- {c}")

    st.subheader("Profile (quick)")
    if st.button("Show profile"):
        from ydata_profiling import ProfileReport
        profile = ProfileReport(cleaned_df, minimal=True)
        st.components.v1.html(profile.to_html(), height=700, scrolling=True)

    st.subheader("Ask a question (Natural language → SQL)")
    query = st.text_input("Example: 'Total sales by region for 2023'")

    col1, col2, col3 = st.columns(3)
    with col1:
        run_query = st.button("Run query")
    with col2:
        save_dashboard = st.button("Generate dashboard HTML")
    with col3:
        gen_report = st.button("Generate PDF report")

    if run_query and query:
        with st.spinner("Generating SQL (local Flan-T5)..."):
            sql = nl_to_sql(query, cleaned_df)
        st.markdown("**Generated SQL:**")
        st.code(sql)
        try:
            res = execute_sql(sql, cleaned_df)
            st.dataframe(res.head(200))
            fig = auto_visualize_from_df(res)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Execution/visualization error: {e}")

    if save_dashboard:
        out = save_dashboard_html(cleaned_df, "dashboard.html")
        st.success(f"Dashboard saved: {out}")

    if gen_report:
        outp = generate_pdf_report(cleaned_df, "report.pdf")
        st.success(f"PDF report generated: {outp}")

    st.subheader("Agentic Mode")
    if st.button("Run Autonomous Mode"):
        report = autonomous_analysis(cleaned_df)
        st.markdown("**Autonomous Analysis:**")
        for line in report:
            st.markdown(f"- {line}")

st.sidebar.markdown("Made with ❤️By RAVINDRA MO")
