
import pandas as pd

from  config import VULNERABILITIES_CSV

df=pd.read_csv(VULNERABILITIES_CSV  ) 

print("leng of rows",len(df))
print("columns",df.columns.to_list())
print(df.head(3))