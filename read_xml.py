import xml.etree.ElementTree as ET
from tqdm import tqdm
from time import time
import pandas as pd
import sys
import re
import os

tic = time()

# Read the file
xml_string = open("/Users/gustavoamarante/Downloads/apple_health_export/export.xml").read()

print("Pre-processing...", end="")
sys.stdout.flush()
start_strip = re.search('<!DOCTYPE', xml_string).span()[0]
end_strip = re.search(']>', xml_string).span()[1]
xml_string = xml_string[:start_strip] + xml_string[end_strip:]
xml_string = xml_string.replace("\x0b", "")
print("done!")

# Process the XML
sys.stdout.flush()

etree = ET.ElementTree(ET.fromstring(xml_string))
attribute_list = []

for child in tqdm(etree.getroot(), 'Processing XML'):
    child_attrib = child.attrib
    for metadata_entry in list(child):
        metadata_values = list(metadata_entry.attrib.values())
        if len(metadata_values) == 2:
            metadata_dict = {metadata_values[0]: metadata_values[1]}
            child_attrib.update(metadata_dict)

    attribute_list.append(child_attrib)

health_df = pd.DataFrame(attribute_list)

# Every health data type and some columns have a long identifer
# Removing these for readability
health_df.type = health_df.type.str.replace('HKQuantityTypeIdentifier', "")
health_df.type = health_df.type.str.replace('HKCategoryTypeIdentifier', "")
health_df.columns = health_df.columns.str.replace("HKCharacteristicTypeIdentifier", "")

# Reorder some of the columns for easier visual data review
original_cols = list(health_df)
shifted_cols = ['type',
                'sourceName',
                'value',
                'unit',
                'startDate',
                'endDate',
                'creationDate']

# Add loop specific column ordering if metadata entries exist
if 'com.loopkit.InsulinKit.MetadataKeyProgrammedTempBasalRate' in original_cols:
    shifted_cols.append(
        'com.loopkit.InsulinKit.MetadataKeyProgrammedTempBasalRate')

if 'com.loopkit.InsulinKit.MetadataKeyScheduledBasalRate' in original_cols:
    shifted_cols.append(
        'com.loopkit.InsulinKit.MetadataKeyScheduledBasalRate')

if 'com.loudnate.CarbKit.HKMetadataKey.AbsorptionTimeMinutes' in original_cols:
    shifted_cols.append(
        'com.loudnate.CarbKit.HKMetadataKey.AbsorptionTimeMinutes')

remaining_cols = list(set(original_cols) - set(shifted_cols))
reordered_cols = shifted_cols + remaining_cols
health_df = health_df.reindex(labels=reordered_cols, axis='columns')

# Sort by newest data first
health_df.sort_values(by='startDate', ascending=False, inplace=True)

# Variables to Keep
var2keep = ['HeartRate',
            'StepCount',
            'DistanceWalkingRunning',
            'WalkingStepLength',
            'WalkingDoubleSupportPercentage',
            'WalkingSpeed',
            'AppleExerciseTime',
            'WalkingAsymmetryPercentage',
            'FlightsClimbed',
            'NumberOfAlcoholicBeverages',
            'DistanceCycling',
            'WalkingHeartRateAverage',
            'RestingHeartRate',
            'WaistCircumference',
            'BloodPressureDiastolic',
            'BloodPressureSystolic',
            'BodyMass',
            'LeanBodyMass',
            'BodyFatPercentage',
            'BodyMassIndex',
            'HeartRateRecoveryOneMinute',
            'DistanceSwimming',
            'SwimmingStrokeCount']

health_df = health_df[health_df['type'].isin(var2keep)]
health_df = health_df[['type', 'value', 'unit', 'endDate']]

toc = time()

# Save data
cwd = os.getcwd()
store = pd.HDFStore(cwd + r'/health_data.h5')
store['health'] = health_df
store.close()

print(round((toc - tic)/60, 1), 'minutes')
