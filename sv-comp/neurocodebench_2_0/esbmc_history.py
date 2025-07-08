#!/usr/bin/env python3

import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.lines import Line2D
import math
from my_constants import *



## adding extra columns
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

def verdict_by_verifiers(df, verdict, tools):
    res = {}
    for run_name in df["run_name"].unique():
        df_run = df[df["run_name"] == run_name]
        number_of_verdicts = (df_run["category"] == verdict).sum()
        tool_names = df_run[df_run["category"] == verdict]["host"].unique()
        if (number_of_verdicts >= 1) and (set(tools).issubset(set(tool_names))):
            res[run_name] = tool_names
    return res

def verdict_by_n_verifiers(df, verdict, n):
    res = {}
    for run_name in df["run_name"].unique():
        df_run = df[df["run_name"] == run_name]
        number_of_verdicts = (df_run["category"] == verdict).sum()
        tool_names = df_run[df_run["category"] == verdict]["host"].unique()
        if number_of_verdicts == n:
            res[run_name] = tool_names
    return res


def plot_cputimes(filenames, df):
    i = 0
    for filename in filenames:
        cputime = df[df["run_filename_clean"] == filename]["cputime"]
        category = df[df["run_filename_clean"] == filename]["category"]
        reason = df[df["run_filename_clean"] == filename]["terminationreason"]
        marker = "^"
        color = "black"
        if (category == "wrong").prod():
            color = "red"
        if (reason == "cputime").prod():
            marker = "x"
        if (reason == "memory").prod():
            marker = "o"
        plt.scatter(i, cputime, color=color, marker=marker)
        i = i + 1
    #plt.title(str("Subcategory: " + subcategory))
    #plt.xlabel("Benchmark name")
    plt.ylabel("CPU time (s)")
    plt.xticks(range(0, len(filenames)), labels = filenames, rotation=90)
    plt.tight_layout()
    plt.ylim(-30, 950)
    #plt.xlim(-1, len(labels))
    plt.show()


def split_df_by_source(df):
    df_plain = df[(df["data_source"] == "plain_results/results.combined.merged.csv")][:]
    df_musl = df[(df["data_source"] == "musl_results/results.combined.merged.csv")][:]
    df_core = df[(df["data_source"] == "core_math_results/results.combined.merged.csv")][:]
    return (df_plain, df_musl, df_core)


## 
# for a given verifier get a dictionary with all the benchmark names split into
# the following verdicts:
#       correct_true: [],
#       correct_false: [],
#       incorrect_true: [],
#       incorrect_false: [],
#       unknown: [],
#       timeout: [],
#       out_of_memory: [],
#       other: []
def get_all_stats_for_verifier(df, tool):
    res = {}
    df = df[df["host"] == tool]
    res["correct_true"] = df[(df["category"] == "correct") & 
            (df["run_expectedVerdict"] == True)]["run_filename_clean"].to_list()

    res["correct_false"] = df[(df["category"] == "correct") & 
            (df["run_expectedVerdict"] == False)]["run_filename_clean"].to_list()
    
    res["incorrect_true"] = df[(df["category"] == "wrong") & 
            (df["run_expectedVerdict"] == False)]["run_filename_clean"].to_list()
    
    res["incorrect_false"] = df[(df["category"] == "wrong") & 
            (df["run_expectedVerdict"] == True)]["run_filename_clean"].to_list()
    
    res["unknown"] = df[df["category"] == "unknown"]["run_filename_clean"].to_list()
    
    res["timeout"] = df[(df["status"] == "TIMEOUT") | 
                (df["status"] == "TIMEOUT (ERROR - no output)")]["run_filename_clean"].to_list()

    res["out_of_memory"] = df[(df["status"] == "OUT OF MEMORY") | 
                (df["status"] == "OUT OF MEMORY (ERROR - no output)")]["run_filename_clean"].to_list()

    res["other"] = df[(df["category"] == "error") 
            & ~(df["status"] == "TIMEOUT")
            & ~(df["status"] == "TIMEOUT (ERROR - no output)")
            & ~(df["status"] == "OUT OF MEMORY")
            & ~(df["status"] == "OUT OF MEMORY (ERROR - no output)")]["run_filename_clean"].to_list()
    
    return res

