#!/usr/bin/env python3

import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.lines import Line2D
import math



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

#    legend = [
#            Line2D([0], [0], marker='^', color="white", markerfacecolor='black', label='correct', markersize=9),
#            Line2D([0], [0], marker='v', color="white", markerfacecolor='black', label='incorrect', markersize=9),
#            Line2D([0], [0], marker='x', color="white", markeredgecolor='black', label='timeout', markersize=7),
#            Line2D([0], [0], marker='+', color="white", markeredgecolor='black', label='out of memory', markersize=7),
#            Line2D([0], [0], marker='s', color="white", markerfacecolor='black', label='Plain', markersize=9),
#            Line2D([0], [0], marker='s', color="white", markerfacecolor='red', label='MUSL', markersize=9),
#            Line2D([0], [0], marker='s', color="white", markerfacecolor='blue', label='CORE_MATH', markersize=9),
#            ]

    #plt.title(str("Subcategory: " + subcategory))
    #plt.xlabel("Benchmark name")
    plt.ylabel("CPU time (s)")
    plt.xticks(range(0, len(filenames)), labels = filenames, rotation=90)
    plt.tight_layout()
    plt.ylim(-30, 950)
    #plt.xlim(-1, len(labels))
    #plt.legend(handles=legend)
    plt.show()




## main()

df = pd.DataFrame()

for arg in sys.argv[1:]:
    new_df = load_df_from_file(arg)
    new_df = add_extra_columns(new_df)
    new_df = tudy_up(new_df)
    df = pd.concat([df, new_df], ignore_index = True)

#print(df["data_source"].unique())

# looking at time distributions to reach true/false verdicts
df_core = df[(df["data_source"] == "core_math_results/results.combined.merged.csv")][:]
df_musl = df[(df["data_source"] == "musl_results/results.combined.merged.csv")][:]
df_plain = df[(df["data_source"] == "plain_results/results.combined.merged.csv")][:]

df_esbmc = df_plain[df_plain["host"] == "cbmc"]
sat_relu = df_esbmc[df_esbmc["run_subcategory"] == "sat_relu"]
sat_relu_safe = sat_relu[sat_relu["run_filename_clean"].str.contains("_safe")] 
sat_relu_unsafe = sat_relu[sat_relu["run_filename_clean"].str.contains("_unsafe")] 

sat_relu_safe_ordered = ["prop_bool_v5_c5_safe", "prop_bool_v5_c10_safe", "prop_bool_v5_c15_safe", "prop_bool_v5_c20_safe", "prop_bool_v5_c25_safe", "prop_bool_v5_c30_safe", "prop_bool_v8_c8_safe", "prop_bool_v8_c16_safe", "prop_bool_v8_c24_safe", "prop_bool_v8_c32_safe", "prop_bool_v8_c40_safe", "prop_bool_v8_c48_safe", "prop_bool_v13_c13_safe", "prop_bool_v13_c26_safe", "prop_bool_v13_c39_safe", "prop_bool_v13_c52_safe", "prop_bool_v13_c65_safe", "prop_bool_v13_c78_safe", "prop_bool_v21_c21_safe", "prop_bool_v21_c42_safe", "prop_bool_v21_c63_safe", "prop_bool_v21_c84_safe", "prop_bool_v21_c105_safe", "prop_bool_v21_c126_safe", "prop_bool_v34_c34_safe", "prop_bool_v34_c68_safe", "prop_bool_v34_c102_safe", "prop_bool_v34_c136_safe", "prop_bool_v34_c170_safe", "prop_bool_v34_c204_safe", "prop_bool_v55_c55_safe", "prop_bool_v55_c110_safe", "prop_bool_v55_c165_safe", "prop_bool_v55_c220_safe", "prop_bool_v55_c275_safe", "prop_bool_v55_c330_safe", "prop_bool_v89_c89_safe", "prop_bool_v89_c178_safe", "prop_bool_v89_c267_safe", "prop_bool_v89_c356_safe", "prop_bool_v89_c445_safe", "prop_bool_v89_c534_safe", "prop_bool_v144_c144_safe", "prop_bool_v144_c288_safe", "prop_bool_v144_c432_safe", "prop_bool_v144_c576_safe", "prop_bool_v144_c720_safe", "prop_bool_v144_c864_safe"]

