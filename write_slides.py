from plot_exploded_treemaps import plot_media_types_treemap, plot_sources_treemap
from plot_repo_map import plot_repo_map, plot_data_repos, plot_repo_map_repo_type
from plot_software_treemap import plot_software_treemap
from plot_timeline import plot_timeline
from has_iris_and_other_repo import list_non_iris_repos_from_iris_institutions, print_non_iris, list_iris_institutions, list_non_iris_institutions
from plot_sunburst import plot_sunburst

import pandas as pd
from pathlib import Path
from plotly.offline import get_plotlyjs

def df_to_html(df, max_height="60vh"):
    table = df.to_html(
        index=False,
        border=0,
        classes="tbl",
        justify="left",       # header cells flush left (pandas default is right)
        na_rep="",
        escape=True,
        float_format=lambda x: f"{x:,.2f}",
    )
    return f'<div class="tbl-wrap" style="max-height:{max_height}">{table}</div>'

FILENAME = "systems_italy_with_coordinates_iris.csv"

TABLE_CSS = """
            :root {
            --border: #d1d5db; --head-bg: #f3f4f6; --row-alt: #f9fafb;
            --hover: #eef2ff;  --cell-fg: #1d2430;
            }
            @media (prefers-color-scheme: dark) {
            :root { --border:#3a424f; --head-bg:#1a1f27; --row-alt:#14181e;
                    --hover:#1e2a44;  --cell-fg:#e8ecf1; }
            }

            .tbl-wrap { overflow: auto; border: 1px solid var(--border); border-radius: 8px; }

            .tbl {
            border-collapse: separate; border-spacing: 0;   /* keeps borders on sticky header */
            width: 100%; font-size: .95rem; color: var(--cell-fg);
            }
            .tbl th, .tbl td {
            padding: .55rem .9rem; text-align: left; white-space: nowrap;
            border-right: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            }
            .tbl th:last-child, .tbl td:last-child { border-right: 0; }
            .tbl tbody tr:last-child td { border-bottom: 0; }

            .tbl thead th {
            position: sticky; top: 0; z-index: 1;
            background: var(--head-bg);
            font-weight: 600;
            border-bottom: 2px solid var(--border);
            }
            .tbl tbody tr:nth-child(even) { background: var(--row-alt); }
            .tbl tbody tr:hover { background: var(--hover); }
            """

def build_page(sections, path="report.html", title="Report", extra_css=""):
    """
    sections: list of (heading, text, content)
      content can be:
        - a Plotly figure          -> interactive chart
        - a pandas DataFrame       -> table (uses df_to_html)
        - a str                    -> raw HTML, inserted as is
        - None                     -> text only
    extra_css: additional CSS, e.g. TABLE_CSS for tables
    """
    blocks = []
    plotly_loaded = False   # load Plotly.js once, on the first figure

    has_table = False 
    has_plotly = False          

    for i, (heading, text, content) in enumerate(sections):
        kind = "empty"
        inner = ""

        if content is None:
            pass
        elif isinstance(content, str):
            kind, inner = "html", content
        elif isinstance(content, pd.DataFrame):
            kind, inner = "html", df_to_html(content, max_height="100%")
            has_table = True
        elif hasattr(content, "to_html"):   # Plotly figure
            kind = "chart"
            content.update_layout(margin=dict(t=10, l=10, r=10, b=10))
            has_plotly = True
            inner = content.to_html(
                full_html=False,
                include_plotlyjs=False,          # library is embedded once in <head>
                config={"responsive": True, "displayModeBar": False},
                default_height="100%",
            )
        else:
            raise TypeError(f"Unsupported content in section {i}: {type(content)}")

        blocks.append(f"""
        <section id="s{i}">
          <div class="text"><h2>{heading}</h2><p>{text}</p></div>
          <div class="content {kind}">{inner}</div>
        </section>""")

    dots = "".join(f'<a href="#s{i}" aria-label="Section {i+1}"></a>' for i in range(len(sections)))

    if has_table:                          # <-- new
        extra_css = TABLE_CSS + extra_css

    plotly_script = f"<script>{get_plotlyjs()}</script>" if has_plotly else ""

    html = f"""<!doctype html>
                <html lang="it">
                <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>{title}</title>
                <style>
                :root {{ --bg:#fff; --fg:#1d2430; --muted:#6b7280; --accent:#2563eb; }}
                @media (prefers-color-scheme: dark) {{
                    :root {{ --bg:#111418; --fg:#e8ecf1; --muted:#9aa4b2; --accent:#60a5fa; }}
                }}
                * {{ box-sizing: border-box; }}
                html {{ scroll-snap-type: y mandatory; scroll-behavior: smooth; }}
                body {{ margin:0; background:var(--bg); color:var(--fg);
                        font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
                section {{
                    height: 100vh; height: 100dvh;
                    scroll-snap-align: start; scroll-snap-stop: always;
                    display: grid; grid-template-columns: 1fr 2fr; gap: 2rem;
                    align-items: center; padding: 4rem 6vw;
                }}
                .text h2 {{ font-size: clamp(1.6rem, 3vw, 2.6rem); margin: 0 0 .75rem; }}
                .text p  {{ color: var(--muted); font-size: 1.1rem; line-height: 1.5; }}
                .content {{ height: 100%; min-height: 0; }}
                .content.html  {{ overflow: auto; display: flex; flex-direction: column; justify-content: center; }}
                .content.html img, .content.html iframe {{ max-width: 100%; }}
                nav {{ position: fixed; right: 1.25rem; top: 50%; transform: translateY(-50%);
                        display: flex; flex-direction: column; gap: .75rem; }}
                nav a {{ width: .7rem; height: .7rem; border-radius: 50%;
                        background: var(--muted); opacity: .4; transition: .2s; }}
                nav a.active {{ background: var(--accent); opacity: 1; transform: scale(1.4); }}
                @media (max-width: 800px) {{
                    section {{ grid-template-columns: 1fr; grid-template-rows: auto 1fr; padding: 2rem 1.25rem; }}
                }}
                {extra_css}
                </style>
                {plotly_script}
                </head>
                <body>
                {''.join(blocks)}
                <nav>{dots}</nav>
                <script>
                const links = document.querySelectorAll('nav a');
                const io = new IntersectionObserver(entries => {{
                    entries.forEach(e => {{
                    if (e.isIntersecting)
                        links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
                    }});
                }}, {{ threshold: 0.6 }});
                document.querySelectorAll('section').forEach(s => io.observe(s));
                </script>
                </body>
                </html>"""
    Path(path).write_text(html, encoding="utf-8")

