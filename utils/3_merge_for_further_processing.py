import pandas as pd

oldest_file_path = '2023-03-27-otodom-merged_file_for_next_update.csv'
updated_data_path = '2024-04-07-otodom-updated_data.csv'
new_data_path = '2024-04-07-otodom-new_data.csv'

oldest_file = pd.read_csv(oldest_file_path)
updated_data = pd.read_csv(updated_data_path)
new_data = pd.read_csv(new_data_path)


def set_url_as_index(df):
    if 'url' in df.columns:
        df.set_index('url', inplace=True)
    else:
        raise ValueError("URL column not found. Please check the column names.")


try:
    set_url_as_index(oldest_file)
    set_url_as_index(updated_data)
    set_url_as_index(new_data)
except ValueError as e:
    print(e)

oldest_file.update(updated_data)

merged_file = pd.concat([oldest_file, new_data], axis=0)

merged_file.reset_index(inplace=True)

merged_file_path = '2024-04-07-otodom-merged_file_for_further_processing.csv'
merged_file.to_csv(merged_file_path, index=False)

merged_file_path