sat_relu_unsafe_ordered = ["prop_bool_v5_c5_unsafe", "prop_bool_v5_c10_unsafe", "prop_bool_v5_c15_unsafe", "prop_bool_v5_c18_unsafe", "prop_bool_v5_c24_unsafe", "prop_bool_v5_c27_unsafe", "prop_bool_v8_c8_unsafe", "prop_bool_v8_c16_unsafe", "prop_bool_v8_c24_unsafe", "prop_bool_v8_c32_unsafe", "prop_bool_v8_c40_unsafe", "prop_bool_v8_c46_unsafe", "prop_bool_v13_c13_unsafe", "prop_bool_v13_c26_unsafe", "prop_bool_v13_c39_unsafe", "prop_bool_v13_c52_unsafe", "prop_bool_v13_c65_unsafe", "prop_bool_v13_c78_unsafe", "prop_bool_v21_c21_unsafe", "prop_bool_v21_c42_unsafe", "prop_bool_v21_c62_unsafe", "prop_bool_v21_c84_unsafe", "prop_bool_v21_c105_unsafe", "prop_bool_v21_c126_unsafe", "prop_bool_v34_c34_unsafe", "prop_bool_v34_c68_unsafe", "prop_bool_v34_c102_unsafe", "prop_bool_v34_c136_unsafe", "prop_bool_v34_c170_unsafe", "prop_bool_v34_c204_unsafe", "prop_bool_v55_c55_unsafe", "prop_bool_v55_c110_unsafe", "prop_bool_v55_c165_unsafe", "prop_bool_v55_c220_unsafe", "prop_bool_v55_c275_unsafe", "prop_bool_v55_c330_unsafe", "prop_bool_v89_c89_unsafe", "prop_bool_v89_c178_unsafe", "prop_bool_v89_c267_unsafe", "prop_bool_v89_c356_unsafe", "prop_bool_v89_c445_unsafe", "prop_bool_v89_c534_unsafe", "prop_bool_v144_c144_unsafe", "prop_bool_v144_c288_unsafe", "prop_bool_v144_c432_unsafe", "prop_bool_v144_c576_unsafe", "prop_bool_v144_c720_unsafe", "prop_bool_v144_c864_unsafe"]

plot_cputimes(sat_relu_safe_ordered, sat_relu_safe)
plot_cputimes(sat_relu_unsafe_ordered, sat_relu_unsafe)

poly_approx = df_esbmc[df_esbmc["run_subcategory"] == "poly_approx"]
poly_approx_safe = poly_approx[poly_approx["run_filename_clean"].str.contains("_safe")] 
poly_approx_unsafe = poly_approx[poly_approx["run_filename_clean"].str.contains("_unsafe")] 

poly_approx_safe_ordered = ["poly_128_thresh_0_safe","poly_128_thresh_1_safe","poly_128_thresh_2_safe","poly_256_thresh_0_safe","poly_256_thresh_1_safe","poly_256_thresh_2_safe","poly_512_thresh_0_safe","poly_512_thresh_1_safe","poly_512_thresh_2_safe","poly_1024_thresh_0_safe","poly_1024_thresh_1_safe","poly_1024_thresh_2_safe","poly_16_16_thresh_0_safe","poly_16_16_thresh_1_safe","poly_16_16_thresh_2_safe","poly_32_32_thresh_0_safe","poly_32_32_thresh_1_safe","poly_32_32_thresh_2_safe","poly_64_64_thresh_0_safe","poly_64_64_thresh_1_safe","poly_64_64_thresh_2_safe","poly_128_128_thresh_0_safe","poly_128_128_thresh_1_safe","poly_128_128_thresh_2_safe","poly_8_8_8_thresh_0_safe","poly_8_8_8_thresh_1_safe","poly_8_8_8_thresh_2_safe","poly_16_16_16_thresh_0_safe","poly_16_16_16_thresh_1_safe","poly_16_16_16_thresh_2_safe","poly_32_32_32_thresh_0_safe","poly_32_32_32_thresh_1_safe","poly_32_32_32_thresh_2_safe","poly_64_64_64_thresh_0_safe","poly_64_64_64_thresh_1_safe","poly_64_64_64_thresh_2_safe","poly_4_4_4_4_thresh_0_safe","poly_4_4_4_4_thresh_1_safe","poly_4_4_4_4_thresh_2_safe","poly_8_8_8_8_thresh_0_safe","poly_8_8_8_8_thresh_1_safe","poly_8_8_8_8_thresh_2_safe","poly_16_16_16_16_thresh_0_safe","poly_16_16_16_16_thresh_1_safe","poly_16_16_16_16_thresh_2_safe","poly_32_32_32_32_thresh_0_safe","poly_32_32_32_32_thresh_1_safe","poly_32_32_32_32_thresh_2_safe"]


