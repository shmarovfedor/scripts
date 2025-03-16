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

# just to check whether termination reason "cputime" means a TIMEOUT
# and "memory" means OUT OF MEMORY
#print(df[(df["terminationreason"] == "cputime")]["status"].unique()) 
#print(df[(df["terminationreason"] == "memory")]["status"].unique()) 
#print(df[(df["category"] == "error")]["status"].unique())
#print((df["category"] == "correct").unique())
#print((df["category"] == "wrong").unique())

df_correct = df[(df["category"] == "correct")]
df_correct_true = df_correct[(df_correct["run_expectedVerdict"] == True)]
df_correct_false = df_correct[(df_correct["run_expectedVerdict"] == False)]
df_wrong = df[(df["category"] == "wrong")]
df_wrong_true = df_wrong[(df_wrong["run_expectedVerdict"] == True)]
df_wrong_false = df_wrong[(df_wrong["run_expectedVerdict"] == False)]
df_timeout = df[(df["terminationreason"] == "cputime")]
df_oom = df[(df["terminationreason"] == "memory")]

df_verdict = pd.concat([df_correct, df_wrong, df_timeout, df_oom], axis = 0)

print(df["run_subcategory"].unique())
print(df_verdict)

for subcategory in df["run_subcategory"].unique():
    df_subcat = df_verdict[(df_verdict["run_subcategory"] == subcategory)].sort_values("run_filename_clean")
    labels = []
    times = []
    i = 0
    for task in df_subcat["run_filename_clean"].unique():
        df_task = df_subcat[(df_subcat["run_filename_clean"] == task)]
        times.append(df_task["cputime"])
        labels.append(task)
        for index, rec in df_task.iterrows():
            if (rec["category"] == "correct") & (rec["run_expectedVerdict"]):
                color = "green"
                marker = "^"
            if (rec["category"] == "correct") & (~rec["run_expectedVerdict"]):
                color = "green"
                marker = "v"
            if (rec["category"] == "wrong") & (rec["run_expectedVerdict"]):
                color = "red"
                marker = "^"
            if (rec["category"] == "wrong") & (~rec["run_expectedVerdict"]):
                color = "red"
                marker = "v"
            if (rec["terminationreason"] == "cputime"):
                color = "black"
                marker = "x"
            if (rec["terminationreason"] == "memory"):
                color = "black"
                marker = "+"
            plt.scatter(i, math.log(rec["cputime"]), color=color, marker=marker)
        i = i + 1

    legend = [
            Line2D([0], [0], marker='^', color="white", markerfacecolor='green', label='correct true', markersize=9),
            Line2D([0], [0], marker='v', color="white", markerfacecolor='green', label='correct false', markersize=9),
            Line2D([0], [0], marker='^', color="white", markerfacecolor='red', label='incorrect true', markersize=9),
            Line2D([0], [0], marker='v', color="white", markerfacecolor='red', label='incorrect false', markersize=9),
            Line2D([0], [0], marker='x', color="white", markeredgecolor='black', label='timeout', markersize=7),
            Line2D([0], [0], marker='+', color="white", markeredgecolor='black', label='out of memory', markersize=9),
            ]

    plt.title(str("Subcategory: " + subcategory))
    plt.xlabel("Benchmark name")
    plt.ylabel("CPU time log(s)")
    plt.xticks(range(0, len(labels)), labels = labels, rotation=90)
    plt.tight_layout()
    #plt.ylim(-30, 1000)
    plt.xlim(-1, len(labels))
    plt.legend(handles=legend)
    plt.show()


# only final verdicts and timeouts
#df_verdict_and_timeout


exit()

solvers = df["host"].unique()

correct_true = dict(zip(solvers, [0] * len(solvers)))
correct_false = dict(zip(solvers, [0] * len(solvers)))
incorrect_true = dict(zip(solvers, [0] * len(solvers)))
incorrect_false = dict(zip(solvers, [0] * len(solvers)))
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
unknown = OrderedDict(sorted(unknown.items()))
timeout = OrderedDict(sorted(timeout.items()))
out_of_memory = OrderedDict(sorted(out_of_memory.items()))
other = OrderedDict(sorted(other.items()))
total = OrderedDict(sorted(total.items()))

# plotting correct and incorrect here
x_axis = np.arange(len(correct_true)) * 5
plt.bar(x_axis, correct_true.values(), width = 1, label = "correct true")
for i, value in enumerate(correct_true.values()):
    plt.text(x_axis[i], value + 5, str(value), ha='center')

plt.bar(x_axis + 1, correct_false.values(), width = 1, label = "correct false")
for i, value in enumerate(correct_false.values()):
    plt.text(x_axis[i] + 1, value + 5, str(value), ha='center')

plt.bar(x_axis + 2, incorrect_true.values(), width = 1, label = "incorrect true")
for i, value in enumerate(incorrect_true.values()):
    plt.text(x_axis[i] + 2, value + 5, str(value), ha='center')

plt.bar(x_axis + 3, incorrect_false.values(), width = 1, label = "incorrect false")
for i, value in enumerate(incorrect_false.values()):
    plt.text(x_axis[i] + 3, value + 5, str(value), ha='center')

plt.xticks(x_axis + 2, correct_true.keys())
plt.legend()
plt.show()


# plotting everything here
x_axis = np.arange(len(correct_true)) * 9
plt.bar(x_axis, correct_true.values(), width = 1, label = "correct true")
for i, value in enumerate(correct_true.values()):
    plt.text(x_axis[i], value + 5, str(value), ha='center')

plt.bar(x_axis + 1, correct_false.values(), width = 1, label = "correct false")
for i, value in enumerate(correct_false.values()):
    plt.text(x_axis[i] + 1, value + 5, str(value), ha='center')

plt.bar(x_axis + 2, incorrect_true.values(), width = 1, label = "incorrect true")
for i, value in enumerate(incorrect_true.values()):
    plt.text(x_axis[i] + 2, value + 5, str(value), ha='center')

plt.bar(x_axis + 3, incorrect_false.values(), width = 1, label = "incorrect false")
for i, value in enumerate(incorrect_false.values()):
    plt.text(x_axis[i] + 3, value + 5, str(value), ha='center')

plt.bar(x_axis + 4, unknown.values(), width = 1, label = "unknown")
for i, value in enumerate(unknown.values()):
    plt.text(x_axis[i] + 4, value + 5, str(value), ha='center')

plt.bar(x_axis + 5, timeout.values(), width = 1, label = "timeout")
for i, value in enumerate(timeout.values()):
    plt.text(x_axis[i] + 5, value + 5, str(value), ha='center')

plt.bar(x_axis + 6, out_of_memory.values(), width = 1, label = "iout of memory")
for i, value in enumerate(out_of_memory.values()):
    plt.text(x_axis[i] + 6, value + 5, str(value), ha='center')

plt.bar(x_axis + 7, other.values(), width = 1, label = "other (errors)")
for i, value in enumerate(other.values()):
    plt.text(x_axis[i] + 7, value + 5, str(value), ha='center')

plt.xticks(x_axis + 4, correct_true.keys())
plt.legend()
plt.show()



#plt.bar(avg_walltime_per_task.keys(), avg_walltime_per_task.values(), width = 1, label = "average times")
#plt.legend()
#plt.show()




