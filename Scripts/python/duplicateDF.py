import pandas as pd

# create a sample dataframe
df = pd.DataFrame({'A': [1, 2, 2, 3, 4, 5, 5],
                   'B': [1, 2, 2, 3, 4, 4, 5],
                   'C': [1, 2, 2, 3, 4, 5, 5]})

# find duplicates
duplicates = df.duplicated()

# display the original dataframe with duplicates marked
print(df)
print()
print(duplicates)
print('\n')
duplicate_rows = df[duplicates]
print(duplicate_rows)
