from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

before = {
        "CBMC" : {
            "correct" : 111,
            "unknown" : 420,
            "incorrect" : 76
            },
        "CPAChecker" : {
            "correct" : 30,
            "unknown" : 508,
            "incorrect" : 69
            },
        "ESBMC" : {
            "correct" : 255,
            "unknown" : 175,
            "incorrect" : 177
            },
        "PeSCo" : {
            "correct" : 224,
            "unknown" : 0,
            "incorrect" : 383
            },
        "UAutomizer" : {
            "correct" : 7,
            "unknown" : 594,
            "incorrect" : 6
            }
        }

after = {
        "CBMC" : {
            "correct" : 204,
            "unknown" : 321,
            "incorrect" : 78
            },
        "CPAChecker" : {
            "correct" : 7,
            "unknown" : 596,
            "incorrect" : 0
            },
        "ESBMC" : {
            "correct" : 50,
            "unknown" : 553,
            "incorrect" : 0
            },
        "PeSCo" : {
            "correct" : 11,
            "unknown" : 592,
            "incorrect" : 0
            },
        "UAutomizer" : {
            "correct" : 6,
            "unknown" : 597,
            "incorrect" : 0
            }
        }

fig = plt.figure(figsize = (9, 4), dpi = 100)
# setting the font family
rc('font', **{'family': 'serif', 'serif': ['Linux Libertine O']})

text_font_size = 20
text_vspace = 10

# before
i = 0
for tool in before:
    tool_stats = before[tool]
    value = tool_stats["correct"]
    plt.bar(i + 0, value, width = 1, edgecolor = "black", facecolor = "blue")
    plt.text(i + 0, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
            
    value = tool_stats["incorrect"]
    plt.bar(i + 1, value, width = 1, edgecolor = "black", facecolor = "red")
    plt.text(i + 1, value + text_vspace, str(value), ha='center', fontsize=text_font_size)

    value = tool_stats["unknown"]
    plt.bar(i + 2, value, width = 1, edgecolor = "black", facecolor = "black")
    plt.text(i + 2, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
    i = i + 4

legend = [
        Line2D([0], [0], marker='s', color="white", markerfacecolor='blue', label='correct', markersize=18),
        Line2D([0], [0], marker='s', color="white", markerfacecolor='red', label='incorrect', markersize=18),
        Line2D([0], [0], marker='s', color="white", markerfacecolor='black', label='unknown', markersize=18),
        ]
plt.legend(handles=legend, fontsize=22, ncols=3)
plt.xticks([1, 5, 9, 13, 17], before.keys(), fontsize=22)
plt.title("August 2023", fontsize = 26)
plt.ylabel("# benchmarks", fontsize = 26)
plt.yticks(fontsize = 24)
plt.ylim([0, 900])
plt.subplots_adjust(left=0.12, bottom=0.1, right=0.99, 
        top=0.91, wspace=0.1, hspace=0.1)

plt.show()
fig.savefig("sv_comp_before.pdf", format = "pdf")

fig = plt.figure(figsize = (9, 4), dpi = 100)
# setting the font family
rc('font', **{'family': 'serif', 'serif': ['Linux Libertine O']})

# after
i = 0
for tool in after:
    tool_stats = after[tool]
    value = tool_stats["correct"]
    plt.bar(i + 0, value, width = 1, edgecolor = "black", facecolor = "blue")
    plt.text(i + 0, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
            
    value = tool_stats["incorrect"]
    plt.bar(i + 1, value, width = 1, edgecolor = "black", facecolor = "red")
    plt.text(i + 1, value + text_vspace, str(value), ha='center', fontsize=text_font_size)

    value = tool_stats["unknown"]
    plt.bar(i + 2, value, width = 1, edgecolor = "black", facecolor = "black")
    plt.text(i + 2, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
    i = i + 4

legend = [
        Line2D([0], [0], marker='s', color="white", markerfacecolor='blue', label='correct', markersize=18),
        Line2D([0], [0], marker='s', color="white", markerfacecolor='red', label='incorrect', markersize=18),
        Line2D([0], [0], marker='s', color="white", markerfacecolor='black', label='unknown', markersize=18),
        ]

plt.legend(handles=legend, fontsize=22, ncols=3)
plt.xticks([1, 5, 9, 13, 17], before.keys(), fontsize=22)
plt.title("December 2023", fontsize = 26)
plt.ylabel("# benchmarks", fontsize = 26)
plt.yticks(fontsize = 24)
plt.ylim([0, 900])
plt.subplots_adjust(left=0.12, bottom=0.1, right=0.99, 
        top=0.91, wspace=0.1, hspace=0.1)

plt.show()
fig.savefig("sv_comp_after.pdf", format = "pdf")


















