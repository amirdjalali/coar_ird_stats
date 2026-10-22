import pandas as pd
import json

def add_roar_dates(df, dates):
    for idx, row in df.iterrows():
        ids_string = row["other_registry_identifiers"]
        print(ids_string)
        ids = ids_string.split("|") if ids_string else []
        for id in ids:
            roar_id = id.replace("roar:", "") if "roar:" in id else None
        if roar_id:
            df.loc[idx,"roar_date"] = dates.get(roar_id, {}).get("date", "roar id not found!")
            df.loc[idx,"roar_datestamp"] = dates.get(roar_id, {}).get("datestamp", "roar id not found!")
            df.loc[idx,"roar_status_changed"] = dates.get(roar_id, {}).get("status_changed", "roar id not found!")
            df.loc[idx,"roar_lastmod"] = dates.get(roar_id, {}).get("lastmod", "roar id not found!")
    return df

def extract_dates(roar):
    dates = {}
    for record in roar:
        id = str(record["eprintid"])
        dates[id] = {
            "date": record["date"],
            "datestamp": record["datestamp"],
            "status_changed": record["status_changed"],
            "lastmod": record["lastmod"]
        }
    return dates

if __name__ == "__main__":
    df = pd.read_csv("systems.csv", encoding="utf-8", keep_default_na=False)
    with open("ROAR/ROAR_record_IT.json", 'r', encoding="utf-8") as f:
        roar = json.load(f)
    dates = extract_dates(roar)
    print(dates)
    df_with_roar_dates = add_roar_dates(df,dates)
    df_with_roar_dates.to_csv("systems_roar.csv")