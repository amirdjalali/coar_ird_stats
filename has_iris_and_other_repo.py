import pandas as pd

# make a dataframe of institutions that have iris
# for those that have iris, list the other repos

def list_iris_institutions(df):
    institutions_with_iris = df[df['is_iris'] == True][['owner_name', 'owner_ror']].drop_duplicates()

    return institutions_with_iris

def list_non_iris_repos_from_iris_institutions(df):
    institutions_with_iris = list_iris_institutions(df)
    non_iris_repos = df[df['is_iris'] == False].merge(
        institutions_with_iris, 
        on=['owner_name', 'owner_ror'], 
        how='inner'
    )

    # Filter out any records that somehow have is_iris=True
    non_iris_repos = non_iris_repos[non_iris_repos['is_iris'] == False]

    return non_iris_repos

def list_non_iris_institutions(df):
    # institutions that do not have iris
    institutions_of_the_non_iris = df[df['is_iris'] == False][['owner_name', 'owner_ror']].drop_duplicates()
    iris_institutions = list_iris_institutions(df)
    non_iris_institutions = (
        institutions_of_the_non_iris.merge(iris_institutions, how='left', indicator=True)
        .query('_merge == "left_only"')
        .drop(columns='_merge')
        .dropna()
        .reset_index(drop=True)
    )

    return non_iris_institutions

def print_non_iris(iris_true_df, iris_false_df):

    unique_ror_count = iris_false_df['owner_ror'].nunique()

    for idx, row in iris_true_df.iterrows():
        institution = row['owner_name']
        
        # Get all records for this institution from iris_false_df
        records = iris_false_df[iris_false_df['owner_name'] == institution]
        if len(records) > 0:
            print(f"\nInstitution: {institution}")
            print("=" * 50)

        for rec_idx, rec_row in records.iterrows():
            print(f"  Name: {rec_row['name']}")
            print(f"  URL: {rec_row['homepage']}")
            print(f"  software: {rec_row['software']}")
            print("-" * 50)

    return f"""
        Ci sono {len(iris_true_df)} istituzioni con IRIS.<br/>
        Di queste, {unique_ror_count} hanno almeno un'altra repository.<br/>
        In totale, ci sono {len(iris_false_df)} repository non IRIS, gestite da di istituzioni che hanno un IRIS.
    """

if __name__ == "__main__":
    df = pd.read_csv("ird_it_with_coordinates_iris.csv", encoding="utf-8")
    institutions_with_iris = list_iris_institutions(df)
    non_iris_repos = list_non_iris_repos_from_iris_institutions(df)
    non_iris_institutions = list_non_iris_institutions(df)
    print(non_iris_institutions)
    print(institutions_with_iris, non_iris_repos)
