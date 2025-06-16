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
from my_utils import *




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
        memory = df[df["run_filename_clean"] == filename]["memory"]
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
        #plt.scatter(i, cputime, color=color, marker=marker, s=160)
        plt.scatter(i, memory, color=color, marker=marker, s=160)
        i = i + 1
    #plt.title(str("Subcategory: " + subcategory))
    plt.xlabel("Benchmark name", fontsize=22)
    #plt.ylabel("CPU time (s)", fontsize=22)
    plt.ylabel("Memory (B)", fontsize=22)
    plt.xticks(range(0, len(filenames)), labels = filenames, rotation=90, fontsize=16)
    plt.yticks(fontsize=16)
    #plt.tight_layout()
    #plt.ylim(-1e6, df[df["run_filename_clean"] == filename]["memory"].max() * 1.05)
    #plt.ylim(-30, df[df["run_filename_clean"] == filename]["memory"].max() * 1.05)
    plt.gca().set_ylim(bottom=0)
    plt.xlim(-1, len(df))
    #plt.xlim(-1, len(labels))
    plt.subplots_adjust(left=0.05, bottom=0.55, right=0.99, 
        top=0.95, wspace=0.15, hspace=0.5)
    plt.grid()
    plt.show()


def plot_verdicts_per_tool(df, verdicts, tools):
    return 0

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



#plt.bar(x_axis, correct_true.values(), width = 1, label = "correct true", edgecolor = "black")
#for i, value in enumerate(correct_true.values()):
#    plt.text(x_axis[i], value + 10, str(value), ha='center', rotation=90, fontsize=7)


## main()

df = load_df_from_files(sys.argv[1:])

# only benchmarks with math functions
#df = df[df["run_filename_clean"].isin(BENCHMARKS_WITH_MATH)]

# only benchmarks without math functions
#df = df[~(df["run_filename_clean"].isin(BENCHMARKS_WITH_MATH))]

# looking at time distributions to reach true/false verdicts
(df_plain, df_musl, df_core) = split_df_by_source(df)


i = 0
j = 1
for tool in df["host"].unique():
    stats_plain = get_all_stats_for_verifier(df_plain, tool)
    stats_musl = get_all_stats_for_verifier(df_musl, tool)
    stats_core = get_all_stats_for_verifier(df_core, tool)

    plt.subplot(4, 2, j)

    text_font_size = 11

    # correct true
    value = len(stats_plain["correct_true"])
    plt.bar(i + 0, value, width = 1, edgecolor = "black", facecolor = "red")
    plt.text(i + 0, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_musl["correct_true"])
    plt.bar(i + 1, value, width = 1, edgecolor = "black", facecolor = "blue")
    plt.text(i + 1, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_core["correct_true"])
    plt.bar(i + 2, value, width = 1, edgecolor = "black", facecolor = "green")
    plt.text(i + 2, value + 2, str(value), ha='center', fontsize=text_font_size)
    
    # correct false
    value = len(stats_plain["correct_false"])
    plt.bar(i + 3.5, value, width = 1, edgecolor = "black", facecolor = "red")
    plt.text(i + 3.5, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_musl["correct_false"])
    plt.bar(i + 4.5, value, width = 1, edgecolor = "black", facecolor = "blue")
    plt.text(i + 4.5, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_core["correct_false"])
    plt.bar(i + 5.5, value, width = 1, edgecolor = "black", facecolor = "green")
    plt.text(i + 5.5, value + 2, str(value), ha='center', fontsize=text_font_size)
   
    # incorrect true
    value = len(stats_plain["incorrect_true"])
    plt.bar(i + 7, value, width = 1, edgecolor = "black", facecolor = "red")
    plt.text(i + 7, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_musl["incorrect_true"])
    plt.bar(i + 8, value, width = 1, edgecolor = "black", facecolor = "blue")
    plt.text(i + 8, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_core["incorrect_true"])
    plt.bar(i + 9, value, width = 1, edgecolor = "black", facecolor = "green")
    plt.text(i + 9, value + 2, str(value), ha='center', fontsize=text_font_size)
    
    # incorrect false
    value = len(stats_plain["incorrect_false"])
    plt.bar(i + 10.5, value, width = 1, edgecolor = "black", facecolor = "red")
    plt.text(i + 10.5, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_musl["incorrect_false"])
    plt.bar(i + 11.5, value, width = 1, edgecolor = "black", facecolor = "blue")
    plt.text(i + 11.5, value + 2, str(value), ha='center', fontsize=text_font_size)
    value = len(stats_core["incorrect_false"])
    plt.bar(i + 12.5, value, width = 1, edgecolor = "black", facecolor = "green")
    plt.text(i + 12.5, value + 2, str(value), ha='center', fontsize=text_font_size)
   
    legend = [
            Line2D([0], [0], marker='s', color="white", markerfacecolor='red', label='Plain', markersize=14),
            Line2D([0], [0], marker='s', color="white", markerfacecolor='blue', label='MUSL', markersize=14),
            Line2D([0], [0], marker='s', color="white", markerfacecolor='green', label='CORE-MATH', markersize=14),
            ]
    plt.legend(handles=legend, fontsize=12, ncols=3)
    plt.title(tool, fontsize=18)
    plt.xticks([1, 4.5, 8, 11.5], ["correct true", "correct false", "incorrect true", "incorrect false"], rotation=20, fontsize=14)
    plt.yticks(fontsize=14)
    #plt.ylim([0, 150])
    plt.ylim([0, 370])
    #plt.ylim([0, 370])
    #plt.tight_layout()
    j = j + 1

