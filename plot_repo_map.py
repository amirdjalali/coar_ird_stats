import plotly.express as px
import pandas as pd

DEFAULT_IRIS_COLOR = "#e4572e"
OTHER_COLOR = "#1f77b4"

def plot_repo_map(df, color=None):

    default_color = color or OTHER_COLOR

    counts = (
        df.groupby(["lat", "lon", "is_iris"])
        .agg(
            count=("name", "size"),
            names=("name", lambda s: "<br>".join(s.dropna().astype(str))),
        )
        .reset_index()
    )
    # total records per category (not number of map points)
    totals = df["is_iris"].value_counts()
    n_iris = int(totals.get(True, 0))
    n_other = int(totals.get(False, 0))

    iris_label = f"IRIS ({n_iris})"
    other_label = f"Other ({n_other})"

    # readable legend labels instead of True/False
    counts["type"] = counts["is_iris"].map({True: iris_label, False: other_label})

    fig = px.scatter_map(
        counts,
        lat="lat",
        lon="lon",
        size="count",
        size_max=40,
        color="type",
        opacity=0.7,
        color_discrete_map={iris_label: DEFAULT_IRIS_COLOR, other_label: default_color},
        category_orders={"type": [iris_label, other_label]},   # last = drawn on top
        hover_data={"count": True, "type": True, "names": True, "lat": False, "lon": False},
        center=dict(lat=counts.lat.mean(), lon=counts.lon.mean()),
        zoom=5,
    )
    fig.update_layout(map_style="carto-positron")   # light, minimal (great for data overlays)
    # other options:
    # "carto-darkmatter"  dark minimal
    # "white-bg"          blank white background, no tiles at all
    # "open-street-map"   what you're using now
    if color:
        fig.update_layout(showlegend=False)

    return fig

def plot_repo_map_repo_type(df):
    counts = (
        df.groupby(["lat", "lon", "repository_type"])
          .agg(
              count=("name", "size"),
              names=("name", lambda s: "<br>".join(s.dropna().astype(str))),
          )
          .reset_index()
    )

    # total records per repository type -> legend label "Type (N)"
    totals = df["repository_type"].value_counts()
    counts["type_label"] = counts["repository_type"].map(
        lambda t: f"{t} ({totals[t]})"
    )

    # legend sorted from most to least frequent
    order = [f"{t} ({n})" for t, n in totals.items()]

    fig = px.scatter_map(
        counts,
        lat="lat",
        lon="lon",
        size="count",
        size_max=40,
        color="type_label",
        category_orders={"type_label": order},
        opacity=0.7,
        hover_data={"count": True, "type_label": True, "names": True,
                    "repository_type": False, "lat": False, "lon": False},
        labels={"type_label": "repository_type"},   # hover/legend title
        center=dict(lat=counts.lat.mean(), lon=counts.lon.mean()),
        zoom=5,
    )
    fig.update_layout(map_style="carto-positron")

    return fig

def plot_data_repos(df):
    df["data_repo"] = df["media_types"].str.contains("research-data", regex=False, na=False)

    counts = (
        df.groupby(["lat", "lon", "data_repo"])
          .agg(
              count=("name", "size"),
              names=("name", lambda s: "<br>".join(s.dropna().astype(str))),
          )
          .reset_index()
    )

    # total records per category -> legend labels with counts
    n_data = int(df["data_repo"].sum())
    n_other = int((~df["data_repo"]).sum())

    data_label = f"Research data ({n_data})"
    other_label = f"Other ({n_other})"

    counts["type"] = counts["data_repo"].map({True: data_label, False: other_label})

    fig = px.scatter_map(
        counts,
        lat="lat",
        lon="lon",
        size="count",
        size_max=40,
        color="type",
        category_orders={"type": [data_label, other_label]},   # last = drawn on top
        opacity=0.7,
        hover_data={"count": True, "type": True, "names": True,
                    "data_repo": False, "lat": False, "lon": False},
        center=dict(lat=counts.lat.mean(), lon=counts.lon.mean()),
        zoom=5,
    )
    fig.update_layout(map_style="carto-positron")

    return fig

if __name__ == "__main__":
    df = pd.read_csv("ird_it_with_coordinates_iris.csv", encoding="utf-8")
    df = df[df["lat"] != -1]
    
    df_not_archived = df[(df["record_status"] != "archived")]
    not_archived = plot_repo_map(df_not_archived)
    repo_type_map = plot_repo_map_repo_type(df_not_archived)
    data_repos = plot_data_repos(df_not_archived)

    df_archived = df[(df["record_status"] == "archived")]
    archived = plot_repo_map(df_archived, color="grey")


    with open("maps.html", "w") as f:
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

        f.write(f"<h1>Tipi di Repository (attivi)</h1>")
        f.write(repo_type_map.to_html(full_html=False, include_plotlyjs="cdn"))

        f.write(f"<h1>Repository dati (attivi)</h1>")
        f.write(data_repos.to_html(full_html=False, include_plotlyjs="cdn"))

        f.write("</body></html>")