df = pd.read_csv(FILENAME, encoding="utf-8", keep_default_na=False)
df_systems = pd.read_csv(FILENAME, encoding="utf-8", keep_default_na=False)
everything = len(df_systems)
sources_treemap = plot_sources_treemap(df_systems)
df = df[df["lat"] != -1]

df_not_archived = df[(df["record_status"] != "archived")]
df_active_iris = df[(df["record_status"] != "archived") & (df["is_iris"])]
df_active_not_iris = df[(df["record_status"] != "archived") & (~df["is_iris"])]
not_archived = plot_repo_map(df_not_archived)
repo_type_map = plot_repo_map_repo_type(df_active_not_iris)
data_repos = plot_data_repos(df_active_not_iris)

df_archived = df[(df["record_status"] == "archived")]
archived = plot_repo_map(df_archived, color="grey")

df_active_under_review = df[(df["record_status"] != "archived") & (df["record_status"] == "under_review")]
df_active_verified = df[(df["record_status"] != "archived") & (df["record_status"] == "verified")]

totali = len(df)
attivi = len(df_not_archived)
archiviati = len(df_archived)
under_review = len(df_active_under_review)
verificati = len(df_active_verified)
totals = plot_sunburst(totali=totali, attivi=attivi, verificati=verificati)

non_iris = len(df_active_not_iris)

software_treemap = plot_software_treemap(df_active_not_iris, "software")
subject_treemap = plot_software_treemap(df_active_not_iris, "primary_subject")

media_types = plot_media_types_treemap(df_not_archived)

non_iris_repos = list_non_iris_repos_from_iris_institutions(df_not_archived)
institutions_with_iris = list_iris_institutions(df_not_archived)
non_iris_institutions = plot_software_treemap(non_iris_repos, "owner_name")
institutions_with_no_iris = list_non_iris_institutions(df_not_archived)
non_iris_institutions_repo_types = plot_software_treemap(non_iris_repos, "repository_type")
software_treemap_non_iris_repos = plot_software_treemap(non_iris_repos, "software")
subject_treemap_non_iris_repos = plot_software_treemap(non_iris_repos, "primary_subject")
media_types_non_iris_repos = plot_media_types_treemap(non_iris_repos)

build_page([
    ("COAR IRD Italia", "Data sources", sources_treemap),
    ("COAR IRD Italia",
        f"""Su {totali} repository analizzati, {attivi} sono stati confermati e {archiviati} sono stati archiviati.
        {under_review} repository sono in attesa di conferma.""", 
        totals),
    ("Repository archiviati", 
     f"Sono stati archiviati {archiviati} repository (siti non più attivi o migrati, o contenuti ad accesso riservato)",
     df_archived[["name", "homepage", "owner_name"]]),
    ("Repository in attesa di conferma",
     f"{under_review} repository sono in attesa di conferma (interfaccia OAI-PMH non linkata o non accessibile).",
     df_active_under_review[["name", "homepage", "owner_name"]]),
    ("Repository confermati o under review", f"Su {len(df_not_archived)}, {len(df_active_iris)} sono IRIS", not_archived),
    ("Repository confermati o under review, non IRIS", f"Tipi di repository, totale {non_iris}.", repo_type_map),
    ("Repository confermati o under review, non IRIS", f"Repository con media_type 'research_data', totale {non_iris}.", data_repos),
    ("Repository confermati o under review, non IRIS", f"Software, totale {non_iris}.", software_treemap),
    ("Repository confermati o under review, non IRIS", f"Soggetti, totale {non_iris}.", subject_treemap),
    ("Repository confermati o under review, non IRIS", f"Media types, totale ({non_iris} repository)", media_types),
    #("Repository non IRIS di istituzioni con Iris", print_non_iris(institutions_with_iris, non_iris_repos), non_iris_institutions),
    #("Istituzioni senza IRIS", f"Ci sono {len(institutions_with_no_iris)} istituzioni che hanno almeno un repository, ma che non hanno IRIS", institutions_with_no_iris)
])