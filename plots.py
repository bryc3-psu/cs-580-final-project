import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
  "figure.dpi":      150,
  "font.size":       12,
  "axes.titlesize":  14,
  "axes.labelsize":  12,
  "legend.fontsize": 10,
  "lines.linewidth": 1.5,
  "lines.markersize": 4,
})
 
def line_plot(
  datapoints: dict[str, list[tuple]],
  xlabel: str,
  ylabel: str,
  title: str,
  styles: dict[str, dict] = None,
) -> plt.Figure:
  fig, ax = plt.subplots(figsize=(6, 5))
  for label, points in datapoints.items():
    x, y = zip(*points)
    kwargs = styles.get(label, {}) if styles else {}
    sns.lineplot(x=x, y=y, label=label, ax=ax, **kwargs)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.legend(framealpha=0.8)
  fig.tight_layout()
  return fig

def bar_plot(
  datapoints: dict[str, dict[str, float]],
  xlabel: str,
  ylabel: str,
  title: str,
) -> plt.Figure:
  rows = [
    {"Algorithm": algo, "Group": group, "Value": value}
    for algo, groups in datapoints.items()
    for group, value in groups.items()
  ]
  df = pd.DataFrame(rows)
  fig, ax = plt.subplots()
  sns.barplot(data=df, x="Group", y="Value", hue="Algorithm", ax=ax)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  return fig
