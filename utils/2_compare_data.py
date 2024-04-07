import pandas as pd

old_file = pd.read_csv('2023-03-27-merged_file_for_next_update.csv', header=0)
new_file = pd.read_csv('2024-04-07-otodom_full_raw_dataset.csv', header=0)

old_file.set_index('url', inplace=True)
new_file.set_index('url', inplace=True)

new_data = new_file.loc[~new_file.index.isin(old_file.index)]
deleted_data = old_file.loc[~old_file.index.isin(new_file.index)]

new_data.reset_index().to_csv('new_data.csv', index=False)
deleted_data.reset_index().to_csv('deleted_data.csv', index=False)

common_keys = old_file.index.intersection(new_file.index)
updated_rows = []

for key in common_keys:
    if not old_file.loc[key].equals(new_file.loc[key]):
        updated_rows.append(new_file.loc[key])

if updated_rows:
    updated_data = pd.concat(updated_rows, axis=1).transpose()
    updated_data.reset_index().rename(columns={'index': 'url'}).to_csv('updated_data.csv', index=False) 
else:
    print("No updated data found.")