poly_approx_unsafe_ordered = ["poly_128_thresh_3_unsafe","poly_128_thresh_4_unsafe","poly_128_thresh_5_unsafe","poly_256_thresh_3_unsafe","poly_256_thresh_4_unsafe","poly_256_thresh_5_unsafe","poly_512_thresh_3_unsafe","poly_512_thresh_4_unsafe","poly_512_thresh_5_unsafe","poly_1024_thresh_3_unsafe","poly_1024_thresh_4_unsafe","poly_1024_thresh_5_unsafe","poly_16_16_thresh_3_unsafe","poly_16_16_thresh_4_unsafe","poly_16_16_thresh_5_unsafe","poly_32_32_thresh_3_unsafe","poly_32_32_thresh_4_unsafe","poly_32_32_thresh_5_unsafe","poly_64_64_thresh_3_unsafe","poly_64_64_thresh_4_unsafe","poly_64_64_thresh_5_unsafe","poly_128_128_thresh_3_unsafe","poly_128_128_thresh_4_unsafe","poly_128_128_thresh_5_unsafe","poly_8_8_8_thresh_3_unsafe","poly_8_8_8_thresh_4_unsafe","poly_8_8_8_thresh_5_unsafe","poly_16_16_16_thresh_3_unsafe","poly_16_16_16_thresh_4_unsafe","poly_16_16_16_thresh_5_unsafe","poly_32_32_32_thresh_3_unsafe","poly_32_32_32_thresh_4_unsafe","poly_32_32_32_thresh_5_unsafe","poly_64_64_64_thresh_3_unsafe","poly_64_64_64_thresh_4_unsafe","poly_64_64_64_thresh_5_unsafe","poly_4_4_4_4_thresh_3_unsafe","poly_4_4_4_4_thresh_4_unsafe","poly_4_4_4_4_thresh_5_unsafe","poly_8_8_8_8_thresh_3_unsafe","poly_8_8_8_8_thresh_4_unsafe","poly_8_8_8_8_thresh_5_unsafe","poly_16_16_16_16_thresh_3_unsafe","poly_16_16_16_16_thresh_4_unsafe","poly_16_16_16_16_thresh_5_unsafe","poly_32_32_32_32_thresh_3_unsafe","poly_32_32_32_32_thresh_4_unsafe","poly_32_32_32_32_thresh_5_unsafe"]

plot_cputimes(poly_approx_safe_ordered, poly_approx_safe)
plot_cputimes(poly_approx_unsafe_ordered, poly_approx_unsafe)


hopfield_nets = df_esbmc[df_esbmc["run_subcategory"] == "hopfield_nets"]
hopfield_nets_safe = hopfield_nets[hopfield_nets["run_filename_clean"].str.contains("_safe")]
hopfield_nets_unsafe = hopfield_nets[hopfield_nets["run_filename_clean"].str.contains("_unsafe")]

