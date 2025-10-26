import plotly.express as px
import pandas as pd

def auto_visualize_from_df(df: pd.DataFrame):
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(exclude='number').columns.tolist()
    if df.shape[1] == 1:
        col = df.columns[0]
        if col in num_cols:
            fig = px.histogram(df, x=col, nbins=30, title=f'Distribution of {col}')
        else:
            fig = px.histogram(df, x=col, title=f'Distribution of {col}')
        return fig
    if len(cat_cols)>=1 and len(num_cols)>=1:
        fig = px.bar(df, x=cat_cols[0], y=num_cols[0], title=f'{num_cols[0]} by {cat_cols[0]}')
        return fig
    if len(num_cols)>=2:
        fig = px.scatter(df, x=num_cols[0], y=num_cols[1], title=f'{num_cols[1]} vs {num_cols[0]}')
        return fig
    fig = px.imshow(df.corr(), text_auto=True, title='Correlation matrix')
    return fig
