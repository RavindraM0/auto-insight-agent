from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

def autonomous_analysis(df: pd.DataFrame, max_steps: int = 6):
    report = []
    report.append(f'Dataset rows: {df.shape[0]}, columns: {df.shape[1]}')
    num = df.select_dtypes(include='number')
    if num.shape[1] > 0:
        variances = num.var().sort_values(ascending=False)
        top = variances.index[0]
        report.append(f'Highest variance numeric column: {top} (variance={variances.iloc[0]:.2f})')
        date_cols = [c for c in df.columns if 'date' in c.lower()]
        if date_cols:
            d = date_cols[0]
            try:
                s = df.sort_values(d)
                start = s.iloc[:max(10, int(len(s)/10))][top].mean()
                end = s.iloc[-max(10, int(len(s)/10)):][top].mean()
                if np.isfinite(start) and np.isfinite(end):
                    change = (end - start) / (abs(start) + 1e-9)
                    report.append(f'{top} changed by {change*100:.1f}% over timeline.')
            except Exception:
                pass
        try:
            iso = IsolationForest(random_state=42, n_estimators=50)
            clean = num.dropna()
            if clean.shape[0] > 10:
                iso.fit(clean)
                preds = iso.predict(clean)
                outlier_pct = (preds == -1).sum() / len(preds) * 100
                report.append(f'Approx {outlier_pct:.1f}% numeric rows flagged as outliers.')
        except Exception:
            pass
    try:
        corr = num.corr().abs()
        if corr.shape[0] > 1:
            tri = corr.where(~pd.np.eye(corr.shape[0],dtype=bool))
            top_pair = tri.stack().idxmax()
            report.append(f'Strongest correlation between {top_pair[0]} and {top_pair[1]} (r={corr.loc[top_pair]:.2f}).')
    except Exception:
        pass
    report.append('Suggested next questions:')
    report.append(' - Show total sales by region')
    report.append(' - Show top 5 customers by revenue')
    report.append(' - Show revenue time-series')
    return report
