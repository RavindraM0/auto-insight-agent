import streamlit as st
import pandas as pd
import plotly.express as px
import speech_recognition as sr
from agents.query_agent import generate_sql_query, execute_query

st.set_page_config(page_title="Auto Insight Agent Pro", layout="wide")

st.title("🧩 DataMind AI — Intelligent Data Companion")
st.markdown("""
<h4 style='text-align:center; color:#4a90e2;'>
🧠 Understand &nbsp; | &nbsp; 💬 Query &nbsp; | &nbsp; 📊 Visualize &nbsp; | &nbsp; ⚡ Instantly
</h4>
""", unsafe_allow_html=True)


# --- Upload CSV ---
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Data cleaning
    df = df.drop_duplicates()
    df = df.fillna(method='ffill').fillna(0)
    st.success("✅ Data cleaned — duplicates removed, nulls handled.")

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # --- User question section ---
    st.subheader("💬 Ask a question about your data")
    user_question = st.text_input("Type your question here (e.g., 'Show top 5 rows', 'Average salary')")

    # --- Voice input ---
    if st.button("🎙️ Speak your question"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎧 Listening... please speak clearly.")
            audio = recognizer.listen(source)
        try:
            user_question = recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: {user_question}")
        except Exception as e:
            st.error(f"Speech recognition error: {e}")

    if user_question:
        with st.spinner("🧠 Understanding your question and generating query..."):
            sql_query = generate_sql_query(user_question, df)
        st.code(sql_query, language="sql")

        # Execute query
        result = execute_query(sql_query, df)

        if not result.empty:
            st.success("✅ Query executed successfully!")
            st.dataframe(result)

            # --- Visualization Section ---
            st.subheader("📈 Visualization")

            # Automatically detect numeric columns for plotting
            numeric_cols = result.select_dtypes(include=['int64', 'float64']).columns
            non_numeric_cols = result.select_dtypes(exclude=['int64', 'float64']).columns

            if len(numeric_cols) >= 1 and len(non_numeric_cols) >= 1:
                x_col = st.selectbox("Choose X-axis (categorical)", non_numeric_cols)
                y_col = st.selectbox("Choose Y-axis (numeric)", numeric_cols)
                chart_type = st.selectbox("Select chart type", ["Bar", "Line", "Scatter", "Pie"])

                if chart_type == "Bar":
                    fig = px.bar(result, x=x_col, y=y_col, title=f"{chart_type} Chart of {y_col} vs {x_col}")
                elif chart_type == "Line":
                    fig = px.line(result, x=x_col, y=y_col, title=f"{chart_type} Chart of {y_col} vs {x_col}")
                elif chart_type == "Scatter":
                    fig = px.scatter(result, x=x_col, y=y_col, title=f"{chart_type} Plot of {y_col} vs {x_col}")
                elif chart_type == "Pie" and len(numeric_cols) > 0:
                    fig = px.pie(result, names=x_col, values=y_col, title=f"Pie Chart of {y_col} by {x_col}")
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("⚠️ Not enough numeric/categorical columns for visualization.")
        else:
            st.error("❌ No results or invalid query.")
else:
    st.warning("📥 Please upload a CSV to start.")
