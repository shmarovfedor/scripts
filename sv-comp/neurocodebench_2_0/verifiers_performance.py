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




## main()

filepath = sys.argv[1]
df = pd.read_csv(filepath)
df = add_extra_columns(df)
df = tudy_up(df)

print(df.columns)


## Generating Figures "statistics per tool"
solvers = df["host"].unique()

correct_true = dict(zip(solvers, [0] * len(solvers)))
correct_false = dict(zip(solvers, [0] * len(solvers)))
incorrect_true = dict(zip(solvers, [0] * len(solvers)))
incorrect_false = dict(zip(solvers, [0] * len(solvers)))
verdicts = dict(zip(solvers, [0] * len(solvers)))
unknown = dict(zip(solvers, [0] * len(solvers)))
timeout = dict(zip(solvers, [0] * len(solvers)))
out_of_memory = dict(zip(solvers, [0] * len(solvers)))
other = dict(zip(solvers, [0] * len(solvers)))
total = dict(zip(solvers, [0] * len(solvers)))


for solver in solvers:
    total[solver] = (df["host"] == solver).sum()

    correct_true[solver] = ((df["host"] == solver) 
            & (df["category"] == "correct")
            & (df["run_expectedVerdict"] == True)).sum()

    correct_false[solver] = ((df["host"] == solver) 
            & (df["category"] == "correct")
            & (df["run_expectedVerdict"] == False)).sum()

    incorrect_true[solver] = ((df["host"] == solver) 
            & (df["category"] == "wrong")
            & (df["run_expectedVerdict"] == False)).sum()
    
    incorrect_false[solver] = ((df["host"] == solver) 
            & (df["category"] == "wrong")
            & (df["run_expectedVerdict"] == True)).sum()

    unknown[solver] = ((df["host"] == solver) 
            & (df["category"] == "unknown")).sum()
    
    timeout[solver] = ((df["host"] == solver) 
            & ((df["status"] == "TIMEOUT") | 
                (df["status"] == "TIMEOUT (ERROR - no output)"))).sum()
    
    out_of_memory[solver] = ((df["host"] == solver) 
            & ((df["status"] == "OUT OF MEMORY") | 
                (df["status"] == "OUT OF MEMORY (ERROR - no output)"))).sum()

    other[solver] = ((df["host"] == solver) 
            & (df["category"] == "error") 
            & ~(df["status"] == "TIMEOUT")
            & ~(df["status"] == "TIMEOUT (ERROR - no output)")
            & ~(df["status"] == "OUT OF MEMORY")
            & ~(df["status"] == "OUT OF MEMORY (ERROR - no output)")).sum()

    verdicts[solver] = ((df["host"] == solver) & 
            ((df["category"] == "correct") | (df["category"] == "wrong"))).sum()


    
print("Correct TRUE: ", correct_true)
print("Correct FALSE: ", correct_false)
print("Incorrect TRUE: ", incorrect_true)
print("Incorrect FALSE: ", incorrect_false)
print("Unknown: ", unknown)
print("TIMEOUT: ", timeout)
print("OUT OF MEMORY: ", out_of_memory)
print("Other (i.e., errors, etc.): ", other)

sum_of_values = dict(Counter(correct_true) +
        Counter(correct_false) +
        Counter(incorrect_true) +
        Counter(incorrect_false) +
        Counter(unknown) +
        Counter(timeout) + 
        Counter(out_of_memory) + 
        Counter(other))

print("Sum: ", sum_of_values)
print("Total: ", total)

if not sum_of_values == total:
    print("Something is missing: sum of values in all categories is not equal to the total number of tasks for some solvers", file=sys.stderr)


# ordering all dictionaries just in case
correct_true = OrderedDict(sorted(correct_true.items()))
correct_false = OrderedDict(sorted(correct_false.items()))
incorrect_true = OrderedDict(sorted(incorrect_true.items()))
incorrect_false = OrderedDict(sorted(incorrect_false.items()))
verdicts = OrderedDict(sorted(verdicts.items()))
unknown = OrderedDict(sorted(unknown.items()))
timeout = OrderedDict(sorted(timeout.items()))
out_of_memory = OrderedDict(sorted(out_of_memory.items()))
other = OrderedDict(sorted(other.items()))
total = OrderedDict(sorted(total.items()))

## New figure here: plotting correct and incorrect here
plt.clf()
plt.tight_layout()

x_axis = np.arange(len(correct_true)) * 6
plt.bar(x_axis, correct_true.values(), width = 1, label = "correct true", edgecolor = "black")
for i, value in enumerate(correct_true.values()):
    plt.text(x_axis[i], value + 10, str(value), ha='center', rotation=90, fontsize=7)

plt.bar(x_axis + 1, correct_false.values(), width = 1, label = "correct false", edgecolor = "black")
for i, value in enumerate(correct_false.values()):
    plt.text(x_axis[i] + 1.1, value + 10, str(value), ha='center', rotation=90, fontsize=7)

plt.bar(x_axis + 2, incorrect_true.values(), width = 1, label = "incorrect true", edgecolor = "black")
for i, value in enumerate(incorrect_true.values()):
    plt.text(x_axis[i] + 2.1, value + 10, str(value), ha='center', rotation=90, fontsize=7)

