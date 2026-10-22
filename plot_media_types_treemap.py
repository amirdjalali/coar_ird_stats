import pandas as pd
import plotly.express as px

def plot_media_types_treemap(df):
    categories = (
        df["media_types"].dropna().str.split("|").explode().tolist()
    )
    cats = pd.DataFrame({"category": categories})
    cats["category"] = cats["category"].replace({"conference papers": "conference-papers",
                                                     "research articles": "research-articles",
                                                     "phd theses": "theses",
                                                     "theses\n": "theses",
                                                     "software\n": "software",
                                                     "contributions to books": "books"})
    counts = (
            cats.groupby("category")
            .size()
            .reset_index(name="count")
    )
  
    print(counts)
    fig = px.treemap(counts, 
                     path=["category"], 
                     values="count",
                     color="category",
                     color_discrete_map={"other": "lightgrey"}
    )
    return fig


if __name__ == "__main__":
    df = pd.read_csv("ird_it_with_coordinates_iris.csv", encoding="utf-8")
    df_not_archived = df[(df["record_status"] != "archived") & (~df["is_iris"])]
    media_types = plot_media_types_treemap(df_not_archived)
    with open("media_types.html", "w") as f:
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

        f.write(f"<h1>Media types per repository attivi non IRIS</h1>")
        f.write(media_types.to_html(full_html=False, include_plotlyjs="cdn"))