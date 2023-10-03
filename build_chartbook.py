import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


show_charts = True

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
nosugardate = '2023-10-02'

# Chart Parameters
size = 7
chart_shape = (size * (16 / 9), size)

# Read data
df = pd.DataFrame(pd.read_hdf('health_data.h5', 'health'))
df = df[['@type', '@unit', '@startDate', '@value']]
df['@value'] = df['@value'].astype(float)
df['@startDate'] = pd.to_datetime(df['@startDate']).dt.tz_localize(None)

rename = {'@type': 'Type',
          '@unit': 'Unit',
          '@startDate': 'Date',
          '@value': 'Value'}
df = df.rename(rename, axis=1)

# Rename Types
replace = {
    'HKQuantityTypeIdentifierBodyMass': 'Weight',
    'HKQuantityTypeIdentifierBodyFatPercentage': 'Body Fat Percentage',
    'HKQuantityTypeIdentifierDistanceWalkingRunning': 'Walk+Run Distance',
    'HKQuantityTypeIdentifierAppleExerciseTime': 'Exercise Time',
    'HKQuantityTypeIdentifierBloodPressureSystolic': 'Systolic',
    'HKQuantityTypeIdentifierBloodPressureDiastolic': 'Diastolic',
    'HKQuantityTypeIdentifierStepCount': 'Steps',
    'HKQuantityTypeIdentifierWaistCircumference': 'Waist Circumference',
    'HKQuantityTypeIdentifierDistanceCycling': 'Distance Cycling',
    'HKQuantityTypeIdentifierLeanBodyMass': 'Lean Body Mass',
}
df['Type'] = df['Type'].replace(replace)

# Pivot
df = pd.pivot_table(df, index='Date', columns='Type', values='Value', aggfunc='mean')


