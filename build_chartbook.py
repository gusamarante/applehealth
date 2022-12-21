import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

chart_size = (17, 8)
show_charts = False

# Important dates
quarentine_date = '2020-03-20'
exercise_date = '2020-04-06'
quarentine_end = '2020-07-13'
ozempic_date = '2020-08-04'
ozempic_date2 = '2021-04-26'
sett_date = '2020-10-23'
CE_start = '2020-12-13'
CE_end = '2020-12-20'
new_scale_date = '2022-01-26'

# Read data
df = pd.read_hdf('health_data.h5', 'health')

with PdfPages('health_chartbook.pdf') as pdf:
    # ===== Weight =====
    df_aux = df[df['Type'] == 'Body Mass']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').mean()
    df_aux = df_aux.interpolate()
    df_aux = df_aux.fillna(method='ffill')
    df_weight = df_aux.copy()
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['Body Mass 7DMA'] = df_aux['Body Mass'].rolling(7).mean()
    df_aux['Body Mass 30DMA'] = df_aux['Body Mass'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(df_aux['Body Mass'], linewidth=0, color='blue', alpha=0.5, marker='o', markeredgecolor='white')
    ax.plot(df_aux['Body Mass 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['Body Mass 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    ax.set(title='Weight',
           xlabel=None,
           ylabel='Kilograms')

    loc = MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    ax.axvline(new_scale_date, color='black', linewidth=1)

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Body Mass Index =====
    df_aux = df[df['Type'] == 'BMI']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').mean()
    df_aux = df_aux.interpolate()
    df_aux = df_aux.fillna(method='ffill')
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['BMI 7DMA'] = df_aux['BMI'].rolling(7).mean()
    df_aux['BMI 30DMA'] = df_aux['BMI'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(df_aux['BMI'], linewidth=0, color='blue', alpha=0.5, marker='o', markeredgecolor='white')
    ax.plot(df_aux['BMI 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['BMI 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    ax.axvline(new_scale_date, color='black', linewidth=1)

    ax.set(title='Body Mass Index',
           xlabel=None,
           ylabel=None)

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Body Fat Percentage =====
    df_aux = df[df['Type'] == 'Body Fat Percentage']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').mean()
    df_aux = df_aux.interpolate()
    df_aux = df_aux.fillna(method='ffill')
    df_bfp = df_aux.copy()
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['Body Fat Percentage 7DMA'] = df_aux['Body Fat Percentage'].rolling(7).mean()
    df_aux['Body Fat Percentage 30DMA'] = df_aux['Body Fat Percentage'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(100*df_aux['Body Fat Percentage'], linewidth=0, color='blue', alpha=0.5, marker='o', markeredgecolor='white')
    ax.plot(100*df_aux['Body Fat Percentage 7DMA'], linewidth=3, color='blue')
    ax.plot(100 * df_aux['Body Fat Percentage 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    loc = MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    ax.axvline(new_scale_date, color='black', linewidth=1)

    ax.set(title='Body Fat Percentage',
           xlabel=None,
           ylabel=r'%')

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Kg of Fat =====
    df_aux = (df_bfp['Body Fat Percentage'] * df_weight['Body Mass']/100).to_frame('Kg of Fat')
    df_aux['Kg of Fat 7DMA'] = df_aux['Kg of Fat'].rolling(7).mean()
    df_aux['Kg of Fat 30DMA'] = df_aux['Kg of Fat'].rolling(30).mean()
    df_aux = df_aux[df_aux.index >= '2020-01-01']

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(100 * df_aux['Kg of Fat'], linewidth=0, color='blue', alpha=0.5, marker='o', markeredgecolor='white')
    ax.plot(100 * df_aux['Kg of Fat 7DMA'], linewidth=3, color='blue')
    ax.plot(100 * df_aux['Kg of Fat 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    loc = MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    ax.axvline(new_scale_date, color='black', linewidth=1)

    ax.set(title='Kg of Fat',
           xlabel=None,
           ylabel=r'Kg')

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Blood Pressure =====
    df_aux = df[(df['Type'] == 'Systolic') | (df['Type'] == 'Diastolic')]
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').mean()
    df_aux = df_aux.interpolate()
    df_aux = df_aux.fillna(method='ffill')
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['Systolic 7DMA'] = df_aux['Systolic'].rolling(7).mean()
    df_aux['Systolic 30DMA'] = df_aux['Systolic'].rolling(30).mean()
    df_aux['Diastolic 7DMA'] = df_aux['Diastolic'].rolling(7).mean()
    df_aux['Diastolic 30DMA'] = df_aux['Diastolic'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(df_aux['Systolic'], linewidth=0, color='blue', alpha=0.5, marker='o', markeredgecolor='white')
    ax.plot(df_aux['Systolic 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['Systolic 30DMA'], linewidth=3, color='navy')
    ax.plot(df_aux['Diastolic'], linewidth=0, color='red', alpha=0.5, marker='o', markeredgecolor='white')
    ax.plot(df_aux['Diastolic 7DMA'], linewidth=3, color='red')
    ax.plot(df_aux['Diastolic 30DMA'], linewidth=3, color='darkred')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    ax.set(title='Blood Pressure',
           xlabel=None,
           ylabel=None)

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Step Count =====
    df_aux = df[df['Type'] == 'Step']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').sum().fillna(method='ffill')
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['Step 7DMA'] = df_aux['Step'].rolling(7).mean()
    df_aux['Step 30DMA'] = df_aux['Step'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.bar(df_aux['Step'].index, df_aux['Step'].values, color='blue',
           alpha=0.5, edgecolor=None, width=1)
    ax.plot(df_aux['Step 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['Step 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    ax.set(title='Step Count',
           xlabel=None,
           ylabel=None)

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    loc = MultipleLocator(base=5000)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Distance Walk+Run =====
    df_aux = df[df['Type'] == 'Distance Walk+Run']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').sum()
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['Distance Walk+Run 7DMA'] = df_aux['Distance Walk+Run'].rolling(7).mean()
    df_aux['Distance Walk+Run 30DMA'] = df_aux['Distance Walk+Run'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.bar(df_aux['Distance Walk+Run'].index, df_aux['Distance Walk+Run'].values,
           color='blue', alpha=0.5, width=1)
    ax.plot(df_aux['Distance Walk+Run 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['Distance Walk+Run 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    loc = MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    ax.set(title='Walking + Running Distance',
           xlabel=None,
           ylabel='Kilometers')

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Cycling Distance =====
    df_aux = df[df['Type'] == 'Distance Cycling']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').sum().fillna(0)
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['Distance Cycling 7DMA'] = df_aux['Distance Cycling'].rolling(7).mean()
    df_aux['Distance Cycling 30DMA'] = df_aux['Distance Cycling'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.bar(df_aux['Distance Cycling'].index, df_aux['Distance Cycling'].values,
           color='blue', alpha=0.5, width=1)
    ax.plot(df_aux['Distance Cycling 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['Distance Cycling 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    loc = MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    ax.set(title='Cycling Distance',
           xlabel=None,
           ylabel='Kilometers')

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, 20))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Exercise Time =====
    df_aux = df[df['Type'] == 'Exercise Time']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').sum()
    df_aux = df_aux[df_aux.index >= '2020-01-01']
    df_aux['Exercise Time 7DMA'] = df_aux['Exercise Time'].fillna(method='ffill').rolling(7).mean()
    df_aux['Exercise Time 30DMA'] = df_aux['Exercise Time'].fillna(method='ffill').rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.bar(df_aux['Exercise Time'].index, df_aux['Exercise Time'].values,
           color='blue', alpha=0.5, width=1)
    ax.plot(df_aux['Exercise Time 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['Exercise Time 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    ax.set(title='Exercise Time',
           xlabel=None,
           ylabel='Minutes')

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    loc = MultipleLocator(base=10)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Heart Rate =====
    df_hr = df[df['Type'] == 'Heart Rate']
    df_hr = pd.pivot_table(df_hr, 'Value', 'End', 'Type')
    df_hr = df_hr.resample('D').mean()
    df_hr = df_hr[df_hr.index >= '2020-01-01']
    df_hr['Heart Rate MA'] = df_hr['Heart Rate'].fillna(method='ffill').rolling(30).mean()

    df_rhr = df[df['Type'] == 'Resting Heart Rate']
    df_rhr = pd.pivot_table(df_rhr, 'Value', 'End', 'Type')
    df_rhr = df_rhr.resample('D').mean()
    df_rhr = df_rhr[df_rhr.index >= '2020-01-01']
    df_rhr['Resting Heart Rate MA'] = df_rhr['Resting Heart Rate'].fillna(method='ffill').rolling(30).mean()

    df_whr = df[df['Type'] == 'Walking Heart Rate']
    df_whr = pd.pivot_table(df_whr, 'Value', 'End', 'Type')
    df_whr = df_whr.resample('D').mean()
    df_whr = df_whr[df_whr.index >= '2020-01-01']
    df_whr['Walking Heart Rate MA'] = df_whr['Walking Heart Rate'].fillna(method='ffill').rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(df_hr['Heart Rate'], color='red', alpha=0.3, linewidth=1)
    ax.plot(df_hr['Heart Rate MA'], linewidth=3, color='red', label='Average')

    ax.plot(df_rhr['Resting Heart Rate'], color='blue', alpha=0.3, linewidth=1)
    ax.plot(df_rhr['Resting Heart Rate MA'], linewidth=3, color='blue', label='Resting')

    ax.plot(df_whr['Walking Heart Rate'], color='green', alpha=0.3, linewidth=1)
    ax.plot(df_whr['Walking Heart Rate MA'], linewidth=3, color='green', label='Walking')

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    y1, y2 = ax.get_ylim()

    plt.legend(loc='upper left')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    loc = MultipleLocator(base=5.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    ax.set(title='Heart Rate',
           xlabel=None,
           ylabel='Beats per Minute')

    x_max, x_min = df_hr.dropna(how='all').index.max(), df_hr.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

    # ===== Waist Circumference =====
    df_aux = df[df['Type'] == 'Waist Circumference']
    df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
    df_aux = df_aux.resample('D').mean()
    df_aux = df_aux.interpolate()
    df_aux = df_aux.fillna(method='ffill')
    df_aux['Waist 7DMA'] = df_aux['Waist Circumference'].rolling(7).mean()
    df_aux['Waist 30DMA'] = df_aux['Waist Circumference'].rolling(30).mean()

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(df_aux['Waist Circumference'], linewidth=0, color='blue', alpha=0.5, marker='o', markeredgecolor='white')
    ax.plot(df_aux['Waist 7DMA'], linewidth=3, color='blue')
    ax.plot(df_aux['Waist 30DMA'], linewidth=3, color='red')

    y1, y2 = ax.get_ylim()

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    ax.set(title='Waist Circumference',
           xlabel=None,
           ylabel='centimeters')

    loc = MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)

    x_max, x_min = df_aux.dropna(how='all').index.max(), df_aux.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()
    plt.ylim((y1, y2))

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()
