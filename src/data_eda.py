import pandas as pd

if __name__ == "__main__":
    data_file = "./../data/investopedia.csv"

    df = pd.read_csv(data_file)

    print("Shape of data: ", df.shape)

    print("Counting Words:")
    # create word count for all texts
    df["word_count"] = df["Text"].apply(lambda x: len(x.split()))

    print("Data Sample:")
    print(df.head())

    print("\n")

    print("Null Values:")
    print(df.isna().sum())

    print("Word Counts:")
    print(df["word_count"].value_counts(normalize=True))
