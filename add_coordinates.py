import pandas as pd
import requests

def get_coordinates(ror):
    if ror != "":
        print(f"Getting coodinates from ror.org for {ror}")

        url = (
            f"https://api.ror.org/v2/organizations/{ror}"
        )
        response = requests.get(url)
        lat = response.json().get("locations")[0]["geonames_details"]["lat"]
        lon = response.json()["locations"][0]["geonames_details"]["lng"]

        print(f"Found coordinates! {lat}, {lon}")
    else:
        lat = -1
        lon = -1
    return lat, lon

def enrich_with_coordinates(df):
    lat_list = []
    lon_list = []
    for ror_url in df["owner_ror"]:
        ror = ror_url.replace("https://ror.org/", "").strip()
        lat, lon = get_coordinates(ror)
        lat_list.append(lat)
        lon_list.append(lon)
    df["lat"] = lat_list
    df["lon"] = lon_list
    return df

if __name__ == "__main__":
    filename = "systems_italy"
    records = pd.read_csv(f"{filename}.csv", encoding="utf-8", keep_default_na=False)
    records_updated = enrich_with_coordinates(records)
    records_updated.to_csv(f"{filename}_with_coordinates.csv", encoding="utf-8")