def print_verifier_stats(stats):
    for key, value in stats.items():
        print(key, ":", len(value))


def print_stats_per_banchmark(df):
    for task in df["run_filename_clean"].unique():
        df_task = df[df["run_filename_clean"] == task]
        print(task)
        verdicts = df_task["category"].to_list()
        years = df_task["year"].astype(str).to_list()
        termination = df_task["terminationreason"].astype(str).to_list()
        expected = df_task["run_expectedVerdict"].astype(str).to_list()
        cputime = df_task["cputime"].astype(int).astype(str).to_list()
        print("\t".join(years))
        print("\t".join(verdicts))
        print("\t".join(termination))
        #print("\t".join(expected))
        print("\t".join(cputime))
        print("----------------------------------------")

def scatter_cputimes_by_year(df):
    i = 0
    for task in df["run_filename_clean"].unique():
        df_task = df[df["run_filename_clean"] == task]
        value_2019 = df_task[df_task["year"] == 2019]["cputime"]
        value_2020 = df_task[df_task["year"] == 2020]["cputime"]
        value_2021 = df_task[df_task["year"] == 2021]["cputime"]
        value_2022 = df_task[df_task["year"] == 2022]["cputime"]
        value_2023 = df_task[df_task["year"] == 2023]["cputime"]
        value_2024 = df_task[df_task["year"] == 2024]["cputime"]
       
        facecolor_2019 = "green"
        if df_task[df_task["year"] == 2019]["category"].unique() == "wrong":
            facecolor_2019 = "red"
        if df_task[df_task["year"] == 2019]["category"].unique() == "error":
            facecolor_2019 = "black"
        facecolor_2020 = "green"
        if df_task[df_task["year"] == 2020]["category"].unique() == "wrong":
            facecolor_2020 = "red"
        if df_task[df_task["year"] == 2020]["category"].unique() == "error":
            facecolor_2020 = "black"
        facecolor_2021 = "green"
        if df_task[df_task["year"] == 2021]["category"].unique() == "wrong":
            facecolor_2021 = "red"
        if df_task[df_task["year"] == 2021]["category"].unique() == "error":
            facecolor_2021 = "black"
        facecolor_2022 = "green"
        if df_task[df_task["year"] == 2022]["category"].unique() == "wrong":
            facecolor_2022 = "red"
        if df_task[df_task["year"] == 2022]["category"].unique() == "error":
            facecolor_2022 = "black"
        facecolor_2023 = "green"
        if df_task[df_task["year"] == 2023]["category"].unique() == "wrong":
            facecolor_2023 = "red"
        if df_task[df_task["year"] == 2023]["category"].unique() == "error":
            facecolor_2023 = "black"
        facecolor_2024 = "green"
        if df_task[df_task["year"] == 2024]["category"].unique() == "wrong":
            facecolor_2024 = "red"
        if df_task[df_task["year"] == 2024]["category"].unique() == "error":
            facecolor_2024 = "black"
        
        plt.scatter(i + 0, value_2019, marker="^", facecolor=facecolor_2019)
        plt.scatter(i + 5, value_2020, marker="v", facecolor=facecolor_2020)
        plt.scatter(i + 10, value_2021, marker="s", facecolor=facecolor_2021)
        plt.scatter(i + 15, value_2022, marker="+", facecolor=facecolor_2022)
        plt.scatter(i + 20, value_2023, marker="x", facecolor=facecolor_2023)
        plt.scatter(i + 25, value_2024, marker="o", facecolor=facecolor_2024)
        i = i + 35

    filenames = df["run_filename_clean"].unique()
    i = 0
    ticks = []
    for file in filenames:
        ticks.append(i * 35 + 15)
        i = i + 1
    plt.xticks(ticks, labels = filenames, rotation=90)
    plt.subplots_adjust(left=0.05, bottom=0.3, right=0.99, 
        top=0.95, wspace=0.15, hspace=0.5)
    #plt.tight_layout()
    plt.show()



## main()

df = pd.DataFrame()

