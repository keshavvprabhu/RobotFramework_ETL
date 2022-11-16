import csv
import json
import os
import pandas as pd
countries_json_path = r'D:\countries.json'

df = pd.read_json(countries_json_path)
df.to_csv(r'D:\coutries.csv', index=False, header=True, quoting=csv.QUOTE_MINIMAL)

