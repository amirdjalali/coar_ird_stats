from plot_media_types_treemap import plot_media_types_treemap
from plot_repo_map import plot_repo_map, plot_data_repos, plot_repo_map_repo_type
from plot_software_treemap import plot_software_treemap
from plot_timeline import plot_timeline

import pandas as pd

df = pd.read_csv("ird_it_with_coordinates_iris.csv", encoding="utf-8")
df = df[df["lat"] != -1]

df_not_archived = df[(df["record_status"] != "archived")]
not_archived = plot_repo_map(df_not_archived)
repo_type_map = plot_repo_map_repo_type(df_not_archived)
data_repos = plot_data_repos(df_not_archived)

df_archived = df[(df["record_status"] == "archived")]
archived = plot_repo_map(df_archived, color="grey")

df_active_not_iris = df[(df["record_status"] != "archived") & (~df["is_iris"])]
active_not_iris_treemap = plot_software_treemap(df_active_not_iris, "software")

media_types = plot_media_types_treemap(df_not_archived)

with open("dashboard.html", "w") as f:
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

    f.write(f"<h1>Software - Repository attivi non IRIS</h1>")
    f.write(active_not_iris_treemap.to_html(full_html=False, include_plotlyjs="cdn"))

    f.write(f"<h1>Media types per repository attivi non IRIS</h1>")
    f.write(media_types.to_html(full_html=False, include_plotlyjs="cdn"))

    systems = pd.read_csv("systems_roar.csv", encoding="utf-8")
    timeline= plot_timeline(systems)

    f.write(f"<h1>Linea del tempo (per ora solo con dati ROAR)</h1>")
    f.write(timeline.to_html(full_html=False, include_plotlyjs="cdn"))

    f.write("</body></html>")