plt.subplots_adjust(left=0.05, bottom=0.1, right=0.95, 
        top=0.95, wspace=0.2, hspace=0.7)
plt.show()

#exit()

# looking at what is solved by N verifiers
#res = verdict_by_n_verifiers(df_plain, "correct", 8)
#print("Benchmarks correctly solved by ALL PLAIN verifiers (", len(res), " overall)" )
#for task, tools in res.items():
#    print(task, tools)

#res = verdict_by_n_verifiers(df_musl, "correct", 8)
#print("Benchmarks correctly solved by ALL MUSL verifiers (", len(res), " overall)" )
#for task, tools in res.items():
#    print(task, tools)

#res = verdict_by_n_verifiers(df_plain, "correct", 0)
#print("Benchmarks correctly solved by NONE PLAIN verifiers (", len(res), " overall)" )
#for task, tools in res.items():
#    print(task, tools)

#res = verdict_by_n_verifiers(df_musl, "correct", 0)
#print("Benchmarks correctly solved by NONE MUSL verifiers (", len(res), " overall)" )
#for task, tools in res.items():
#    print(task, tools)

#res = verdict_by_verifiers(df_plain, "correct", ["esbmc"])
#print("Benchmarks correctly solved by ESBMC (", len(res), " overall)")
#for task, tools in res.items():
#    print(task, tools)


tool = "esbmc"
df_esbmc = df_plain[df_plain["host"] == tool]
sat_relu = df_esbmc[df_esbmc["run_subcategory"] == "sat_relu"]
sat_relu_safe = sat_relu[sat_relu["run_filename_clean"].str.contains("_safe")] 
sat_relu_unsafe = sat_relu[sat_relu["run_filename_clean"].str.contains("_unsafe")] 

