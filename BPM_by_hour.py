import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
register_matplotlib_converters()

chart_size = (12, 8)
show_charts = False

df = pd.read_hdf('health_data.h5', 'health')

df_hr = df[df['Type'] == 'Heart Rate']
df_hr = pd.pivot_table(df_hr, 'Value', 'End', 'Type')
df_hr = df_hr.resample('H').mean()

df_ex = df[df['Type'] == 'Exercise Time']
df_ex = pd.pivot_table(df_ex, 'Value', 'End', 'Type')
df_ex = df_ex.resample('H').sum()

df_hr['Hour'] = df_hr.index.hour
df_hr['Date'] = df_hr.index.date
df_hr['Exercise'] = ~(df_ex['Exercise Time'] <= 5)

# Plot
fig = plt.figure(figsize=(15, 7))
ax = fig.gca()
ax = sns.violinplot(data=df_hr,
                    x="Hour",
                    y="Heart Rate",
                    hue="Exercise",
                    split=True,
                    linewidth=0.5,
                    ax=ax)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
