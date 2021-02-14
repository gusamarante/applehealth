import pandas as pd
import xml.etree.cElementTree as et
from tqdm import tqdm
import matplotlib.pyplot as plt
from time import time
import os

tic = time()

DATETIME_KEYS = ['startDate', 'endDate']
NUMERIC_KEYS = ['value']
OTHER_KEYS = ['type', 'sourceName', 'unit']
ALL_KEYS = DATETIME_KEYS + NUMERIC_KEYS + OTHER_KEYS

xtree = et.parse(r'/Users/gustavoamarante/Downloads/apple_health_export/export.xml')
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
              'HKCategoryValueSleepAnalysisInBed': 0,
              'HKCategoryValueEnvironmentalAudioExposureEventMomentaryLimit': 1}

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

cwd = os.getcwd()
store = pd.HDFStore(cwd + r'/health_data.h5')
store['health'] = df
store.close()
toc = time()

print(toc-tic, 'seconds')