hopfield_nets_safe_ordered = ["softsign_w4_r1_case_1_safe","softsign_w4_r2_case_0_safe","softsign_w4_r3_case_0_safe","softsign_w4_r4_case_0_safe","softsign_w8_r1_case_1_safe","softsign_w8_r2_case_0_safe","softsign_w8_r3_case_0_safe","softsign_w8_r4_case_0_safe","softsign_w16_r1_case_1_safe","softsign_w16_r2_case_0_safe","softsign_w16_r3_case_0_safe","softsign_w16_r4_case_0_safe","softsign_w32_r1_case_1_safe","softsign_w32_r2_case_0_safe","softsign_w32_r3_case_0_safe","softsign_w32_r4_case_0_safe","softsign_w64_r1_case_1_safe","softsign_w64_r2_case_0_safe","softsign_w64_r3_case_0_safe","softsign_w64_r4_case_0_safe","tanh_w4_r1_case_1_safe","tanh_w4_r2_case_0_safe","tanh_w4_r3_case_0_safe","tanh_w4_r4_case_0_safe","tanh_w8_r1_case_1_safe","tanh_w8_r2_case_0_safe","tanh_w8_r3_case_0_safe","tanh_w8_r4_case_0_safe","tanh_w16_r1_case_1_safe","tanh_w16_r2_case_0_safe","tanh_w16_r3_case_0_safe","tanh_w16_r3_case_1_safe","tanh_w16_r4_case_0_safe","tanh_w16_r4_case_1_safe","tanh_w32_r1_case_1_safe","tanh_w32_r2_case_0_safe","tanh_w32_r3_case_0_safe","tanh_w32_r3_case_1_safe","tanh_w32_r4_case_0_safe","tanh_w32_r4_case_1_safe","tanh_w64_r1_case_1_safe","tanh_w64_r2_case_0_safe","tanh_w64_r3_case_0_safe","tanh_w64_r3_case_1_safe","tanh_w64_r4_case_0_safe","tanh_w64_r4_case_1_safe"]

hopfield_nets_unsafe_ordered = ["softsign_w4_r1_case_0_unsafe","softsign_w4_r2_case_1_unsafe","softsign_w4_r3_case_1_unsafe","softsign_w4_r4_case_1_unsafe","softsign_w8_r1_case_0_unsafe","softsign_w8_r2_case_1_unsafe","softsign_w8_r3_case_1_unsafe","softsign_w8_r4_case_1_unsafe","softsign_w16_r1_case_0_unsafe","softsign_w16_r2_case_1_unsafe","softsign_w16_r3_case_1_unsafe","softsign_w16_r4_case_1_unsafe","softsign_w32_r1_case_0_unsafe","softsign_w32_r2_case_1_unsafe","softsign_w32_r3_case_1_unsafe","softsign_w32_r4_case_1_unsafe","softsign_w64_r1_case_0_unsafe","softsign_w64_r2_case_1_unsafe","softsign_w64_r3_case_1_unsafe","softsign_w64_r4_case_1_unsafe","tanh_w4_r1_case_0_unsafe","tanh_w4_r2_case_1_unsafe","tanh_w4_r3_case_1_unsafe","tanh_w4_r4_case_1_unsafe","tanh_w8_r1_case_0_unsafe","tanh_w8_r2_case_1_unsafe","tanh_w8_r3_case_1_unsafe","tanh_w8_r4_case_1_unsafe","tanh_w16_r1_case_0_unsafe","tanh_w16_r2_case_1_unsafe","tanh_w32_r1_case_0_unsafe","tanh_w32_r2_case_1_unsafe","tanh_w64_r1_case_0_unsafe","tanh_w64_r2_case_1_unsafe"]

plot_cputimes(hopfield_nets_safe_ordered, hopfield_nets_safe)
plot_cputimes(hopfield_nets_unsafe_ordered, hopfield_nets_unsafe)


lipschitz_bounded = df_esbmc[df_esbmc["run_subcategory"] == "lipschitz_bounded"]
#lipschitz_bounded_safe = lipschitz_bounded[lipschitz_bounded["run_filename_clean"].str.contains("_safe")]
#lipschitz_bounded_unsafe = lipschitz_bounded[lipschitz_bounded["run_filename_clean"].str.contains("_unsafe")]