for arg in sys.argv[1:]:
    new_df = load_df_from_file(arg)
    new_df = add_extra_columns(new_df)
    new_df = tudy_up(new_df)
    df = pd.concat([df, new_df], ignore_index = True)


source_list = df["data_source"].to_list()
year_list = []
for source in source_list:
    year_list.append(int(source[19:23]))

df["year"] = year_list

# exclude ESBMC 2024
#df = df[~(df["year"] == 2024)]

print("Overall CPU time: ", df["cputime"].sum())



correct_true = []
correct_false = []
incorrect_true = []
incorrect_false = []
for year in df["year"].unique():
    df_year = df[df["year"] == year]
    #correct_true.append(len(df_year[(df_year["category"] == "correct") & (df_year["run_expectedVerdict"] == True)]))
    #correct_false.append(len(df_year[(df_year["category"] == "correct") & (df_year["run_expectedVerdict"] == False)]))
    #incorrect_true.append(len(df_year[(df_year["category"] == "wrong") & (df_year["run_expectedVerdict"] == False)]))
    #incorrect_false.append(len(df_year[(df_year["category"] == "wrong") & (df_year["run_expectedVerdict"] == True)]))
    #print(year)
    res = get_all_stats_for_verifier(df_year, "esbmc")
    print("Year: ", year)
    for key in res:
        print(key, ":", len(res[key]))
    print("--------------------")

exit()
    

years = df["year"].unique()

plt.fill_between([2023.5, 2025.5], -50, 400, color="lightgray", label="_nolegend_")
plt.text(2023.5, 250, "v1.0 release", rotation=90, fontsize = 20)
plt.plot(years, correct_true, lw = 2, marker = "s")
plt.plot(years, correct_false, lw = 2, marker = "s")
plt.plot(years, incorrect_true, lw = 2, marker = "s")
plt.plot(years, incorrect_false, lw = 2, marker = "s")
plt.legend(["correct true", "correct false", "incorrect true", "incorrect false"], fontsize = 14)
plt.xticks(fontsize = 16)
plt.xlabel("Year", fontsize = 18)
plt.yticks(fontsize = 16)
plt.ylabel("# benchmarks", fontsize = 18)
plt.xlim([2017.5, 2025.5])
plt.ylim([-20, 370])
plt.grid()
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, 
#        top=0.95, wspace=0.2, hspace=0.7)
plt.show()


df_2025 = df[df["year"] == 2025]
print(df_2025[df_2025["category"] == "wrong"]["run_filename_clean"].unique())


# only benchmarks with math functions
#df = df[df["run_filename_clean"].isin(BENCHMARKS_WITH_MATH)]

# only benchmarks without math functions
#df = df[~(df["run_filename_clean"].isin(BENCHMARKS_WITH_MATH))]


changed = []
for task in df["run_filename_clean"].unique():
    df_task = df[df["run_filename_clean"] == task]
    subcategory = df_task["run_subcategory"].unique()[0]
    if len(df_task["category"].unique()) > 1:
        changed.append(task)

#print("WHAT CHANGED (", len(changed), " benchmarks)")
#df_changed = df[df["run_filename_clean"].isin(changed)]
#print_stats_per_banchmark(df_changed)
#scatter_cputimes_by_year(df_changed)

#print("WHAT DID NOT CHANGE")
#df_unchanged = df[~(df["run_filename_clean"].isin(changed))]
#print_stats_per_banchmark(df_unchanged)

exit()

df_unchanged_and_verdict = df_unchanged[~(df_unchanged["category"] == "error")]
print("CPU time change")
#print_stats_per_banchmark(df_unchanged_and_verdict)

df_safe = df_unchanged_and_verdict[df_unchanged_and_verdict["run_filename_clean"].str.contains("_safe")]
print_stats_per_banchmark(df_safe)
scatter_cputimes_by_year(df_safe)

df_unsafe = df_unchanged_and_verdict[df_unchanged_and_verdict["run_filename_clean"].str.contains("_unsafe")]
print_stats_per_banchmark(df_unsafe)
scatter_cputimes_by_year(df_unsafe)
