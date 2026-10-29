import pandas as pd
import plotly.express as px

DEFAULT_IRIS_COLOR = "#e4572e"
OTHER_COLOR = "#1f77b4"
NOT_ACTIVE_COLOR = "lightgrey"
ACTIVE_COLOR = "grey"
TOTAL_COLOR = "white"
SENZA_IRIS = "#2c97e4"
CON_IRIS = "#49b3ff"

def plot_sunburst(totali, attivi, verificati):
    
    data = {
        'labels':  ['Totali', 'Attivi', 'Archiviati', 'Verificati',   'Da confermare'],
        'parents': ['',       'Totali', 'Totali',     'Attivi',       'Attivi'],
        'values': [totali, attivi, totali - attivi, verificati, attivi - verificati]
    }

    df = pd.DataFrame(data)

    fig = px.sunburst(df,
                      names='labels',      # <-- era 'labels='
                      parents='parents',
                      values='values',
                      color='labels',
                      color_discrete_map={
                            "Totali": TOTAL_COLOR,
                            "Attivi": ACTIVE_COLOR,
                            "Archiviati": NOT_ACTIVE_COLOR,
                            "IRIS": DEFAULT_IRIS_COLOR,
                            "Non IRIS": OTHER_COLOR,
                            "Senza IRIS": SENZA_IRIS,
                            "Con IRIS": CON_IRIS
                      })


    fig.update_traces(
        branchvalues='total',
        texttemplate='<b>%{label}</b><br>%{value}',
        insidetextorientation='horizontal',
        textfont=dict(size=14),
    )
    return fig

if __name__ == "__main__":
    plot_sunburst(totali=174, attivi=138, attivi_iris=79, con_iris=30).show()