lipschitz_bounded_ordered = ["sll_2x4x4x1_case_0_unsafe","sll_2x4x4x1_case_1_unsafe","sll_2x4x4x1_case_2_unsafe","sll_2x4x4x1_case_3_safe","sll_2x4x4x1_case_4_safe","sll_2x4x4x1_case_5_safe","sll_3x4x4x1_case_0_unsafe","sll_3x4x4x1_case_1_unsafe","sll_3x4x4x1_case_2_unsafe","sll_3x4x4x1_case_3_safe","sll_3x4x4x1_case_4_safe","sll_3x4x4x1_case_5_safe","sll_4x4x4x1_case_0_unsafe","sll_4x4x4x1_case_1_unsafe","sll_4x4x4x1_case_2_unsafe","sll_4x4x4x1_case_3_safe","sll_4x4x4x1_case_4_safe","sll_4x4x4x1_case_5_safe","sll_2x8x8x1_case_0_unsafe","sll_2x8x8x1_case_1_unsafe","sll_2x8x8x1_case_2_unsafe","sll_2x8x8x1_case_3_safe","sll_2x8x8x1_case_4_safe","sll_2x8x8x1_case_5_safe","sll_3x8x8x1_case_0_unsafe","sll_3x8x8x1_case_1_unsafe","sll_3x8x8x1_case_2_unsafe","sll_3x8x8x1_case_3_safe","sll_3x8x8x1_case_4_safe","sll_3x8x8x1_case_5_safe","sll_4x8x8x1_case_0_unsafe","sll_4x8x8x1_case_1_unsafe","sll_4x8x8x1_case_2_unsafe","sll_4x8x8x1_case_3_safe","sll_4x8x8x1_case_4_safe","sll_4x8x8x1_case_5_safe","sll_2x12x12x1_case_0_unsafe","sll_2x12x12x1_case_1_unsafe","sll_2x12x12x1_case_2_unsafe","sll_2x12x12x1_case_3_safe","sll_2x12x12x1_case_4_safe","sll_2x12x12x1_case_5_safe","sll_3x12x12x1_case_0_unsafe","sll_3x12x12x1_case_1_unsafe","sll_3x12x12x1_case_2_unsafe","sll_3x12x12x1_case_3_safe","sll_3x12x12x1_case_4_safe","sll_3x12x12x1_case_5_safe","sll_4x12x12x1_case_0_unsafe","sll_4x12x12x1_case_1_unsafe","sll_4x12x12x1_case_2_unsafe","sll_4x12x12x1_case_3_safe","sll_4x12x12x1_case_4_safe","sll_4x12x12x1_case_5_safe","sll_2x16x16x1_case_0_unsafe","sll_2x16x16x1_case_1_unsafe","sll_2x16x16x1_case_2_unsafe","sll_2x16x16x1_case_3_safe","sll_2x16x16x1_case_4_safe","sll_2x16x16x1_case_5_safe","sll_3x16x16x1_case_0_unsafe","sll_3x16x16x1_case_1_unsafe","sll_3x16x16x1_case_2_unsafe","sll_3x16x16x1_case_3_safe","sll_3x16x16x1_case_4_safe","sll_3x16x16x1_case_5_safe","sll_4x16x16x1_case_0_unsafe","sll_4x16x16x1_case_1_unsafe","sll_4x16x16x1_case_2_unsafe","sll_4x16x16x1_case_3_safe","sll_4x16x16x1_case_4_safe","sll_4x16x16x1_case_5_safe","sll_2x20x20x1_case_0_unsafe","sll_2x20x20x1_case_1_unsafe","sll_2x20x20x1_case_2_unsafe","sll_2x20x20x1_case_3_safe","sll_2x20x20x1_case_4_safe","sll_2x20x20x1_case_5_safe","sll_3x20x20x1_case_0_unsafe","sll_3x20x20x1_case_1_unsafe","sll_3x20x20x1_case_2_unsafe","sll_3x20x20x1_case_3_safe","sll_3x20x20x1_case_4_safe","sll_3x20x20x1_case_5_safe","sll_4x20x20x1_case_0_unsafe","sll_4x20x20x1_case_1_unsafe","sll_4x20x20x1_case_2_unsafe","sll_4x20x20x1_case_3_safe","sll_4x20x20x1_case_4_safe","sll_4x20x20x1_case_5_safe","sll_2x24x24x1_case_0_unsafe","sll_2x24x24x1_case_1_unsafe","sll_2x24x24x1_case_2_unsafe","sll_2x24x24x1_case_3_safe","sll_2x24x24x1_case_4_safe","sll_2x24x24x1_case_5_safe","sll_3x24x24x1_case_0_unsafe","sll_3x24x24x1_case_1_unsafe","sll_3x24x24x1_case_2_unsafe","sll_3x24x24x1_case_3_safe","sll_3x24x24x1_case_4_safe","sll_3x24x24x1_case_5_safe","sll_4x24x24x1_case_0_unsafe","sll_4x24x24x1_case_1_unsafe","sll_4x24x24x1_case_2_unsafe","sll_4x24x24x1_case_3_safe","sll_4x24x24x1_case_4_safe","sll_4x24x24x1_case_5_safe"]