sat_relu_safe_ordered = ["prop_bool_v5_c5_safe", "prop_bool_v5_c10_safe", "prop_bool_v5_c15_safe", "prop_bool_v5_c20_safe", "prop_bool_v5_c25_safe", "prop_bool_v5_c30_safe", "prop_bool_v8_c8_safe", "prop_bool_v8_c16_safe", "prop_bool_v8_c24_safe", "prop_bool_v8_c32_safe", "prop_bool_v8_c40_safe", "prop_bool_v8_c48_safe", "prop_bool_v13_c13_safe", "prop_bool_v13_c26_safe", "prop_bool_v13_c39_safe", "prop_bool_v13_c52_safe", "prop_bool_v13_c65_safe", "prop_bool_v13_c78_safe", "prop_bool_v21_c21_safe", "prop_bool_v21_c42_safe", "prop_bool_v21_c63_safe", "prop_bool_v21_c84_safe", "prop_bool_v21_c105_safe", "prop_bool_v21_c126_safe", "prop_bool_v34_c34_safe", "prop_bool_v34_c68_safe", "prop_bool_v34_c102_safe", "prop_bool_v34_c136_safe", "prop_bool_v34_c170_safe", "prop_bool_v34_c204_safe", "prop_bool_v55_c55_safe", "prop_bool_v55_c110_safe", "prop_bool_v55_c165_safe", "prop_bool_v55_c220_safe", "prop_bool_v55_c275_safe", "prop_bool_v55_c330_safe", "prop_bool_v89_c89_safe", "prop_bool_v89_c178_safe", "prop_bool_v89_c267_safe", "prop_bool_v89_c356_safe", "prop_bool_v89_c445_safe", "prop_bool_v89_c534_safe", "prop_bool_v144_c144_safe", "prop_bool_v144_c288_safe", "prop_bool_v144_c432_safe", "prop_bool_v144_c576_safe", "prop_bool_v144_c720_safe", "prop_bool_v144_c864_safe"]

sat_relu_unsafe_ordered = ["prop_bool_v5_c5_unsafe", "prop_bool_v5_c10_unsafe", "prop_bool_v5_c15_unsafe", "prop_bool_v5_c18_unsafe", "prop_bool_v5_c24_unsafe", "prop_bool_v5_c27_unsafe", "prop_bool_v8_c8_unsafe", "prop_bool_v8_c16_unsafe", "prop_bool_v8_c24_unsafe", "prop_bool_v8_c32_unsafe", "prop_bool_v8_c40_unsafe", "prop_bool_v8_c46_unsafe", "prop_bool_v13_c13_unsafe", "prop_bool_v13_c26_unsafe", "prop_bool_v13_c39_unsafe", "prop_bool_v13_c52_unsafe", "prop_bool_v13_c65_unsafe", "prop_bool_v13_c78_unsafe", "prop_bool_v21_c21_unsafe", "prop_bool_v21_c42_unsafe", "prop_bool_v21_c62_unsafe", "prop_bool_v21_c84_unsafe", "prop_bool_v21_c105_unsafe", "prop_bool_v21_c126_unsafe", "prop_bool_v34_c34_unsafe", "prop_bool_v34_c68_unsafe", "prop_bool_v34_c102_unsafe", "prop_bool_v34_c136_unsafe", "prop_bool_v34_c170_unsafe", "prop_bool_v34_c204_unsafe", "prop_bool_v55_c55_unsafe", "prop_bool_v55_c110_unsafe", "prop_bool_v55_c165_unsafe", "prop_bool_v55_c220_unsafe", "prop_bool_v55_c275_unsafe", "prop_bool_v55_c330_unsafe", "prop_bool_v89_c89_unsafe", "prop_bool_v89_c178_unsafe", "prop_bool_v89_c267_unsafe", "prop_bool_v89_c356_unsafe", "prop_bool_v89_c445_unsafe", "prop_bool_v89_c534_unsafe", "prop_bool_v144_c144_unsafe", "prop_bool_v144_c288_unsafe", "prop_bool_v144_c432_unsafe", "prop_bool_v144_c576_unsafe", "prop_bool_v144_c720_unsafe", "prop_bool_v144_c864_unsafe"]

#plot_cputimes(sat_relu_safe_ordered, sat_relu_safe)
#plot_cputimes(sat_relu_unsafe_ordered, sat_relu_unsafe)


#sat_relu = ["v5_c5_","v5_c10_","v5_c15_","v5_c20_","v5_c25_","v5_c30_",
#        "v8_c8_","v8_c16_","v8_c24_","v8_c32_","v8_c40_","v8_c46_","v8_c48_",
#        "v13_", 
#        "v21_", 
#        "v34_", 
#        "v55_", 
#        "v89_", 
#        "v144_"]
        
sat_relu = ["v5_",
        "v8_",
        "v13_", 
        "v21_", 
        "v34_", 
        "v55_", 
        "v89_", 
        "v144_"]

