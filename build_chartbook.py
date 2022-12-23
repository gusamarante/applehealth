import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.backends.backend_pdf import PdfPages
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

chart_size = (15, 7)
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

# Parameters
title_dict = {'AppleExerciseTime': 'Exercise Time',
              'BodyFatPercentage': 'Body Fat Percentage',
              'BodyMass': 'Weight',
              'BodyMassIndex': 'BMI',
              'DistanceCycling': 'Cycling Distance',
              'DistanceSwimming': 'Swimming Distance',
              'DistanceWalkingRunning': 'Walking + Running Distance',
              'NumberOfAlcoholicBeverages': 'Number of Alcoholic Drinks',
              'StepCount': 'Step Count',
              'WaistCircumference': 'Waist Circumference'}

resample_dict = {'AppleExerciseTime': 'sum',
                 'BodyFatPercentage': 'mean',
                 'BodyMass': 'mean',
                 'BodyMassIndex': 'mean',
                 'DistanceCycling': 'sum',
                 'DistanceSwimming': 'sum',
                 'DistanceWalkingRunning': 'sum',
                 'NumberOfAlcoholicBeverages': 'sum',
                 'StepCount': 'sum',
                 'WaistCircumference': 'mean'}

interpolate_dict = {'AppleExerciseTime': 'zeros',
                    'BodyFatPercentage': 'linear',
                    'BodyMass': 'linear',
                    'BodyMassIndex': 'linear',
                    'DistanceCycling': 'zeros',
                    'DistanceSwimming': 'zeros',
                    'DistanceWalkingRunning': 'zeros',
                    'NumberOfAlcoholicBeverages': 'zeros',
                    'StepCount': 'zeros',
                    'WaistCircumference': 'linear'}

unit_dict = {'AppleExerciseTime': 'Minutes',
             'BodyFatPercentage': 'Percent',
             'BodyMass': 'Kilograms',
             'BodyMassIndex': '',
             'DistanceCycling': 'Kilometers',
             'DistanceSwimming': 'Meters',
             'DistanceWalkingRunning': 'Kilometers',
             'NumberOfAlcoholicBeverages': '',
             'StepCount': '',
             'WaistCircumference': ''}

locator_dict = {'AppleExerciseTime': 10,
                'BodyFatPercentage': 1,
                'BodyMass': 1,
                'BodyMassIndex': 0.5,
                'DistanceCycling': 5,
                'DistanceSwimming': 100,
                'DistanceWalkingRunning': 5,
                'HeartRateRecoveryOneMinute': 1,
                'NumberOfAlcoholicBeverages': 1,
                'StepCount': 2000,
                'WaistCircumference': 1}

# Read data
df = pd.read_hdf('health_data.h5', 'health')
df['value'] = df['value'].astype(float)
df['endDate'] = pd.to_datetime(df['endDate'])
df = pd.pivot_table(df, index='endDate', columns='type', values='value', aggfunc='mean')

