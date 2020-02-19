import pandas as pd
import xml.etree.cElementTree as et
from tqdm import tqdm
import matplotlib.pyplot as plt
from time import time

tic = time()

DATETIME_KEYS = ['startDate', 'endDate']
NUMERIC_KEYS = ['value']
OTHER_KEYS = ['type', 'sourceName', 'unit']
ALL_KEYS = DATETIME_KEYS + NUMERIC_KEYS + OTHER_KEYS

xtree = et.parse(r'C:\Users\gamarante\Desktop\export.xml')
xroot = xtree.getroot()

df = pd.DataFrame([{key: r.get(key) for key in ALL_KEYS} for r in xroot if r.tag == 'Record'])

rename_dict = {'startDate': 'Start',
               'endDate': 'End',
               'value': 'Value',
               'type': 'Type',
               'sourceName': 'Source',
               'unit': 'Unit'}
df = df.rename(rename_dict, axis=1)

# Clean the "Value" Column
stood_dict = {'HKCategoryValueAppleStandHourStood': 1,
              'HKCategoryValueAppleStandHourIdle': 0,
              'HKCategoryValueSleepAnalysisAsleep': 1,
              'HKCategoryValueSleepAnalysisInBed': 0}

df['Value'] = df['Value'].replace(stood_dict)
df['Value'] = pd.to_numeric(df['Value'])

# Clean "Type" column
type_dict = {'HKQuantityTypeIdentifierHeight': 'Height',
             'HKQuantityTypeIdentifierBodyMass': 'Body Mass',
             'HKQuantityTypeIdentifierHeartRate': 'Heart Rate',
             'HKQuantityTypeIdentifierBloodPressureSystolic': 'Systolic',
             'HKQuantityTypeIdentifierBloodPressureDiastolic': 'Diastolic',
             'HKQuantityTypeIdentifierBodyFatPercentage': 'Body Fat Percentage',
             'HKQuantityTypeIdentifierStepCount': 'Step',
             'HKQuantityTypeIdentifierDistanceWalkingRunning': 'Distance Walk+Run',
             'HKQuantityTypeIdentifierBasalEnergyBurned': 'Basal Energy Burned',
             'HKQuantityTypeIdentifierActiveEnergyBurned': 'Active Energy Burned',
             'HKQuantityTypeIdentifierFlightsClimbed': 'Flights Climbed',
             'HKQuantityTypeIdentifierAppleExerciseTime': 'Exercise Time',
             'HKQuantityTypeIdentifierDistanceCycling': 'Distance Cycling',
             'HKQuantityTypeIdentifierRestingHeartRate': 'Resting Heart Rate',
             'HKQuantityTypeIdentifierVO2Max': 'VO2 Max',
             'HKQuantityTypeIdentifierWalkingHeartRateAverage': 'Walking Heart Rate Average',
             'HKQuantityTypeIdentifierEnvironmentalAudioExposure': 'Environment Audio Exposure',
             'HKQuantityTypeIdentifierHeadphoneAudioExposure': 'Headphone Audio Exposure',
             'HKQuantityTypeIdentifierAppleStandTime': 'Stand Time',
             'HKCategoryTypeIdentifierSleepAnalysis': 'Sleep Analysis',
             'HKCategoryTypeIdentifierAppleStandHour': 'Stand Hour',
             'HKCategoryTypeIdentifierMindfulSession': 'Mindfull Session',
             'HKQuantityTypeIdentifierHeartRateVariabilitySDNN': 'Heart Rate Variability',
             'HKQuantityTypeIdentifierBodyMassIndex': 'BMI'}

df = df[df['Type'].isin(type_dict.keys())]
df['Type'] = df['Type'].replace(type_dict)

# Clean dates columns
df['Start'] = pd.to_datetime(df['Start']).dt.tz_localize(None)
df['End'] = pd.to_datetime(df['End']).dt.tz_localize(None)

toc = time()

print(toc-tic, 'seconds')

# Systolic and Diastolic
df_aux = df[(df['Type'] == 'Systolic') | (df['Type'] == 'Diastolic')]
df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
df_aux = df_aux.resample('D').mean().fillna(method='ffill')
df_aux.plot(grid=True)
plt.show()

# Weight
df_aux = df[df['Type'] == 'Body Mass']
df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
df_aux['MA 30d'] = df_aux['Body Mass'].rolling('30d').mean()
df_aux.plot(grid=True)
plt.show()

# Body Fat Percentage
df_aux = df[df['Type'] == 'Body Fat Percentage']
df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
df_aux['MA 30d'] = df_aux['Body Fat Percentage'].rolling('30d').mean()
df_aux.plot(grid=True)
plt.show()

# Step
df_aux = df[df['Type'] == 'Step']
df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
df_aux = df_aux.resample('M').sum()
df_aux.plot(grid=True, kind='bar')
plt.show()

# Distance Walk+Run
df_aux = df[df['Type'] == 'Distance Walk+Run']
df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
df_aux = df_aux.resample('D').sum().resample('M').mean()
df_aux.plot(grid=True, kind='bar')
plt.show()

# Distance Cycling
df_aux = df[df['Type'] == 'Distance Cycling']
df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
df_aux = df_aux.resample('D').sum().resample('M').mean()
df_aux.plot(grid=True, kind='bar')
plt.show()

# Stand Time
df_aux = df[df['Type'] == 'Stand Time']
df_aux = pd.pivot_table(df_aux, 'Value', 'End', 'Type')
df_aux = df_aux.resample('H').sum()
df_aux['Hour'] = df_aux.index.hour
df_aux = df_aux.groupby('Hour').mean()
df_aux.plot(grid=True, kind='bar')
plt.show()

# Mindfull Session
df_aux = df[df['Type'] == 'Mindfull Session']
df_aux['Minutes'] = (df['End'] - df['Start']).dt.total_seconds() / 60
df_aux = pd.pivot_table(df_aux, 'Minutes', 'End')
df_aux = df_aux.resample('D').sum().resample('W').mean()
df_aux.plot(grid=True, kind='bar')
plt.show()

# BMI
# Heart Rate
# Basal Energy Burned
# Active Energy Burned
# Flights Climbed
# Exercise Time
# Resting Heart Rate
# VO2 Max
# Walking Heart Rate Average
# Environment Audio Exposure
# Headphone Audio Exposure
# Sleep Analysis
# Heart Rate Variability

# writer = pd.ExcelWriter(r'C:\Users\gamarante\Desktop\HealtData.xlsx')
# df.to_excel(writer)
# writer.save()
