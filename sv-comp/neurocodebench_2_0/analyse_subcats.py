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




df = load_df_from_files(sys.argv[1:])

for subcat in df["run_subcategory"].unique():
    df_subcat = df[df["run_subcategory"] == subcat]
    print("--------------------")
    print(subcat)
    print("--------------------")
    #print(df_subcat["run_filename_clean"].unique())
    for tool in df_subcat["host"].unique():
        df_new = df_subcat[df_subcat["host"] == tool]
        print(tool, ": correct = ", (df_new["category"] == "correct").sum(),
                "; wrong = ", (df_new["category"] == "wrong").sum(),
                "; overall = ", len(df_new))