plot_cputimes(lipschitz_bounded_ordered, lipschitz_bounded)



exit()

df_core_verdicts = df_core[(df_core["category"] == "correct") | (df_core["category"] == "wrong")][:]
df_musl_verdicts = df_musl[(df_musl["category"] == "correct") | (df_musl["category"] == "wrong")][:]
df_plain_verdicts = df_plain[(df_plain["category"] == "correct") | (df_plain["category"] == "wrong")][:]

df_plain_2ls = df_plain[df_plain["host"] == "2ls"]
df_plain_2ls = df_plain_2ls[df_plain_2ls["category"] == "correct"]

df_plain_divine = df_plain[df_plain["host"] == "divine"]
df_plain_divine = df_plain_divine[df_plain_divine["category"] == "correct"]

df_plain_uautomizer = df_plain[df_plain["host"] == "uautomizer"]
df_plain_uautomizer = df_plain_uautomizer[df_plain_uautomizer["category"] == "correct"]

print(df_plain["host"].unique())

tools = ['2ls' 'cbmc' 'cpachecker' 'divine' 'esbmc' 'pesco' 'pinaka' 'uautomizer']
all_correct_name = []
for run_name in df_plain["run_name"].unique():
    df_run = df_plain[df_plain["run_name"] == run_name]
    are_all_correct = (df_run["category"] == "correct").prod()
    if are_all_correct:
        all_correct_name.append(run_name)

for run_name in df_plain["run_name"].unique():
    df_run = df_plain[df_plain["run_name"] == run_name]
    number_of_correct = (df_run["category"] == "correct").sum()
    tool_names = df_run[df_run["category"] == "correct"]["host"].unique()
    if number_of_correct >= 8:
        print(run_name, ": correctly solved by ", len(tool_names), "tools: ", tool_names)

df_plain = df_musl
cpa_plain_correct = df_plain[(df_plain["host"] == "cpachecker") & (df_plain["category"] == "correct")]
cpa_plain_wrong = df_plain[(df_plain["host"] == "cpachecker") & (df_plain["category"] == "wrong")]
#print(cpa_plain_correct["run_name"].unique())
#print()
#print(cpa_plain_wrong["run_name"].unique())

esbmc_wrong = df_plain[(df_plain["host"] == "esbmc") & (df_plain["category"] == "wrong")]
print(esbmc_wrong["run_filename_clean"].to_list())


exit()


# just to check whether termination reason "cputime" means a TIMEOUT
# and "memory" means OUT OF MEMORY

df_correct = df[(df["category"] == "correct")]
df_correct_true = df_correct[(df_correct["run_expectedVerdict"] == True)]
df_correct_false = df_correct[(df_correct["run_expectedVerdict"] == False)]
df_wrong = df[(df["category"] == "wrong")]
df_wrong_true = df_wrong[(df_wrong["run_expectedVerdict"] == True)]
df_wrong_false = df_wrong[(df_wrong["run_expectedVerdict"] == False)]
df_timeout = df[(df["terminationreason"] == "cputime")]
df_oom = df[(df["terminationreason"] == "memory")]


## Generating a Figure "verdicts per benchmark"
df_verdict = pd.concat([df_correct, df_wrong, df_timeout, df_oom], axis = 0)
#df_verdict_timeout_oom = pd.concat([df_correct, df_wrong, df_timeout, df_oom], axis = 0)

#print(df["run_subcategory"].unique())
#print(df_verdict)



# only final verdicts and timeouts
#df_verdict_and_timeout
