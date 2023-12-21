# Smartsheet of Kyle

It was created Khang Vuong

## Examples of How To Use

Ksheet

```python

from Kyle_Smartsheet import KSheet

sheet = KSheet(SheetID,token)
# Get dataframe
df = sheet.get_dataframe()
# Get column ID
columnID = sheet.get_columnID()
# Get column type
columntype = sheet.get_columnType()
# Convert df to dictionary
dic = convert_df_to_dict(df)
# Add rows
sheet.add_rows(df)
# Update rows
sheet.update_rows(df,list_rowID)
# Delete rows
sheet.delete_rows(df,lst_rowID)

```

KSmartsheet

```python

from Kyle_Smartsheet import KSmartsheet

smart = KSmartSheet(token).smart

```