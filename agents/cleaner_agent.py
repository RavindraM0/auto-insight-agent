import pandas as pd
from dateutil.parser import parse

def try_parse_date(series):
    try:
        return pd.to_datetime(series, errors='coerce', infer_datetime_format=True)
    except Exception:
        return series

def clean_data(df: pd.DataFrame):
    corrections = []
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before != after:
        corrections.append(f'Dropped {before-after} duplicate rows.')

    for col in df.columns:
        if df[col].dtype == 'object':
            parsed = try_parse_date(df[col])
            if parsed.dtype == 'datetime64[ns]':
                df[col] = parsed
                corrections.append(f"Column '{col}' converted to datetime.")
                continue
            coerced = pd.to_numeric(df[col], errors='coerce')
            non_na = coerced.notna().sum()
            if non_na / max(1, len(coerced)) > 0.6:
                df[col] = coerced
                corrections.append(f"Column '{col}' converted to numeric where possible.")

    for col in df.columns:
        nulls = df[col].isnull().sum()
        if nulls == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            med = df[col].median()
            df[col] = df[col].fillna(med)
            corrections.append(f"Filled {nulls} nulls in numeric column '{col}' with median ({med}).")
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].fillna(method='ffill').fillna(df[col].median() if df[col].dropna().shape[0]>0 else pd.NaT)
            corrections.append(f"Filled {nulls} nulls in datetime column '{col}' with forward-fill/median.")
        else:
            try:
                mode = df[col].mode()[0]
                df[col] = df[col].fillna(mode)
                corrections.append(f"Filled {nulls} nulls in column '{col}' with mode ('{mode}').")
            except Exception:
                df[col] = df[col].fillna('Unknown')
                corrections.append(f"Filled {nulls} nulls in column '{col}' with 'Unknown'.")
    return df, corrections