df = df_plain
#x_labels = [5, 8, 13, 21, 34, 55, 89, 144]
x_labels = sat_relu
x_vals = range(0, len(sat_relu))
tools = df["host"].unique()
#tools = ["2ls", "esbmc", "pinaka"]
#colors = ["blue", "orange", "green"] * 2

fig, ax = plt.subplots(ncols = 2, nrows = 4)

i = 0
j = 0
for tool in tools:
    ax1 = ax[i, j]
    df_tool = df[df["host"] == tool]
    mem_mean_vals = []
    mem_low_vals = []
    mem_high_vals = []
    cpu_mean_vals = []
    cpu_low_vals = []
    cpu_high_vals = []
    for task in sat_relu:
        df_task = df_tool[df_tool["run_filename_clean"].str.contains(task)]
        memory = df_task["memory"].to_numpy() / 1e6
        cputime = df_task["cputime"].to_numpy()
        mem_mean_vals.append(round(sum(memory) / len(memory)))
        mem_low_vals.append(round((sum(memory) / len(memory)) - min(memory)))
        mem_high_vals.append(round(max(memory) - (sum(memory) / len(memory))))
        cpu_mean_vals.append(round(sum(cputime) / len(cputime)))
        cpu_low_vals.append(round((sum(cputime) / len(cputime)) - min(cputime)))
        cpu_high_vals.append(round(max(cputime) - (sum(cputime) / len(cputime))))
    ax1.errorbar(x_vals, mem_mean_vals, [mem_low_vals, mem_high_vals], 
            capsize = 8, lw = 2, elinewidth = 1, marker = "s", color = "blue")
    
    ax2 = ax1.twinx()

    ax2.errorbar(x_vals, cpu_mean_vals, [cpu_low_vals, cpu_high_vals], 
            capsize = 8, lw = 2, elinewidth = 1, marker = "o", color = "orange")
    
    i = i + 1
    if i == 4:
        i = 0
        j = j + 1
    
    ax1.set_xticks(x_vals, x_labels)
    ax1.legend(["memory"])
    ax2.legend(["CPU time"])
    #plt.plot(x_vals, mean_vals, marker="s")
    #plt.legend([tool], fontsize=14)
    #ax1.xticks(x_vals, x_labels, fontsize=14)
    #ax1.xlabel("Number of variables per SAT formula", fontsize=16)
    #ax1.yticks(fontsize=14)
    #ax1.ylabel("Memory (MB)", fontsize=16)

plt.show()

exit()

for tool in tools:
    df_tool = df[df["host"] == tool]
    mean_vals = []
    low_vals = []
    high_vals = []
    plt.subplot(2,3,i)
    for task in sat_relu:
        df_task = df_tool[df_tool["run_filename_clean"].str.contains(task)]
        memory = df_task["cputime"].to_numpy()
        mean_vals.append(round(sum(memory) / len(memory)))
        low_vals.append(round((sum(memory) / len(memory)) - min(memory)))
        high_vals.append(round(max(memory) - (sum(memory) / len(memory))))
    print(mean_vals)
    print(low_vals)
    print(high_vals)
    plt.errorbar(x_vals, mean_vals, [low_vals, high_vals], 
            capsize = 8, lw = 2, elinewidth = 1, marker = "s",
            color = colors[i-1])
    i = i + 1
    #plt.plot(x_vals, mean_vals, marker="s")
    plt.legend([tool], fontsize=14)
    plt.xticks(x_vals, x_labels, fontsize=14)
    plt.xlabel("Number of variables per SAT formula", fontsize=16)
    plt.yticks(fontsize=14)
    plt.ylabel("CPU time (s)", fontsize=16)

#plt.legend(tools, fontsize=14)
#plt.xticks(x_vals, x_labels, fontsize=14)
#plt.yticks(fontsize=14)
plt.subplots_adjust(left=0.05, bottom=0.1, right=0.99, 
        top=0.95, wspace=0.2, hspace=0.3)
plt.show()


