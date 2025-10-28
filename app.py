import streamlit as st
import pandas as pd
import plotly.express as px
from agents.query_agent import generate_sql_queries, execute_query

st.set_page_config(page_title="Auto Insight Agent Pro", layout="wide")

st.title("🧩 DataMind AI — Intelligent Data Companion")
st.markdown("""
<h4 style='text-align:center; color:#4a90e2;'>
🧠 Understand &nbsp; | &nbsp; 💬 Query &nbsp; | &nbsp; 📊 Visualize &nbsp; | &nbsp; ⚡ Instantly
</h4>
""", unsafe_allow_html=True)


if "data" not in st.session_state:
    st.session_state.data = None

# 📂 Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state.data = df.copy()

    # 🧹 Clean Data
    st.subheader("🧹 Data Cleaning Summary")
    before = df.shape
    df.drop_duplicates(inplace=True)
    df.fillna(df.mean(numeric_only=True), inplace=True)
    after = df.shape

    st.write(f"✅ Removed {before[0]-after[0]} duplicate rows.")
    st.write("✅ Filled missing numeric values with column means.")
    st.session_state.data = df

    # 📊 Data Preview
    st.subheader("📊 Data Preview")
    st.dataframe(df.head(10))

    # 💬 Ask question
    st.subheader("💬 Ask a Question about Your Data")
    user_question = st.text_input("Example: 'Show top 5 highest salaries'")

    if st.button("Generate & Execute Query"):
        if not user_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("🔍 Understanding your question..."):
                queries = generate_sql_queries(user_question, df)

            if not queries:
                st.error("❌ Couldn't generate a valid SQL query. Try rephrasing.")
            else:
                for i, query in enumerate(queries, start=1):
                    st.markdown(f"### 🧠 Query {i}")
                    st.code(query, language="sql")

                    try:
                        result = execute_query(query, df)
                        st.dataframe(result.head(10))

                        # 🧭 Auto Visualization
                        numeric_cols = result.select_dtypes(include='number').columns.tolist()
                        if len(result.columns) >= 2 and len(numeric_cols) >= 1:
                            x_col = result.columns[0]
                            y_col = numeric_cols[0]
                            st.markdown(f"📈 Visualization for {x_col} vs {y_col}")
                            fig = px.bar(result, x=x_col, y=y_col, title="Auto Visualization")
                            st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"⚠️ Error executing query: {e}")
