import pandas as pd
from unicodedata import normalize

db = pd.read_csv('unica.csv', encoding='latin-1')
string = 'cort'
string = string.upper()

db = db[db['ENTIDAD'].str.contains(string)]
print(db)