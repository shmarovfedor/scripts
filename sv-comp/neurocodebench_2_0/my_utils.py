import pandas as pd


## adding extra columns into a dataframe
def add_extra_columns(df):
    # picking the filename and the subcategory from the filepath
    df["run_filename"] = df["run_name"].apply(lambda path : path.split("/")[-1])
    df["run_filename_clean"] = df["run_filename"].apply(lambda path : path.split(".")[0])
    df["run_subcategory"] = df["run_name"].apply(lambda path : path.split("/")[-2])
    return df

## tudying up the data
def tudy_up(df):
    # removing "s" from time values and turning them into float
    df["walltime"] = df["walltime"].apply(lambda time : float(time.replace("s", "")))
    df["cputime"] = df["cputime"].apply(lambda time : float(time.replace("s", "")))
    # removing "B" from memory values and turning them into int
    df["memory"] = df["memory"].apply(lambda mem : int(mem.replace("B", "")))
    return df

## creating a DataFrame from file, and adding the "data source" column
def load_df_from_file(filepath):
    df = pd.read_csv(filepath)
    df["data_source"] = filepath
    return df

def load_df_from_files(filepaths):
    df = pd.DataFrame()
    for filepath in filepaths:
        new_df = load_df_from_file(filepath)
        new_df = add_extra_columns(new_df)
        new_df = tudy_up(new_df)
        df = pd.concat([df, new_df], ignore_index = True)
    return df

def split_df_by_column(df, column):
    res = []
    for val in df[column].unique():
        res.append(df[df[column] == val])
    return res



