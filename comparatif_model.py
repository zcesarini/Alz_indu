import json
import glob
import os
import matplotlib.pyplot as plt
import pandas as pd

files = glob.glob("artifacts/*metrics.json")

data = []

for f in files:
    with open(f, "r") as file:
        metrics = json.load(file)
        metrics["model"] = os.path.splitext(os.path.basename(f))[0]
        data.append(metrics)

df = pd.DataFrame(data)
ax = df.set_index("model").plot(kind="bar", figsize=(12, 6))

cols = ["model", "precision_1", "recall_1", "f1-score_1", "accuracy"]
df = df[cols]


for container in ax.containers:
    ax.bar_label(container, fmt="%.3f", padding=3)

plt.title("Comparaison des métriques des modèles")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()


