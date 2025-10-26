import re
import duckdb
import pandas as pd
import threading
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
except Exception:
    AutoTokenizer = None
    AutoModelForSeq2SeqLM = None
    pipeline = None

# Lazy model loader
_lock = threading.Lock()
_pipe = None

def _get_pipe():
    global _pipe
    with _lock:
        if _pipe is None:
            model_name = 'google/flan-t5-base'  # change to flan-t5-small if size is an issue
            if pipeline is None:
                raise RuntimeError('transformers not available. Install requirements.')
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            _pipe = pipeline('text2text-generation', model=model, tokenizer=tokenizer, device=0 if False else -1)
        return _pipe

def nl_to_sql(nl_query: str, df: pd.DataFrame) -> str:
    q = nl_query.lower()
    # Rule-based quick match
    m = re.search(r'(total|sum|count|average|avg|mean)\s+(?P<metric>\w+)\s+by\s+(?P<group>\w+)(?:\s+(?:for|in)\s+(?P<year>\d{4}))?', q)
    if m:
        metric = m.group('metric')
        group = m.group('group')
        year = m.group('year')
        if metric == 'count':
            metric_expr = 'COUNT(*) as count'
        elif 'avg' in m.group(1) or 'mean' in m.group(1):
            metric_expr = f'AVG({metric}) as avg_{metric}'
        else:
            metric_expr = f'SUM({metric}) as total_{metric}'
        where = ''
        year_col = None
        for c in df.columns:
            if 'year' in c.lower() or 'date' in c.lower():
                year_col = c
                break
        if year and year_col:
            where = f"WHERE EXTRACT(year FROM {year_col}) = {year}"
        sql = f"SELECT {group}, {metric_expr} FROM df {where} GROUP BY {group} ORDER BY 2 DESC"
        return sql

    # Use model
    try:
        pipe = _get_pipe()
        prompt = f"Convert this natural language request into a DuckDB SQL query on a table named 'df'.\nRequest: {nl_query}\nOnly output SQL."
        out = pipe(prompt, max_length=256, do_sample=False)[0]['generated_text']
        out = out.strip().strip('`').strip()
        if not out.lower().startswith('select'):
            found = re.search(r'(select[\s\S]+)', out, flags=re.IGNORECASE)
            if found:
                out = found.group(1)
        return out
    except Exception:
        return "SELECT * FROM df LIMIT 200"

def execute_sql(sql: str, df: pd.DataFrame) -> pd.DataFrame:
    con = duckdb.connect(':memory:')
    con.register('df', df)
    try:
        res = con.execute(sql).df()
    finally:
        con.close()
    return res
