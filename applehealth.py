import pandas as pd
import xml.etree.cElementTree as et
from tqdm import tqdm
import matplotlib.pyplot as plt

DATETIME_KEYS = ['startDate', 'endDate']
NUMERIC_KEYS = ['value']
OTHER_KEYS = ['type', 'sourceName', 'unit', 'device']

xtree = et.parse(r'C:\Users\gamarante\Desktop\export.xml')
xroot = xtree.getroot()

df = pd.DataFrame(columns=['Type', 'Source', 'Unit', 'Start', 'End', 'Value'])

for node in tqdm(xroot, 'Processing'):
    if node.tag == 'Record':
        type = node.attrib['type']
        sourceName = node.attrib['sourceName']
        unit = node.attrib['unit']
        startDate = node.attrib['startDate']
        endDate = node.attrib['endDate']
        value = node.attrib['value']

        df = df.append({'Type': type, 'Source': sourceName, 'Unit': unit, 'Start': startDate, 'End': endDate, 'Value': value}, ignore_index=True)


writer = pd.ExcelWriter(r'C:\Users\gamarante\Desktop\HealtData.xlsx')
df.to_excel(writer)
writer.save()
