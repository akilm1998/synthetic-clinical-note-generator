import pandas as pd


def verify_dataset(file_name: str):
    try:
        df = pd.read_parquet(file_name)
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        return 1

    print(df.shape)
    print("\n\n", df.head())
    print("\n\n", df.tail())
    is_na = df.isna().sum()
    if is_na.any():
        print("\nDataset contains missing values")
        return 1
    print("\n\n", is_na)
    if df["patient_id"].nunique() == len(df):
        print("\n\n", "Patient IDs are unique")
    else:
        print("\n\n", "Patient IDs are NOT unique")
        is_duplicated = df["patient_id"].duplicated(keep=False)
        # print just the dulicated rows
        print("\n\n", "Duplicated rows:")
        print("\n\n", df[is_duplicated])
        return 1

    # Get note count for each condition
    unique_conditions = df["diagnosis_name"].unique()
    count = 0
    for i in unique_conditions:
        print(f"{i} | {len(df[df['diagnosis_name'] == i])}")
        count += len(df[df["diagnosis_name"] == i])
    print(f"total notes: {count}")
    print("Success !!")
    return 0


if __name__ == "__main__":
    verify_dataset("clinical_notes.parquet")
