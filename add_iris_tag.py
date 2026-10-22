import pandas as pd

ird_filename = "ird_it_with_coordinates"

iris_installations = pd.read_csv("iris_installazioni.csv", encoding="utf-8")
coar_ird = pd.read_csv(f"{ird_filename}.csv", encoding="utf-8")
iris_installations["url"] = (
    iris_installations["url"]
    .str.replace("https://", "")
    .str.replace("http://", "")
    .str.replace("www.", "")
    .str.rstrip("/")
    .str.strip()
)

coar_ird["homepage"] = (
    coar_ird["homepage"]
    .str.replace("https://", "")
    .str.replace("http://", "")
    .str.replace("www.", "")
    .str.rstrip("/")
    .str.strip()
)

coar_ird["is_iris"] = coar_ird["homepage"].isin(iris_installations["url"])
iris_installations["in_coar"] = iris_installations["url"].isin(coar_ird["homepage"])
print(coar_ird[coar_ird["is_iris"]].count())

coar_ird.to_csv(f"{ird_filename}_iris.csv", encoding="utf-8")
iris_installations.to_csv(f"iris_installations_enriched.csv", encoding="utf-8")


