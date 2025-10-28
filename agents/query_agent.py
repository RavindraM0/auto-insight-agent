import re
import pandas as pd
from pandasql import sqldf

# ✅ Safely executes the query using pandasql
def execute_query(query: str, df: pd.DataFrame):
    try:
        result = sqldf(query, {"data": df})
        return result
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

# ✅ Generates multiple relevant SQL queries
def generate_sql_queries(user_question: str, df: pd.DataFrame):
    question = user_question.lower()
    columns = [col.lower() for col in df.columns]
    queries = []

    # --- General Queries ---
    if "first" in question or "show" in question and "rows" in question:
        queries.append("SELECT * FROM data LIMIT 10;")

    if "count" in question and "job" in question:
        queries.append("SELECT COUNT(*) AS total_jobs FROM data;")

    if "average" in question or "avg" in question:
        for col in columns:
            if "salary" in col:
                queries.append(f"SELECT AVG({col}) AS avg_salary FROM data;")

    if "top" in question or "highest" in question:
        for col in columns:
            if "salary" in col:
                queries.append(f"SELECT * FROM data ORDER BY {col} DESC LIMIT 10;")

    if "remote" in question:
        if any("job" in col for col in columns):
            queries.append("SELECT * FROM data WHERE job_type LIKE '%remote%';")

    if "location" in question or "city" in question:
        for col in columns:
            if "location" in col:
                queries.append(f"SELECT {col}, COUNT(*) AS total_jobs FROM data GROUP BY {col} ORDER BY total_jobs DESC LIMIT 5;")

    if "company" in question:
        for col in columns:
            if "company" in col:
                queries.append(f"SELECT {col}, COUNT(*) AS total_jobs FROM data GROUP BY {col} ORDER BY total_jobs DESC LIMIT 5;")

    # --- Fallback: just show preview ---
    if not queries:
        queries.append("SELECT * FROM data LIMIT 10;")

    return queries