poly_approx = df_esbmc[df_esbmc["run_subcategory"] == "poly_approx"]
poly_approx_safe = poly_approx[poly_approx["run_filename_clean"].str.contains("_safe")] 
poly_approx_unsafe = poly_approx[poly_approx["run_filename_clean"].str.contains("_unsafe")] 

poly_approx_safe_ordered = ["poly_128_thresh_0_safe","poly_128_thresh_1_safe","poly_128_thresh_2_safe","poly_256_thresh_0_safe","poly_256_thresh_1_safe","poly_256_thresh_2_safe","poly_512_thresh_0_safe","poly_512_thresh_1_safe","poly_512_thresh_2_safe","poly_1024_thresh_0_safe","poly_1024_thresh_1_safe","poly_1024_thresh_2_safe","poly_16_16_thresh_0_safe","poly_16_16_thresh_1_safe","poly_16_16_thresh_2_safe","poly_32_32_thresh_0_safe","poly_32_32_thresh_1_safe","poly_32_32_thresh_2_safe","poly_64_64_thresh_0_safe","poly_64_64_thresh_1_safe","poly_64_64_thresh_2_safe","poly_128_128_thresh_0_safe","poly_128_128_thresh_1_safe","poly_128_128_thresh_2_safe","poly_8_8_8_thresh_0_safe","poly_8_8_8_thresh_1_safe","poly_8_8_8_thresh_2_safe","poly_16_16_16_thresh_0_safe","poly_16_16_16_thresh_1_safe","poly_16_16_16_thresh_2_safe","poly_32_32_32_thresh_0_safe","poly_32_32_32_thresh_1_safe","poly_32_32_32_thresh_2_safe","poly_64_64_64_thresh_0_safe","poly_64_64_64_thresh_1_safe","poly_64_64_64_thresh_2_safe","poly_4_4_4_4_thresh_0_safe","poly_4_4_4_4_thresh_1_safe","poly_4_4_4_4_thresh_2_safe","poly_8_8_8_8_thresh_0_safe","poly_8_8_8_8_thresh_1_safe","poly_8_8_8_8_thresh_2_safe","poly_16_16_16_16_thresh_0_safe","poly_16_16_16_16_thresh_1_safe","poly_16_16_16_16_thresh_2_safe","poly_32_32_32_32_thresh_0_safe","poly_32_32_32_32_thresh_1_safe","poly_32_32_32_32_thresh_2_safe"]


poly_approx_unsafe_ordered = ["poly_128_thresh_3_unsafe","poly_128_thresh_4_unsafe","poly_128_thresh_5_unsafe","poly_256_thresh_3_unsafe","poly_256_thresh_4_unsafe","poly_256_thresh_5_unsafe","poly_512_thresh_3_unsafe","poly_512_thresh_4_unsafe","poly_512_thresh_5_unsafe","poly_1024_thresh_3_unsafe","poly_1024_thresh_4_unsafe","poly_1024_thresh_5_unsafe","poly_16_16_thresh_3_unsafe","poly_16_16_thresh_4_unsafe","poly_16_16_thresh_5_unsafe","poly_32_32_thresh_3_unsafe","poly_32_32_thresh_4_unsafe","poly_32_32_thresh_5_unsafe","poly_64_64_thresh_3_unsafe","poly_64_64_thresh_4_unsafe","poly_64_64_thresh_5_unsafe","poly_128_128_thresh_3_unsafe","poly_128_128_thresh_4_unsafe","poly_128_128_thresh_5_unsafe","poly_8_8_8_thresh_3_unsafe","poly_8_8_8_thresh_4_unsafe","poly_8_8_8_thresh_5_unsafe","poly_16_16_16_thresh_3_unsafe","poly_16_16_16_thresh_4_unsafe","poly_16_16_16_thresh_5_unsafe","poly_32_32_32_thresh_3_unsafe","poly_32_32_32_thresh_4_unsafe","poly_32_32_32_thresh_5_unsafe","poly_64_64_64_thresh_3_unsafe","poly_64_64_64_thresh_4_unsafe","poly_64_64_64_thresh_5_unsafe","poly_4_4_4_4_thresh_3_unsafe","poly_4_4_4_4_thresh_4_unsafe","poly_4_4_4_4_thresh_5_unsafe","poly_8_8_8_8_thresh_3_unsafe","poly_8_8_8_8_thresh_4_unsafe","poly_8_8_8_8_thresh_5_unsafe","poly_16_16_16_16_thresh_3_unsafe","poly_16_16_16_16_thresh_4_unsafe","poly_16_16_16_16_thresh_5_unsafe","poly_32_32_32_32_thresh_3_unsafe","poly_32_32_32_32_thresh_4_unsafe","poly_32_32_32_32_thresh_5_unsafe"]

