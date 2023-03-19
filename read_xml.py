import xml.etree.ElementTree as etree
from dateutil.parser import parse
import re
import os
import pandas as pd
from tqdm import tqdm
from time import time
tic = time()


export_path = '/Users/gustavoamarante/Downloads/apple_health_export/export.xml'
var2skip = ['DietaryWater', 'HeartRate', 'LeanBodyMass', 'BasalEnergyBurned',
            'ActiveEnergyBurned', 'RespiratoryRate', 'DietaryFatTotal',
            'DietaryFatPolyunsaturated', 'DietaryFatMonounsaturated', 'DietaryFatSaturated',
            'DietaryCholesterol', 'DietarySodium', 'DietaryCarbohydrates',
            'DietaryFiber', 'DietarySugar', 'DietaryEnergyConsumed',
            'DietaryProtein', 'DietaryVitaminB6', 'DietaryVitaminE',
            'DietaryCalcium', 'DietaryIron', 'DietaryThiamin', 'DietaryNiacin',
            'DietaryFolate', 'DietaryPhosphorus', 'DietaryMagnesium', 'DietaryZinc',
            'DietarySelenium', 'DietaryCopper', 'DietaryPotassium', 'SwimmingStrokeCount',
            'VO2Max', 'EnvironmentalAudioExposure', 'HeadphoneAudioExposure',
            'WalkingDoubleSupportPercentage', 'SixMinuteWalkTestDistance',
            'WalkingStepLength', 'WalkingAsymmetryPercentage', 'HKDataTypeSleepDurationGoal',
            'AppleWalkingSteadiness', 'HeartRateRecoveryOneMinute', 'SleepAnalysis',
            'MindfulSession', 'HighHeartRateEvent', 'AudioExposureEvent', 'HandwashingEvent',
            'HeartRateVariabilitySDNN']

formatted_records = []
total_count = 0
PREFIX_RE = re.compile('HK.*Identifier(.+)$')


def try_to_float(v):
    """convert v to float or 0"""
    try:
        return float(v)
    except ValueError:
        try:
            return int(v)
        except:
            return 0


def format_record(record):
    """format a export health xml record for influx"""
    m = re.match(PREFIX_RE, record.get("type"))
    measurement = m.group(1) if m else record.get("type")
    value = try_to_float(record.get("value", 1))
    unit = record.get("unit", "unit")
    date = pd.to_datetime(record.get("startDate")).tz_localize(None)

    series = pd.Series(name=measurement, index=[date], data=value)

    return series


df = pd.DataFrame()
for _, elem in tqdm(etree.iterparse(export_path)):
    if elem.tag == "Record":
        f = format_record(elem)
        if not (f.name in var2skip):
            # print(f.name)
            df.loc[f.index[0], f.name] = f.values[0]
        del elem


cwd = os.getcwd()
store = pd.HDFStore(cwd + r'/health_data.h5')
store['health'] = df
store.close()

toc = time()
print(round((toc - tic)/60, 1), 'minutes')
