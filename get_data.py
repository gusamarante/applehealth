import xmltodict
from time import time
import pandas as pd
import os

tic = time()

file_name = "C:/Users/gamarante/Dropbox/export.xml"  # BWGI
with open(file_name) as file:
    xml = xmltodict.parse(file.read())
    data = xml["HealthData"]

print('Data Keys', data.keys())

# ===== Records =====
records = pd.DataFrame(data['Record'])

# Columns
# '@type', '@sourceName', '@sourceVersion', '@unit', '@creationDate',
#        '@startDate', '@endDate', '@value', 'MetadataEntry', '@device',
#        'HeartRateVariabilityMetadataList'

fields2keep = [
    'HKQuantityTypeIdentifierBodyMass',
    # 'HKQuantityTypeIdentifierHeartRate',
    'HKQuantityTypeIdentifierBloodPressureSystolic',
    'HKQuantityTypeIdentifierBloodPressureDiastolic',
    'HKQuantityTypeIdentifierBodyFatPercentage',
    # 'HKQuantityTypeIdentifierLeanBodyMass',
    # 'HKQuantityTypeIdentifierStepCount',
    'HKQuantityTypeIdentifierDistanceWalkingRunning',
    # 'HKQuantityTypeIdentifierActiveEnergyBurned',
    'HKQuantityTypeIdentifierAppleExerciseTime',
    # 'HKQuantityTypeIdentifierDistanceCycling',
    # 'HKQuantityTypeIdentifierDistanceSwimming',
    # 'HKQuantityTypeIdentifierWaistCircumference',
    # 'HKQuantityTypeIdentifierRestingHeartRate',
    # 'HKQuantityTypeIdentifierVO2Max',
    # 'HKQuantityTypeIdentifierWalkingHeartRateAverage',
    # 'HKQuantityTypeIdentifierNumberOfAlcoholicBeverages',
]

print(records.shape[0], 'before filter')
records = records[records['@type'].isin(fields2keep)]
print(records.shape[0], 'After filter')

# Save data to HDF5
print('saving...')
cwd = os.getcwd()
store = pd.HDFStore(cwd + r'/health_data.h5')
store['health'] = records
store.close()

print(time() - tic)
