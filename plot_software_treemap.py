import plotly.express as px
import pandas as pd

def plot_software_treemap(df, path):
    counts = (
            df.groupby(path)
            .size()
            .reset_index(name="count")
    )
    fig = px.treemap(counts, 
                     path=[path], 
                     values="count",
                     color=path,
                     color_discrete_map={"_unknown": "lightgrey"}
    )
    return fig

def plot_iris_treemap(df):
    grouped = (
        df.groupby()
    )

if __name__ == "__main__":
    df = pd.read_csv("ird_it_with_coordinates_iris.csv", encoding="utf-8")
    
    df_not_archived = df[df["record_status"] != "archived"]
    not_archived = plot_software_treemap(df_not_archived, "software")

    df_archived = df[(df["record_status"] == "archived")]
    archived = plot_software_treemap(df_archived, "software")

    df_active_not_iris = df[(df["record_status"] != "archived") & (~df["is_iris"])]
    active_not_iris = plot_software_treemap(df_active_not_iris, "software")

    with open("software.html", "w") as f:
        f.write("""
                <html>
                <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        background-color: #f9f9f9;
                    }
                    h1 {
                        font-size: 2em;
                        color: #333;
                        border-bottom: 2px solid #ccc;
                        padding-bottom: 10px;
                        margin-top: 40px;
                    }
                    h2 {
                        font-size: 1.5em;
                        color: #555;
                        margin-top: 30px;
                    }
                </style>
                </head>
                <body>
                """)

        f.write(f"<h1>Repository attivi</h1>")
        f.write(not_archived.to_html(full_html=False, include_plotlyjs="cdn"))

        f.write(f"<h1>Repository non più attivi</h1>")
        f.write(archived.to_html(full_html=False, include_plotlyjs="cdn"))

        f.write(f"<h1>Repository attivi non IRIS</h1>")
        f.write(active_not_iris.to_html(full_html=False, include_plotlyjs="cdn"))

        f.write("</body></html>")