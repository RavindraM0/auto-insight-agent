import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

def save_dashboard_html(df: pd.DataFrame, out_path='dashboard.html'):
    html = ['<html><head><meta charset="utf-8"><title>Auto Dashboard</title></head><body>']
    html.append('<h1>Auto-Generated Dashboard</h1>')
    html.append('<h2>Data preview</h2>')
    html.append(df.head(30).to_html(index=False))
    G = nx.Graph()
    cols = df.columns.tolist()
    for c in cols:
        G.add_node(c)
    for i,a in enumerate(cols):
        for b in cols[i+1:]:
            if len(set(a.lower().split('_')) & set(b.lower().split('_'))) > 0:
                G.add_edge(a,b)
    net = Network(height='400px', width='100%')
    net.from_nx(G)
    tmp = 'graph.html'
    net.show(tmp)
    if os.path.exists(tmp):
        with open(tmp,'r',encoding='utf-8') as f:
            graph_html = f.read()
        html.append('<h2>Inferred Column Graph</h2>')
        html.append(graph_html)
    html.append('</body></html>')
    with open(out_path,'w',encoding='utf-8') as f:
        f.write('\n'.join(html))
    return out_path
