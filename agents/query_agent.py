import re
import pandas as pd
from pandasql import sqldf

# --- Function: Generate SQL query based on user question ---
def generate_sql_query(user_question: str, df: pd.DataFrame) -> str:
    """
    Converts simple natural language questions into SQL queries
    using rule-based pattern matching.
    """
    question = user_question.lower()

    # Default query
    sql_query = "SELECT * FROM data LIMIT 10;"

    if "count" in question:
        sql_query = "SELECT COUNT(*) FROM data;"
    elif "average" in question or "mean" in question:
        # Try to find numeric column
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            sql_query = f"SELECT AVG({numeric_cols[0]}) as average_{numeric_cols[0]} FROM data;"
    elif "max" in question or "highest" in question:
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            sql_query = f"SELECT MAX({numeric_cols[0]}) as max_{numeric_cols[0]} FROM data;"
    elif "min" in question or "lowest" in question:
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            sql_query = f"SELECT MIN({numeric_cols[0]}) as min_{numeric_cols[0]} FROM data;"
    elif "show" in question or "display" in question:
        sql_query = "SELECT * FROM data LIMIT 10;"
    elif "top" in question:
        limit = re.findall(r'\d+', question)
        limit = int(limit[0]) if limit else 5
        sql_query = f"SELECT * FROM data LIMIT {limit};"

    return sql_query


# --- Function: Execute SQL query safely ---
def execute_query(sql_query: str, df: pd.DataFrame):
    """
    Executes an SQL query against the dataframe using pandasql.
    """
    try:
        result = sqldf(sql_query, {"data": df})
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()
