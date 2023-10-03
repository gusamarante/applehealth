import xmltodict
from time import time
import pandas as pd
import os

tic = time()

file_name = "/Users/gustavoamarante/Downloads/apple_health_export/export.xml"
print('Parsing XML...')
with open(file_name) as file:
    xml = xmltodict.parse(file.read())
    data = xml["HealthData"]

print('Available Data Keys', data.keys())

# ===== Records =====
records = pd.DataFrame(data['Record'])

# Columns
# '@type', '@sourceName', '@sourceVersion', '@unit', '@creationDate',
#        '@startDate', '@endDate', '@value', 'MetadataEntry', '@device',
#        'HeartRateVariabilityMetadataList'

fields2keep = [
    'HKQuantityTypeIdentifierBodyMass',
    'HKQuantityTypeIdentifierBloodPressureSystolic',
    'HKQuantityTypeIdentifierBloodPressureDiastolic',
    'HKQuantityTypeIdentifierBodyFatPercentage',
    'HKQuantityTypeIdentifierStepCount',
    'HKQuantityTypeIdentifierDistanceWalkingRunning',
    'HKQuantityTypeIdentifierAppleExerciseTime',
    'HKQuantityTypeIdentifierWaistCircumference',
    'HKQuantityTypeIdentifierDistanceCycling',
    'HKQuantityTypeIdentifierLeanBodyMass',
    # 'HKQuantityTypeIdentifierHeartRate',
    # 'HKQuantityTypeIdentifierRestingHeartRate',
    # 'HKQuantityTypeIdentifierWalkingHeartRateAverage',
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

print(round((time() - tic)/60, 2), 'minutes')