# ==================
# ===== Charts =====
# ==================
with PdfPages('/Users/gamarante/Dropbox/health_chartbook.pdf') as pdf:
    # ===== WEIGHT =====
    col_name = 'Weight'
    s2plot = df[col_name].resample('D').mean()
    s2plot = s2plot.interpolate(limit_area='inside').to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()
    s2plot = s2plot[s2plot.index >= '2019-11-01']

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.plot(s2plot[col_name], linewidth=0, color='tab:blue', alpha=0.3, marker='o', markeredgecolor='white',
            label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='Kg')

    loc = MultipleLocator(base=1)
    ax.yaxis.set_major_locator(loc)

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== WAIST CIRCUMFERENCE =====
    col_name = 'Waist Circumference'
    s2plot = df[col_name].resample('D').mean()
    s2plot = s2plot.interpolate(limit_area='inside').to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()
    # s2plot = s2plot[s2plot.index >= '2019-11-01']

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.plot(s2plot[col_name], linewidth=0, color='tab:blue', alpha=0.3, marker='o', markeredgecolor='white',
            label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='Centimeters')

    loc = MultipleLocator(base=1)
    ax.yaxis.set_major_locator(loc)

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== BODY FAT PERCENTAGE =====
    col_name = 'Body Fat Percentage'
    s2plot = df[col_name].resample('D').mean() * 100
    s2plot = s2plot.interpolate(limit_area='inside').to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.plot(s2plot[col_name], linewidth=0, color='tab:blue', alpha=0.3, marker='o', markeredgecolor='white',
            label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='%')

    loc = MultipleLocator(base=1)
    ax.yaxis.set_major_locator(loc)

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== LEAN BODY MASS =====
    col_name = 'Lean Body Mass'
    s2plot = df[col_name].resample('D').mean()
    s2plot = s2plot.interpolate(limit_area='inside').to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()
    s2plot = s2plot[s2plot.index >= '2019-11-01']

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.plot(s2plot[col_name], linewidth=0, color='tab:blue', alpha=0.3, marker='o', markeredgecolor='white',
            label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='Kg')

    loc = MultipleLocator(base=1)
    ax.yaxis.set_major_locator(loc)

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== EXERCISE TIME =====
    col_name = 'Exercise Time'
    s2plot = df[col_name].resample('D').sum()
    s2plot = s2plot.fillna(0).to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot = s2plot[s2plot.index >= '2019-11-01']
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.plot(s2plot[col_name], linewidth=0, color='tab:blue', alpha=0.3, marker='o', markeredgecolor='white',
            label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='Minutes')

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, None)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== STEPS =====
    col_name = 'Steps'
    s2plot = df[col_name].resample('D').sum()
    s2plot = s2plot.fillna(0).to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot = s2plot[s2plot.index >= '2019-11-01']
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.bar(s2plot[col_name].index, s2plot[col_name].values, alpha=0.4, width=1, color='tab:blue', label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='Steps')

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, None)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    loc = MultipleLocator(base=5000)
    ax.yaxis.set_major_locator(loc)

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== WALK + RUN =====
    col_name = 'Walk+Run Distance'
    s2plot = df[col_name].resample('D').sum()
    s2plot = s2plot.fillna(0).to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot = s2plot[s2plot.index >= '2019-11-01']
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.bar(s2plot[col_name].index, s2plot[col_name].values, alpha=0.4, width=1, color='tab:blue', label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='Kilometers')

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, None)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== DISTANCE CYCLING =====
    col_name = 'Distance Cycling'
    s2plot = df[col_name].resample('D').sum()
    s2plot = s2plot.interpolate(limit_area='inside').to_frame(col_name)
    s2plot = s2plot.dropna()
    s2plot['7d MA'] = s2plot[col_name].rolling(7).mean()
    s2plot['30d MA'] = s2plot[col_name].rolling(30).mean()
    s2plot['365d MA'] = s2plot[col_name].rolling(365).mean()
    s2plot = s2plot[s2plot.index >= '2019-11-01']

    # Chart
    fig, ax = plt.subplots(figsize=chart_shape)
    ax.bar(s2plot[col_name].index, s2plot[col_name].values, alpha=0.4, width=1, color='tab:blue', label=col_name)
    ax.plot(s2plot['7d MA'], linewidth=2, color='tab:blue', label='7d MA')
    ax.plot(s2plot['30d MA'], linewidth=2, color='tab:orange', label='30d MA')
    ax.plot(s2plot['365d MA'], linewidth=2, color='tab:green', label='365d MA')

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title=col_name, ylabel='Km')

    x_max, x_min = s2plot.dropna(how='all').index.max(), s2plot.index.dropna(how='all').min()
    ax.set_xlim(x_min, x_max)

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.legend(loc='best', frameon=True)

    plt.tight_layout()
    pdf.savefig(fig)
    if show_charts:
        plt.show()

    plt.close()

    # ===== BLOOD PRESSURE =====
    df_bp = pd.DataFrame()
    df_bp['Systolic'] = df['Systolic'].resample('D').mean().interpolate(limit_area='inside')
    df_bp['Diastolic'] = df['Diastolic'].resample('D').mean().interpolate(limit_area='inside')

    df_bp['Systolic 30d MA'] = df_bp['Systolic'].rolling(30).mean()
    df_bp['Diastolic 30d MA'] = df_bp['Diastolic'].rolling(30).mean()

    df_bp['Systolic std'] = df_bp['Systolic'].rolling(30).std()
    df_bp['Diastolic std'] = df_bp['Diastolic'].rolling(30).std()

    df_bp = df_bp.dropna(how='all')

    fig, ax = plt.subplots(figsize=chart_shape)
    ax.plot(df_bp['Systolic'], linewidth=0, color='tab:blue', alpha=0.3, marker='o', markeredgecolor='white',
            label='Systolic')
    ax.plot(df_bp['Diastolic'], linewidth=0, color='tab:orange', alpha=0.3, marker='o', markeredgecolor='white',
            label='Diastolic')

    ax.plot(df_bp['Systolic 30d MA'], linewidth=3, color='tab:blue', label='Systolic 30d MA')
    ax.plot(df_bp['Diastolic 30d MA'], linewidth=3, color='tab:orange', label='Diastolic 30d MA')

    plt.fill_between(x=df_bp.index,
                     y1=df_bp['Systolic 30d MA'] + 1.68 * df_bp['Systolic std'],
                     y2=df_bp['Systolic 30d MA'] - 1.68 * df_bp['Systolic std'],
                     alpha=0.3, color='tab:blue', edgecolor=None)

    plt.fill_between(x=df_bp.index,
                     y1=df_bp['Diastolic 30d MA'] + 1.68 * df_bp['Diastolic std'],
                     y2=df_bp['Diastolic 30d MA'] - 1.68 * df_bp['Diastolic std'],
                     alpha=0.3, color='tab:orange', edgecolor=None)

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.xaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    ax.set(title='Blood Pressure')

    loc = MultipleLocator(base=10)
    ax.yaxis.set_major_locator(loc)

    x_max, x_min = df_bp.dropna(how='all').index.max(), df_bp.index.dropna(how='all').min()
    plt.xlim(x_min, x_max)

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    locators = mdates.YearLocator()
    ax.xaxis.set_major_locator(locators)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.legend(loc='best', frameon=True)

    plt.tight_layout()

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()