#plot_cputimes(poly_approx_safe_ordered, poly_approx_safe)
#plot_cputimes(poly_approx_unsafe_ordered, poly_approx_unsafe)

poly_approx = ["poly_128_", "poly_256_", "poly_512", "poly_1024", 
        "poly_16_16", "poly_32_32", "poly_64_64", "poly_128_128",
        "poly_8_8_8","poly_16_16_16","poly_32_32_32","poly_64_64_64",
        "poly_4_4_4_4","poly_8_8_8_8","poly_16_16_16_16","poly_32_32_32_32"]

df = df_plain
x_labels = poly_approx
x_vals = range(0, len(poly_approx))

for tool in tools:
    df_tool = df[df["host"] == tool]
    mean_vals = []
    low_vals = []
    high_vals = []
    for task in poly_approx:
        df_task = df_tool[df_tool["run_filename_clean"].str.contains(task)]
        memory = df_task["memory"].tolist()
        mean_vals.append(math.log(sum(memory) / len(memory)))
        low_vals.append(math.log((sum(memory) / len(memory)) - min(memory) + 1))
        high_vals.append(math.log(max(memory) - (sum(memory) / len(memory)) + 1))
    #plt.errorbar(x_vals, mean_vals, [low_vals, high_vals], 
    #        capsize = 6, lw = 2, elinewidth = 1, marker = "s")
    plt.plot(x_vals, mean_vals, marker="s")


