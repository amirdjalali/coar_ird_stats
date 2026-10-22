import pandas as pd
import plotly.express as px

def plot_timeline(df):
    for c in ["roar_date", "roar_lastmod"]:
        df[c] = pd.to_datetime(df[c], errors="coerce", utc=True).dt.tz_convert(None)
    df = df[df["roar_date"].notna()]
    today = pd.Timestamp.today().normalize()
    archived = df["record_status"] == "archived"
    df["end"] = df["roar_lastmod"].where(archived, today).fillna(today)
    df = df.sort_values(["owner_name", "roar_date"])
    df["row"] = df["owner_name"] + "  |  " + df["name"]
    df["color_key"] = df["owner_name"].where(df["record_status"] != "archived", "archived")
    fig = px.timeline(
        df,
        x_start="roar_date",
        x_end="end",
        y="row",
        color="color_key",
        color_discrete_map={"archived": "#b8b8b8"},   # others use the default palette
        hover_data=["software", "record_status", "homepage"],
        category_orders={"row": df["row"].tolist()},  # keep the owner grouping
    )
    fig.update_yaxes(autorange="reversed", title=None)
    fig.update_traces(width=0.5)          # slimmer bars, closer to "lines"
    fig.update_layout(showlegend=False, height=max(500, 22 * len(df)))
    return fig

if __name__ == "__main__":
    systems = pd.read_csv("systems_roar.csv", encoding="utf-8")
    plot_timeline(systems)