with PdfPages('health_chartbook.pdf') as pdf:

    for var in tqdm(df.columns, 'Building Charts'):

        if var not in title_dict.keys():
            continue

        aux = df[var].to_frame(title_dict[var])
        aux = aux.dropna()

        # Resample
        if resample_dict[var] == 'sum':
            aux = aux.resample('D').sum()
        elif resample_dict[var] == 'mean':
            aux = aux.resample('D').mean()
        else:
            raise ValueError(f'Missing resample parameter for {var}')

        # Interpolation
        if interpolate_dict[var] == 'zeros':
            aux = aux.fillna(0)
        elif interpolate_dict[var] == 'linear':
            aux = aux.interpolate(limit_area='inside')
            aux = aux.fillna(method='ffill')
        else:
            raise ValueError(f'Missing interpolation parameter for {var}')

        # Percent Scaling
        if unit_dict[var] == 'Percent':
            aux = aux * 100

        aux = aux[aux.index >= '2020-01-01']
        aux[title_dict[var] + ' 7DMA'] = aux[title_dict[var]].rolling(7).mean()
        aux[title_dict[var] + ' 30DMA'] = aux[title_dict[var]].rolling(30).mean()

        fig, ax = plt.subplots(figsize=chart_size)
        ax.plot(aux[title_dict[var]], linewidth=0, color='blue', alpha=0.3, marker='o', markeredgecolor='white')
        ax.plot(aux[title_dict[var] + ' 7DMA'], linewidth=2, color='blue')
        ax.plot(aux[title_dict[var] + ' 30DMA'], linewidth=3, color='red')

        # y1, y2 = ax.get_ylim()

        ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

        ax.set(title=title_dict[var],
               xlabel=None,
               ylabel=unit_dict[var])

        loc = MultipleLocator(base=locator_dict[var])  # this locator puts ticks at regular intervals
        ax.yaxis.set_major_locator(loc)

        # Add a line to relevant dates
        # ax.axvline(new_scale_date, color='black', linewidth=1)

        x_max, x_min = aux.dropna(how='all').index.max(), aux.index.dropna(how='all').min()
        plt.xlim(x_min, x_max + pd.offsets.Day(10))

        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()

        plt.tight_layout()
        # plt.ylim((y1, y2))

        pdf.savefig(fig)

        if show_charts:
            plt.show()

        plt.close()

    # Blood Preassure
    df_bp = pd.DataFrame()
    df_bp['Systolic'] = df['BloodPressureSystolic'].resample('D').mean().interpolate(limit_area='inside')
    df_bp['Diastolic'] = df['BloodPressureDiastolic'].resample('D').mean().interpolate(limit_area='inside')

    df_bp['Systolic 30DMA'] = df_bp['Systolic'].rolling(30).mean()
    df_bp['Diastolic 30DMA'] = df_bp['Diastolic'].rolling(30).mean()

    df_bp['Systolic std'] = df_bp['Systolic'].rolling(30).std()
    df_bp['Diastolic std'] = df_bp['Diastolic'].rolling(30).std()

    df_bp = df_bp.dropna(how='all')

    fig, ax = plt.subplots(figsize=chart_size)
    ax.plot(df_bp['Systolic'], linewidth=0, color='blue', alpha=0.3, marker='o', markeredgecolor='white')
    ax.plot(df_bp['Diastolic'], linewidth=0, color='red', alpha=0.3, marker='o', markeredgecolor='white')

    ax.plot(df_bp['Systolic 30DMA'], linewidth=3, color='blue')
    ax.plot(df_bp['Diastolic 30DMA'], linewidth=3, color='red')

    plt.fill_between(x=df_bp.index,
                     y1=df_bp['Systolic 30DMA'] + 1.68 * df_bp['Systolic std'],
                     y2=df_bp['Systolic 30DMA'] - 1.68 * df_bp['Systolic std'],
                     alpha=0.3, color='blue', edgecolor=None)

    plt.fill_between(x=df_bp.index,
                     y1=df_bp['Diastolic 30DMA'] + 1.68 * df_bp['Diastolic std'],
                     y2=df_bp['Diastolic 30DMA'] - 1.68 * df_bp['Diastolic std'],
                     alpha=0.3, color='red', edgecolor=None)

    ax.yaxis.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.6)

    ax.set(title='Blood Pressure')

    loc = MultipleLocator(base=10)
    ax.yaxis.set_major_locator(loc)

    x_max, x_min = df_bp.dropna(how='all').index.max(), df_bp.index.dropna(how='all').min()
    plt.xlim(x_min, x_max + pd.offsets.Day(10))

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.tight_layout()

    pdf.savefig(fig)

    if show_charts:
        plt.show()

    plt.close()

# ====== Special Charts =====
# 'HeartRate': '',
# 'RestingHeartRate': '',
# 'WalkingHeartRateAverage': '',
