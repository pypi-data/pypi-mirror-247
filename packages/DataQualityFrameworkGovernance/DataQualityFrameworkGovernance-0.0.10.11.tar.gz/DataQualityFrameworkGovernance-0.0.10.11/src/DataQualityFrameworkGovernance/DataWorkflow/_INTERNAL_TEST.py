import pandas as pd
import statistics

# List of Tuples
employees = [
            ('Saumya', 32, 'Delhi',70),
            ('Saumya', 32, 'Delhi',20),
            ('Saumya', 32, (None),10),
            ('Aaditya', 40, (None),89),
            ('Seema', 32, 'Delhi',(None))
            ]

df = pd.DataFrame(employees,
                  columns = ['Name', 'Age', 'City','Score'])

import _Completeness as cp
#print(cp.missing_values_in_dataset(df,"Yes"))

#print('Invalid')
#print(df.isnull().sum())
#print('Valid')
#print(len(df) - df.isnull().sum())

print((len(df) * len(df.columns)) - df.isnull().sum().sum())
print(df.isnull().sum().sum())
print(statistics.mean((len(df) - df.isnull().sum()) / len(df)))