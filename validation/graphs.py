import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


old_df = pd.read_csv("validation/oldVersion.csv")
new_df = pd.read_csv("validation/newVersion.csv")

testName = {"oldVersion": old_df["testName"], "newVersion": new_df["testName"]}
nSubmodels = {"oldVersion": old_df["nSubmodels"], "newVersion": new_df["nSubmodels"]}
nMutants = {"oldVersion": old_df["nMutants"], "newVersion": new_df["nMutants"]}
nQuestions = {"oldVersion": old_df["nQuestions"], "newVersion": new_df["nQuestions"]}

width = 0.25  # the width of the bars
multiplier = 0

x = np.arange(len(testName["oldVersion"]))  # the label locations


fig, ax = plt.subplots(layout='constrained')


for attribute, measurement in nMutants.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('# generated')
ax.set_title('Number of mutations')
ax.set_xticks(x + width, testName["oldVersion"])
ax.legend(loc='upper right', ncols=3)
ax.set_ylim(0, 40)

plt.show()