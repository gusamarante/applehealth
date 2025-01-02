"""
In construction
"""

from xmltodict import parse
import pandas as pd
from time import time

file_name = "/Users/gamarante/Downloads/apple_health_export/export.xml"

print("Reading File")
tic = time()
with open(file_name, "r", encoding="utf-8") as file:
    data = parse(file.read())
print("Finished Reading File", time() - tic)


print("Start Pandasing")
tic = time()
records = data["HealthData"]["Record"]
df = pd.DataFrame(records)
print("Finished Pandasing", time() - tic)


print(df.head())