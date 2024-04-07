import json
import csv

json_files = ['results.json']

csv_file = '2024-04-07-otodom_full_raw_dataset.csv'

all_columns = [
    'url', 'name/title', 'address', 'price', 'area', 'price-per-area',
    'floor/store', 'no of rooms', 'year of construction', 'parking space',
    'market', 'form of ownership', 'condition', 'rent', 'heating',
    'advertiser type', 'elevator', 'outdoor area', 'building type',
    'building material'
]


with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_columns)
    
    writer.writeheader()
    
    processed_urls = set()
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for entry in data:
            url = entry['resultData']['data']['url']
            
            if url not in processed_urls:
                processed_urls.add(url)
                
                if entry['resultData']['data']['results']:
                    result = entry['resultData']['data']['results'][0]
                    result['url'] = url
                    
                    row = {column: result.get(column, None) for column in all_columns}
                    writer.writerow(row)