plt.bar(x_axis + 3, incorrect_false.values(), width = 1, label = "incorrect false", edgecolor = "black")
for i, value in enumerate(incorrect_false.values()):
    plt.text(x_axis[i] + 3.1, value + 10, str(value), ha='center', rotation=90, fontsize=7)

plt.xticks(x_axis + 2, correct_true.keys())
plt.title("True/false verdicts returned by the verifiers")
#plt.xlabel("Verifier name")
plt.ylabel("# of benchmarks")
plt.legend(fontsize = 8)
plt.ylim(0, 400)
plt.xticks(rotation=45)
#plt.show()
plt.gca().set_aspect(0.04)
plt.savefig("verifiers_true_false.pdf", 
        bbox_inches = "tight", 
        orientation = "landscape")




## New figure here: plotting the rest of verdicts
plt.clf()
plt.tight_layout()

x_axis = np.arange(len(correct_true)) * 7
plt.bar(x_axis, verdicts.values(), width = 1, label = "true/false", edgecolor = "black", color = "white", hatch = "x")
for i, value in enumerate(verdicts.values()):
    plt.text(x_axis[i], value + 20, str(value), ha='center', rotation=90, fontsize=6)

plt.bar(x_axis + 1, timeout.values(), width = 1, label = "timeout", edgecolor = "black")
for i, value in enumerate(timeout.values()):
    plt.text(x_axis[i] + 1.1, value + 20, str(value), ha='center', rotation=90, fontsize=6)

plt.bar(x_axis + 2, out_of_memory.values(), width = 1, label = "out of memory", edgecolor = "black")
for i, value in enumerate(out_of_memory.values()):
    plt.text(x_axis[i] + 2.1, value + 20, str(value), ha='center', rotation=90, fontsize=6)

plt.bar(x_axis + 3, unknown.values(), width = 1, label = "unknown", edgecolor = "black")
for i, value in enumerate(unknown.values()):
    plt.text(x_axis[i] + 3.1, value + 20, str(value), ha='center', rotation=90, fontsize=6)

plt.bar(x_axis + 4, other.values(), width = 1, label = "errors", edgecolor = "black")
for i, value in enumerate(other.values()):
    plt.text(x_axis[i] + 4.1, value + 20, str(value), ha='center', rotation=90, fontsize=6)

plt.xticks(x_axis + 2, correct_true.keys())
plt.title("All categories of verdicts returned by the verifiers")
#plt.xlabel("Verifier name")
plt.ylabel("# of benchmarks")
plt.legend(fontsize = 8)
plt.ylim(0, 1050)
plt.xticks(rotation=45)
#plt.show()
plt.gca().set_aspect(0.03)
plt.savefig("verifiers_all_verdicts.pdf",
        bbox_inches = "tight", 
        orientation = "landscape")


## Analysing time distributions for all the "true/false" verdicts
df_verdict = df[(df["category"] == "correct") | (df["category"] == "wrong")] 

plt.clf()
plt.tight_layout()

plt.hist(df_verdict["cputime"], bins = 50, edgecolor = "black", color = "blue")
plt.title("Distribution of CPU time taken to return \"TRUE / FALSE\" verdicts")
plt.xlabel("Termination time (s)")
plt.ylabel("# of benchmarks")

memo = "\"TRUE / FALSE\" verdicts by verifier:\n"
for solver in solvers:
    memo = memo + solver + " : " + str(other[solver]) + "\n"

plt.text(300, 20, memo)
plt.gca().set_aspect(0.6)
plt.xlim(0, 920)
plt.savefig("true_false_time_dist.pdf",
        bbox_inches = "tight", 
        orientation = "landscape")


## Analysing time distributions for all the "unknown" verdicts
df_unknown = df[(df["category"] == "unknown")]

plt.clf()
plt.tight_layout()

plt.hist(df_unknown["cputime"], bins = 50, edgecolor = "black", color = "green")
plt.title("Distribution of CPU time taken to return \"UNKNOWN\" verdicts")
plt.xlabel("Termination time (s)")
plt.ylabel("# of benchmarks")

memo = "\"UNKNOWN\" verdicts by verifier:\n"
for solver in solvers:
    memo = memo + solver + " : " + str(unknown[solver]) + "\n"

plt.text(200, 20, memo)
plt.gca().set_aspect(0.35)
plt.xlim(0, 920)
plt.savefig("unknowns_time_dist.pdf",
        bbox_inches = "tight", 
        orientation = "landscape")


## Analysing time distributions for all the "unknown" verdicts
df_error = df[(df["category"] == "error") 
            & ~(df["status"] == "TIMEOUT")
            & ~(df["status"] == "TIMEOUT (ERROR - no output)")
            & ~(df["status"] == "OUT OF MEMORY")
            & ~(df["status"] == "OUT OF MEMORY (ERROR - no output)")]

plt.clf()
plt.tight_layout()

plt.hist(df_error["cputime"], bins = 50, edgecolor = "black", color = "red")
plt.title("Distribution of CPU time taken to return \"ERROR\" verdicts")
plt.xlabel("Termination time (s)")
plt.ylabel("# of benchmarks")

memo = "\"ERROR\" verdicts by verifier:\n"
for solver in solvers:
    memo = memo + solver + " : " + str(other[solver]) + "\n"

plt.text(300, 20, memo)
plt.gca().set_aspect(1)
plt.xlim(0, 920)
plt.savefig("errors_time_dist.pdf",
        bbox_inches = "tight", 
        orientation = "landscape")
