plt.legend(tools, fontsize=14)
plt.xticks(x_vals, x_labels, fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.show()

exit()

hopfield_nets = df_esbmc[df_esbmc["run_subcategory"] == "hopfield_nets"]
hopfield_nets_safe = hopfield_nets[hopfield_nets["run_filename_clean"].str.contains("_safe")]
hopfield_nets_unsafe = hopfield_nets[hopfield_nets["run_filename_clean"].str.contains("_unsafe")]

hopfield_nets_safe_ordered = ["softsign_w4_r1_case_1_safe","softsign_w4_r2_case_0_safe","softsign_w4_r3_case_0_safe","softsign_w4_r4_case_0_safe","softsign_w8_r1_case_1_safe","softsign_w8_r2_case_0_safe","softsign_w8_r3_case_0_safe","softsign_w8_r4_case_0_safe","softsign_w16_r1_case_1_safe","softsign_w16_r2_case_0_safe","softsign_w16_r3_case_0_safe","softsign_w16_r4_case_0_safe","softsign_w32_r1_case_1_safe","softsign_w32_r2_case_0_safe","softsign_w32_r3_case_0_safe","softsign_w32_r4_case_0_safe","softsign_w64_r1_case_1_safe","softsign_w64_r2_case_0_safe","softsign_w64_r3_case_0_safe","softsign_w64_r4_case_0_safe","tanh_w4_r1_case_1_safe","tanh_w4_r2_case_0_safe","tanh_w4_r3_case_0_safe","tanh_w4_r4_case_0_safe","tanh_w8_r1_case_1_safe","tanh_w8_r2_case_0_safe","tanh_w8_r3_case_0_safe","tanh_w8_r4_case_0_safe","tanh_w16_r1_case_1_safe","tanh_w16_r2_case_0_safe","tanh_w16_r3_case_0_safe","tanh_w16_r3_case_1_safe","tanh_w16_r4_case_0_safe","tanh_w16_r4_case_1_safe","tanh_w32_r1_case_1_safe","tanh_w32_r2_case_0_safe","tanh_w32_r3_case_0_safe","tanh_w32_r3_case_1_safe","tanh_w32_r4_case_0_safe","tanh_w32_r4_case_1_safe","tanh_w64_r1_case_1_safe","tanh_w64_r2_case_0_safe","tanh_w64_r3_case_0_safe","tanh_w64_r3_case_1_safe","tanh_w64_r4_case_0_safe","tanh_w64_r4_case_1_safe"]

hopfield_nets_unsafe_ordered = ["softsign_w4_r1_case_0_unsafe","softsign_w4_r2_case_1_unsafe","softsign_w4_r3_case_1_unsafe","softsign_w4_r4_case_1_unsafe","softsign_w8_r1_case_0_unsafe","softsign_w8_r2_case_1_unsafe","softsign_w8_r3_case_1_unsafe","softsign_w8_r4_case_1_unsafe","softsign_w16_r1_case_0_unsafe","softsign_w16_r2_case_1_unsafe","softsign_w16_r3_case_1_unsafe","softsign_w16_r4_case_1_unsafe","softsign_w32_r1_case_0_unsafe","softsign_w32_r2_case_1_unsafe","softsign_w32_r3_case_1_unsafe","softsign_w32_r4_case_1_unsafe","softsign_w64_r1_case_0_unsafe","softsign_w64_r2_case_1_unsafe","softsign_w64_r3_case_1_unsafe","softsign_w64_r4_case_1_unsafe","tanh_w4_r1_case_0_unsafe","tanh_w4_r2_case_1_unsafe","tanh_w4_r3_case_1_unsafe","tanh_w4_r4_case_1_unsafe","tanh_w8_r1_case_0_unsafe","tanh_w8_r2_case_1_unsafe","tanh_w8_r3_case_1_unsafe","tanh_w8_r4_case_1_unsafe","tanh_w16_r1_case_0_unsafe","tanh_w16_r2_case_1_unsafe","tanh_w32_r1_case_0_unsafe","tanh_w32_r2_case_1_unsafe","tanh_w64_r1_case_0_unsafe","tanh_w64_r2_case_1_unsafe"]

plot_cputimes(hopfield_nets_safe_ordered, hopfield_nets_safe)
plot_cputimes(hopfield_nets_unsafe_ordered, hopfield_nets_unsafe)

lipschitz_bounded = df_esbmc[df_esbmc["run_subcategory"] == "lipschitz_bounded"]
lipschitz_bounded_safe = lipschitz_bounded[lipschitz_bounded["run_filename_clean"].str.contains("_safe")]
lipschitz_bounded_unsafe = lipschitz_bounded[lipschitz_bounded["run_filename_clean"].str.contains("_unsafe")]

lipschitz_bounded_safe_ordered = ["sll_2x4x4x1_case_3_safe","sll_2x4x4x1_case_4_safe","sll_2x4x4x1_case_5_safe","sll_3x4x4x1_case_3_safe","sll_3x4x4x1_case_4_safe","sll_3x4x4x1_case_5_safe","sll_4x4x4x1_case_3_safe","sll_4x4x4x1_case_4_safe","sll_4x4x4x1_case_5_safe","sll_2x8x8x1_case_3_safe","sll_2x8x8x1_case_4_safe","sll_2x8x8x1_case_5_safe","sll_3x8x8x1_case_3_safe","sll_3x8x8x1_case_4_safe","sll_3x8x8x1_case_5_safe","sll_4x8x8x1_case_3_safe","sll_4x8x8x1_case_4_safe","sll_4x8x8x1_case_5_safe","sll_2x12x12x1_case_3_safe","sll_2x12x12x1_case_4_safe","sll_2x12x12x1_case_5_safe","sll_3x12x12x1_case_3_safe","sll_3x12x12x1_case_4_safe","sll_3x12x12x1_case_5_safe","sll_4x12x12x1_case_3_safe","sll_4x12x12x1_case_4_safe","sll_4x12x12x1_case_5_safe","sll_2x16x16x1_case_3_safe","sll_2x16x16x1_case_4_safe","sll_2x16x16x1_case_5_safe","sll_3x16x16x1_case_3_safe","sll_3x16x16x1_case_4_safe","sll_3x16x16x1_case_5_safe","sll_4x16x16x1_case_3_safe","sll_4x16x16x1_case_4_safe","sll_4x16x16x1_case_5_safe","sll_2x20x20x1_case_3_safe","sll_2x20x20x1_case_4_safe","sll_2x20x20x1_case_5_safe","sll_3x20x20x1_case_3_safe","sll_3x20x20x1_case_4_safe","sll_3x20x20x1_case_5_safe","sll_4x20x20x1_case_3_safe","sll_4x20x20x1_case_4_safe","sll_4x20x20x1_case_5_safe","sll_2x24x24x1_case_3_safe","sll_2x24x24x1_case_4_safe","sll_2x24x24x1_case_5_safe","sll_3x24x24x1_case_3_safe","sll_3x24x24x1_case_4_safe","sll_3x24x24x1_case_5_safe","sll_4x24x24x1_case_3_safe","sll_4x24x24x1_case_4_safe","sll_4x24x24x1_case_5_safe"]

lipschitz_bounded_unsafe_ordered = ["sll_2x4x4x1_case_0_unsafe","sll_2x4x4x1_case_1_unsafe","sll_2x4x4x1_case_2_unsafe","sll_3x4x4x1_case_0_unsafe","sll_3x4x4x1_case_1_unsafe","sll_3x4x4x1_case_2_unsafe","sll_4x4x4x1_case_0_unsafe","sll_4x4x4x1_case_1_unsafe","sll_4x4x4x1_case_2_unsafe","sll_2x8x8x1_case_0_unsafe","sll_2x8x8x1_case_1_unsafe","sll_2x8x8x1_case_2_unsafe","sll_3x8x8x1_case_0_unsafe","sll_3x8x8x1_case_1_unsafe","sll_3x8x8x1_case_2_unsafe","sll_4x8x8x1_case_0_unsafe","sll_4x8x8x1_case_1_unsafe","sll_4x8x8x1_case_2_unsafe","sll_2x12x12x1_case_0_unsafe","sll_2x12x12x1_case_1_unsafe","sll_2x12x12x1_case_2_unsafe","sll_3x12x12x1_case_0_unsafe","sll_3x12x12x1_case_1_unsafe","sll_3x12x12x1_case_2_unsafe","sll_4x12x12x1_case_0_unsafe","sll_4x12x12x1_case_1_unsafe","sll_4x12x12x1_case_2_unsafe","sll_2x16x16x1_case_0_unsafe","sll_2x16x16x1_case_1_unsafe","sll_2x16x16x1_case_2_unsafe","sll_3x16x16x1_case_0_unsafe","sll_3x16x16x1_case_1_unsafe","sll_3x16x16x1_case_2_unsafe","sll_4x16x16x1_case_0_unsafe","sll_4x16x16x1_case_1_unsafe","sll_4x16x16x1_case_2_unsafe","sll_2x20x20x1_case_0_unsafe","sll_2x20x20x1_case_1_unsafe","sll_2x20x20x1_case_2_unsafe","sll_3x20x20x1_case_0_unsafe","sll_3x20x20x1_case_1_unsafe","sll_3x20x20x1_case_2_unsafe","sll_4x20x20x1_case_0_unsafe","sll_4x20x20x1_case_1_unsafe","sll_4x20x20x1_case_2_unsafe","sll_2x24x24x1_case_0_unsafe","sll_2x24x24x1_case_1_unsafe","sll_2x24x24x1_case_2_unsafe","sll_3x24x24x1_case_0_unsafe","sll_3x24x24x1_case_1_unsafe","sll_3x24x24x1_case_2_unsafe","sll_4x24x24x1_case_0_unsafe","sll_4x24x24x1_case_1_unsafe","sll_4x24x24x1_case_2_unsafe"]

plot_cputimes(lipschitz_bounded_safe_ordered, lipschitz_bounded_safe)
plot_cputimes(lipschitz_bounded_unsafe_ordered, lipschitz_bounded_unsafe)


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
