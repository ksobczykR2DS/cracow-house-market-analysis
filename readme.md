# Analysis of Real Estate Prices in Krakow
Project for the Data Exploration course conducted in the summer semester of the academic year 2023/2024 at the Faculty of Computer Science of the AGH University of Science and Technology in Krakow, under the supervision of Dr. Tomasz Pełecha-Pilichowski.

## Authors
Katarzyna Dębowska

Kacper Sobczyk

Piotr Urbańczyk

## Abstract
The project aims to understand the relationship between the characteristics of apartments and their asking prices in the local real estate market. As part of the work, we will conduct descriptive statistics, hedonic regression, and spatial analysis to identify the most important factors influencing apartment prices in Krakow.

### Data
**Dataset:** We used a dataset containing information about real estate sale offers.

**Data Source:** The data were extracted using automated methods from two popular real estate sales portals.

**Data Preparation:** Understanding the data, removing missing values, unification, format conversion, supplementing geographical data (coordinates) based on the address, adding a vector of distances from the city center (Main Market Square) based on geographical data, etc. — to be supplemented as the work progresses.

### Proposed Analyses and Modeling
Descriptive statistics, hedonic regression, correlation matrix (identifying factors affecting real estate prices), spatial analysis (geographically weighted regression [1]), etc. — to be supplemented after consultations and as the work progresses.

### Expected Results
Understanding which property features most influence the asking price of apartments in Krakow, detecting possible price trends in individual districts, etc. — to be supplemented as the work progresses.

## Table of Contents
### Understanding the Data
1.1. Data Collection

1.2. Data Description

1.3. Preliminary Data Quality Assessment

### Data Preparation
2.1. Operations on Columns

2.2. Examples of Applying Expert Knowledge

2.3. Data Quality Verification

2.4. Data Engineering

2.5. Data Exploration

### Data Analysis
3.1. Correlation Matrix (Pearson Matrix)

3.2. Analysis of Apartment Prices in Different Districts

3.3. Principal Component Analysis (PCA)

3.4. Feature Selection

### Modeling
4.1. SearchGrid

4.2. Selection of the Best Predictor

4.3. Model Evaluation Results

### Data Visualization in the Spatial Component

### Summary and Conclusions

 ---

## Understanding the Data
The project uses a dataset containing information about apartment sale offers in Krakow.

### Data Collection
#### Data Source
The data were obtained using automated methods from freely accessible sources — two popular real estate sales portals: [nieruchomości-online.pl](nieruchomości-online.pl) and [otodom.pl](otodom.pl).

#### Data Acquisition Methods
Both datasets were obtained using a professional dedicated solution for web scraping, written in `Scala` and using the `Selenium` platform for dynamic crawls.

Przykładowy fragment pliku konfiguracyjnego:
```json
"extractionTemplate": {
    ".box-offer-top h1.h1Title": {
        "resultId": "name/title",
        "optional": true
    },
    ".adress span": {
        "resultId": "address",
        "optional": true
    },
    ...
    "#detailsWrapper > div:first-of-type ul:nth-of-type(1) li:nth-of-type(5) span": {
        "resultId": "form of ownership",
        "optional": true
    }
}
```
Example snippet of crawl results in json format:
```json
"url": "https://krakow.nieruchomosci-online.pl/mieszkanie,na-sprzedaz/24679599.html",
"results": [
	{
		"area": "41 m²",
		"market": "wtórny",
		"price": "750 000 zł",
		"name/title": "Mieszkanie, ul. Wawrzyńca",
		"no of floors/stores in the building": "4",
		"parking space": "-",
		"no of rooms": "2",
		"address": "Wawrzyńca, Kazimierz, Kraków, małopolskie",
		"price-per-area": "18 292,68 zł/m²",
		"floor/store": "2",
		"year of construction": "1930"
	}
],
```
The data were then converted to csv format using a simple script in Python.

## Data Description

The data were collected five times in the period from March 8, 2024, to May 5, 2024, at two-week intervals for both data sources (nieruchomości-online.pl, otodom.pl) separately.

##### nieruchomosci-online dataset
Files obtained from the nieruchomości-online.pl source contain 13 columns: 'url', 'name/title', 'address', 'price', 'area', 'price-per-area', 'floor/store', 'no of floors/stores in the building', 'no of rooms', 'year of construction', 'parking space', 'market', 'form of ownership'.

- Plik `2024-03-08-nieruchomosci-online_dataset_raw.csv` zawiera 3949 wierszy (bez nagłówka). 
- Plik `2024-03-25-nieruchomosci-online-full_raw_dataset.csv` zawiera 3348 wierszy (bez nagłówka). 
- Plik `2024-04-07-nieruchomosci-online_full_raw_dataset.csv` zawiera 4141 wierszy (bez nagłówka). 
- Plik `2024-04-21-nieruchomosci-online_full_raw_dataset.csv` zawiera 6185 wierszy (bez nagłówka). 
- Plik `2024-05-05-nieruchomosci-online_full_raw_dataset.csv` zawiera 6182 wierszy (bez nagłówka).

The DataFrame created by merging these files (updating changed and adding new offers) contains 9,659 rows.

```python
>>> 2024-03-08-nieruchomosci-online_dataset_raw.csv.size
3949
```
```python
>>> 2024-03-08-nieruchomosci-online_dataset_raw.csv.info
RangeIndex: 3949 entries, 0 to 3948
Data columns (total 13 columns):
 #   Column                               Non-Null Count  Dtype
---  ------                               --------------  -----
 0   url                                  3949 non-null   object
 1   name/title                           3949 non-null   object
 2   address                              3848 non-null   object
 3   price                                3920 non-null   object
 4   area                                 3949 non-null   object
 5   price-per-area                       3920 non-null   object
 6   floor/store                          3949 non-null   object
 7   no of floors/stores in the building  3710 non-null   float64
 8   no of rooms                          3949 non-null   object
 9   year of construction                 3949 non-null   object
 10  parking space                        3949 non-null   object
 11  market                               3918 non-null   object
 12  form of ownership                    1488 non-null   object
dtypes: float64(1), object(12)
memory usage: 401.2+ KB
```

```python
>>> 2024-03-08-nieruchomosci-online_dataset_raw.csv.head(10)
                                                 url                      name/title  ...                                             market           form of ownership
0  https://krakow.nieruchomosci-online.pl/mieszka...  Mieszkanie, ul. Żelechowskiego  ...                                             wtórny                    własność
1  https://krakow.nieruchomosci-online.pl/mieszka...         Mieszkanie, ul. Balicka  ...                                             wtórny  własność, księga wieczysta
2  https://krakow.nieruchomosci-online.pl/mieszka...          Mieszkanie, ul. Zauchy  ...                                             wtórny                         NaN
3  https://krakow.nieruchomosci-online.pl/mieszka...      Mieszkanie, ul. Racławicka  ...                                             wtórny                         NaN
4  https://krakow.nieruchomosci-online.pl/mieszka...        Mieszkanie, ul. Pustynna  ...                                             wtórny  własność, księga wieczysta
5  https://krakow.nieruchomosci-online.pl/mieszka...               Apartament Kraków  ...  pierwotny (zobacz inne nowe mieszkania w Krako...                    własność
6  https://krakow.nieruchomosci-online.pl/mieszka...      Mieszkanie, ul. Przemiarki  ...                                             wtórny                    własność
7  https://krakow.nieruchomosci-online.pl/mieszka...     Mieszkanie, ul. Felińskiego  ...                                             wtórny                         NaN
8  https://krakow.nieruchomosci-online.pl/mieszka...       Apartament, ul. Lublańska  ...                                             wtórny  własność, księga wieczysta
9  https://krakow.nieruchomosci-online.pl/mieszka...   Apartament, ul. Szablowskiego  ...                                             wtórny  własność, księga wieczysta
```

##### otodom_dataset

Files obtained from the otodom.pl source contain 20 columns: `'url', 'name/title', 'address', 'price', 'area', 'price-per-area', 'floor/store', 'no of rooms', 'year of construction', 'parking space', 'market', 'form of ownership', 'condition', 'rent', 'heating', 'advertiser type', 'elevator', 'outdoor area', 'building type', 'building material'`.

- File `2024-03-08-otodom_dataset_raw.csv` contains 6819 rows (without header).
- File `2024-03-25-otodom-full_raw_dataset.csv` contains 7130 rows (without header).
- File `2024-04-07-otodom_full_raw_dataset.csv` contains 7148 rows (without header).
- File `2024-04-21-otodom_full_raw_dataset.csv` contains 7436 rows (without header).
- File `2024-05-05-otodom-full_raw_dataset.csv` contains 7465 rows (without header).

The DataFrame created by merging these files (updating changed and adding new offers) contains 14,171 rows.

```python
>>> 2024-03-08-otodom_dataset_raw.csv.size
136400
```

```python
>>> 2024-03-08-otodom_dataset_raw.csv.info
RangeIndex: 6820 entries, 0 to 6819
Data columns (total 20 columns):
 #   Column                Non-Null Count  Dtype
---  ------                --------------  -----
 0   url                   6820 non-null   object
 1   name/title            6820 non-null   object
 2   address               6820 non-null   object
 3   price                 6820 non-null   object
 4   area                  6820 non-null   object
 5   price-per-area        6526 non-null   object
 6   floor/store           6720 non-null   object
 7   no of rooms           6820 non-null   object
 8   year of construction  6154 non-null   object
 9   parking space         4206 non-null   object
 10  market                6154 non-null   object
 11  form of ownership     4941 non-null   object
 12  condition             5229 non-null   object
 13  rent                  2846 non-null   object
 14  heating               4913 non-null   object
 15  advertiser type       6154 non-null   object
 16  elevator              6154 non-null   object
 17  outdoor area          5088 non-null   object
 18  building type         6154 non-null   object
 19  building material     6154 non-null   object
dtypes: object(20)
memory usage: 1.0+ MB
```

```python
>>> 2024-03-08-otodom_dataset_raw.csv.head(10)
                                                 url                                         name/title  ...    building type building material
0  https://www.otodom.pl/pl/oferta/gotowe-2-pokoj...          Gotowe| 2 pokoje| blisko centrum| Bonarka  ...  apartamentowiec   brak informacji
1  https://www.otodom.pl/pl/oferta/4-pok-mieszkan...  4-pok.mieszkanie z Sauną - Wysoki Standard ! 2...  ...  brak informacji             cegła
2  https://www.otodom.pl/pl/oferta/3-pokoje-w-rza...            3 pokoje w rządowym programie kredyt 2%  ...             blok   brak informacji
3  https://www.otodom.pl/pl/oferta/mieszkanie-ide...           Mieszkanie idealne na start, 3 - pokoje!  ...  apartamentowiec   brak informacji
4  https://www.otodom.pl/pl/oferta/ul-lasowka-3-p...          ul. Lasówka, 3 pokoje, 65m2 + taras 20m2!  ...  brak informacji   brak informacji
5  https://www.otodom.pl/pl/oferta/przestronne-mi...  Przestronne mieszkanie / 5 pok -113m2 / Kurdwanów  ...             blok   brak informacji
6  https://www.otodom.pl/pl/oferta/przestronne-m2...  Przestronne M2 z ogródkiem,Blisko Ronda Matecz...  ...  apartamentowiec   brak informacji
7  https://www.otodom.pl/pl/oferta/bk2-3-pokoje-d...          Bk2%, 3 pokoje, duży salon, jasne, balkon  ...             blok              inny
8  https://www.otodom.pl/pl/oferta/mieszkanie-w-m...                       Mieszkanie w Mistrzejowicach  ...             blok   brak informacji
9  https://www.otodom.pl/pl/oferta/3-pokoje-z-ust...    3 pokoje z ustawnym salonem | Dobra komunikacja  ...             blok   brak informacji
```

### Preliminary Data Quality Assessment

- Since the otodom.pl service allowed for the collection of more information about the offered properties, the data from this service contains more features (columns).
- The information about the floor on which the property is located in the `nieruchomosci-online_dataset_raw.csv` set is contained in two columns: *floor/store* and *no of floors/stores in the building*. The same information in the `otodom_dataset_raw.csv` set is contained in one column -- *floor/store* and takes the form [floor]/[number of floors], e.g., "1/5". If a joint analysis of both datasets is needed, the data should be standardized.
- Due to the origin of the data, most columns in both datasets contain textual data that require conversion for further analysis.
- Due to the data acquisition method, the `nieruchomosci-online_dataset_raw.csv` set contains a number of incorrect rows resulting from atypical selector settings on the page containing the sale announcement. This particularly applies to properties from the primary market. The data in these rows will need to be reconstructed or removed.
- In a small number of cases, data on properties from the primary market do not contain prices (the option "Ask for the offer" was selected).
- In a small number of cases, the price in the offer is given in another currency (euro).
- Due to the nature of the market (actions of intermediaries and agencies) and the websites containing real estate sales offers, both sets potentially contain many rows concerning the same apartment (potential "duplicates" of offers from different intermediaries).
- Due to the nature of the market (hiding the exact address of the property by intermediaries and agencies), information about the location of the property is often not very accurate. This inaccuracy is unlikely to prevent potential analysis or modeling with a spatial/geographic component.
- For a similar reason, the datasets may contain properties located outside Krakow (apartments from Skawina or Wieliczka are often placed in these services as apartments from Krakow/suburbs of Krakow).

## Data Preparation
In the initial phase of the project, we focused on cleaning and preparing the collected data. We removed missing and incorrect values, standardized data formats, converted data types, and supplemented values where necessary. Finally, we added geographical data, which allowed for the analysis and modeling of real estate data in the geographical component.

For spatial modeling and analysis, the data collected at different times were aggregated within one dataset (for both sources). The modified data were updated, and the data from new offers were added to the set.

### Operations on Columns

#### Price
Similar operations were performed in both datasets. Missing data ("Ask for the price") and non-standard values, such as prices in other currencies, were removed. The values were converted to floating-point numeric type. Prices given in other currencies were converted to zlotys – in the case of the otodom dataset using the product of the value in zlotys `price-per-area` and `area`, and in the case of the nieruchomosci-online dataset using current exchange rates (current average in a 50-day moving window from the `yfinance` library).

#### Area, Price per Square Meter
Conversion of values from text format to numeric, removal of units ("m²", "zł/m²"). Rows with properties having an area above 200 m² and a price below 11,000 zł/m² were removed, thus eliminating offers for attics, service premises, entire floors (and errors).

#### Floor, Number of Floors in the Building
For the otodom dataset: the information about the floor and the number of floors in the building was separated to unify the datasets. In both datasets: conversion to integer types, replacing textual floor descriptions with numeric values ("parter" to 0, "suterena" to -1).

#### Number of Rooms
Standardization of data on the number of rooms, conversion to integer type. In the nieruchomosci-online dataset, rows with missing data resulting from selector shifts on some pages with primary market offers (which caused incorrect scraping) were removed.

#### Year of Construction
Similar steps for data verification and cleaning were performed in both datasets: conversion of the year of construction to integer type; in the case of obvious errors ("typos"): changing unrealistic values (years very distant in time) resulting from incorrect manual data entry in the offer (human factor), and in other cases, removing such data.

#### Parking Space
For the otodom dataset: conversion of categorical data ("yes"/"no") to boolean values. In the nieruchomosci-online dataset, the categorical data were more granular (e.g., "assigned parking space", "underground garage", "none", etc.). This column was simultaneously: 1) normalized and copied to a new column (parking space details) to retain data granularity when analyzing the dataset separately, and 2) converted to a boolean type for further unification of the datasets.

#### Market
In both datasets: the values in the 'market' column were unified by converting various descriptions to standard labels ('primary', 'secondary'). Missing data were supplemented based on the year of construction – properties with a construction year above 2022 were automatically classified as 'primary', others as 'secondary'.

#### Form of Ownership
The 'form of ownership' column was mapped to more uniform categories. Missing values were also filled based on the year of construction (see below).

#### Additional Columns in the Otodom Dataset
- **rent**: Rent values were converted to numeric type, and values in other currencies were converted based on the average current exchange rates (average in a 50-day moving window).
- **heating, advertiser type, elevator, outdoor area, building type, building material**: Standardization of categories, conversion to numeric or boolean types where applicable and possible, removal of non-standard entries.

### Examples of Applying Expert Knowledge


#### Harmonizing the Number of Floors with the Tallest Buildings in Krakow
Filtered data by eliminating properties that reported a greater number of floors than the tallest residential buildings in Krakow, thereby removing offers for properties located abroad.

#### Adjusting Ownership Type to Comply with Current Law
The building law effective from 2007 excluded the possibility of establishing cooperative ownership rights for buildings constructed after this date. Data from offers for apartments built after this date were supplemented with the default ownership type 'full ownership'.

#### Legal Requirement for Elevator Installation in Tall Buildings
According to building law effective since the 1960s, an elevator is mandatory in buildings over 9.5 meters, which is associated with a certain number of floors (per minimum floor height). Consequently, missing data regarding the presence or absence of an elevator were supplemented for buildings above (and below) 4 floors.

#### Classifying Advertiser Type
It was assumed that if the advertiser type is not specified, the default is a real estate agency. This assumption is motivated by two reasons: 1) Private individuals usually readily provide this information in offers; 2) "real estate agency" is also the most common category in this column. As a result, the appropriate default value was assigned for missing data.

#### Data Exploration
- **Statistical Analyses**: Basic statistical analyses were performed, including calculating means, medians, and analyzing value distributions in key columns, which helped us understand the price and location characteristics of the market.


### Data Engineering

#### Data Integration and Removing Duplicates
Proper data preparation allowed for the integration of data into a single dataset. The data were then subjected to engineering processes. The first step involved removing duplicates.

This step was necessary for two reasons: 1) The unified dataset could inherently contain information about the same apartment from two different sources. 2) According to our preliminary data quality assessment, even within a single source, advertisements for the same apartment introduced by different real estate agents could be found.

We attempted to identify such "duplicates" using unique property identifiers (the Cartesian product of features: address, number of rooms, floor, number of floors in the building). Properties were considered duplicates if they were identical in terms of the above values and had "sufficiently close" price and area values. "Sufficiently close" was defined as within 1% of the average value of the given feature. From the duplicates, the one with fewer missing data was selected. When possible, the missing data of the selected instance were supplemented based on data from other (rejected) members of the group.


```python
def check_similarity(group):
    if len(group) > 1:
        price_mean = group['price'].mean()
        area_mean = group['area'].mean()
        price_range = price_mean * 0.01
        area_range = area_mean * 0.01
        similar_price = group['price'].between(price_mean - price_range, price_mean + price_range)
        similar_area = group['area'].between(area_mean - area_range, area_mean + area_range)
        return (similar_price & similar_area).rename('is_duplicate')
    else:
        return pd.Series(False, index=group.index, name='is_duplicate')

def fill_from_group(group):
    group['non_null_count'] = group.notna().sum(axis=1)
    sorted_group = group.sort_values('non_null_count', ascending=False)
    sorted_group.drop('non_null_count', axis=1, inplace=True)
    most_complete_row = sorted_group.iloc[0]
    for _, row in sorted_group.iloc[1:].iterrows():
        most_complete_row = most_complete_row.combine_first(row)
    return most_complete_row

def remove_duplicates(df, group_cols=None):
    if group_cols is None:
        group_cols = ['address', 'floor/store', 'no of floors/stores in the building', 'no of rooms']
    most_complete_duplicates = duplicates.groupby(group_cols).apply(fill_from_group).reset_index(drop=True)
    filtered_df = pd.concat([non_duplicates, most_complete_duplicates], ignore_index=True)
    sorted_filtered_df = filtered_df.sort_values(by=['address', 'price', 'area'])
    return sorted_filtered_df
```

#### Supplementing Address Data and Creating Geolocation Data
Sometimes the title of the advertisement contained more detailed address information than the address column (originally from the selector). Such cases were identified and supplemented using a regular expression pattern. Similarly, the address column was cleaned to facilitate geolocation.

```python
pattern = r'(ul\.|Aleja|aleja|pl\.|al\.)\s*([^,\d]+[\d]*\b)'

def update_address(row):
    if pd.isna(row['name/title']):
        return row['address']
    match = re.search(pattern, row['name/title'])
    if match:
        street_name = match.group(2).strip()
        if pd.isna(row['address']):
            updated_address = street_name
        else:
            if street_name.lower() not in row['address'].lower():
                updated_address = f"{street_name}, {row['address']}"
            else:
                updated_address = row['address']
    else:
        updated_address = row['address']
    return updated_address
```

Next, using an external API, the addresses were converted into geographic data (detailed location including latitude and longitude), enabling the analysis of price dependencies and property data (and modeling) in the spatial component.


```python
def geocode(address):
  location = geolocator.geocode(address)
  return pd.Series([location.address, location.latitude, location.longitude])
```

From the data created in this way, the distance from the center of Krakow was calculated using the [haversine formula](https://en.wikipedia.org/wiki/Haversine_formula). Additionally, using regex, the district information was extracted into a new column. Rows with data from offers outside of Krakow were removed.


### Data Quality Verification
The integrated dataset and the nieruchomosci-online dataset contained gaps in the columns for the year of construction and form of ownership. The Otodom dataset also had gaps in the columns for rent, heating, and apartment condition.

To enable modeling and prediction, the data were supplemented using the following strategies:
- **Numerical Data** (year of construction, rent) were supplemented based on descriptive statistics – mean value, after first rejecting outliers using the IQR (Interquartile Range) method.
- **Ownership Data** were supplemented with the category "full ownership", justified by two facts: it was the most frequently appearing category, and it is logical to assume that the default ownership type for apartment sales is full ownership. Any other type of ownership, such as a share or cooperative ownership, should be (and we assume it is) clearly marked to avoid misleading the buyer.
- **Missing Categorical Data** in the Otodom dataset (heating and apartment condition) were supplemented with the category "no information". It is assumed that such classification will not significantly affect model predictions, and this value already appeared in other parts of this dataset (as it was directly in the data sources).

## Data Analysis

### Correlation Matrix (Pearson Matrix)
For the analysis of the correlation matrix for the unified dataset, the following features were selected:

![pearson.png](assets/pearson.png)

```python
#   Column                               Non-Null Count  Dtype  
---  ------                               --------------  -----  
 0   area                                 17932 non-null  float64
 1   price-per-area                       17932 non-null  float64
 2   floor/store                          17932 non-null  int64  
 3   no of floors/stores in the building  17932 non-null  int64  
 4   no of rooms                          17932 non-null  int64  
 5   year of construction                 17932 non-null  float64
 6   parking space                        17932 non-null  bool   
 7   market                               17932 non-null  int64  
 8   distance                             17932 non-null  float64
```
In the *market* column, the values *primary* and *secondary* were converted to 0 and 1, respectively.

#### Conclusions from Correlation Analysis
Besides the obvious relationships such as the number of rooms and apartment size, the year of construction and market type, or the number of floors in the building and the floor on which the apartment is located, there is a clear negative correlation between the price per square meter and the distance from the center. This confirms our assumption that as the distance from the center increases, the apartment price decreases. Slightly weaker, but noteworthy correlations also exist between the year of construction and the availability of a parking space, indicating that newer apartments more frequently have access to parking. The chart also shows a positive correlation between the year of construction and the distance from the center, confirming that new apartments are generally built further from the city center.

### Analysis of Apartment Prices in Different Districts
The analysis of apartment prices in different districts confirms the conclusions from the correlation matrix. The most expensive apartments are located in the center - Old Town. Apartments in the Old Town also have the greatest price range. The cheapest apartments are found in the districts of Swoszowice, Wzgórza Krzesławickie, and Nowa Huta.

![districts.png](assets/districts.png)

### Components Analysis (PCA)

![first_component.png](assets/first_component.png)

![second_component.png](assets/second_component.png)

The principal component analysis showed that when projecting onto the first leading component, the highest values are associated with features such as the number of rooms, parking space, and market (negative value). These features have the greatest variability and impact on the first component, but they are not key characteristics of the apartments. For the second leading component, the highest values correspond to features such as area, number of rooms (positive values), and year of construction, distance from the center (negative values). These features better reflect the characteristics of the apartments.

![biplot.png](assets/biplot.png)


Significant information about the relationships between various apartment features is provided by the visualization of feature vectors projected onto the first two principal components. The plot reflects some obvious correlations, such as the relationship between apartment area and number of rooms, and the floor on which the apartment is located and the number of floors in the building. There is an inverse relationship between these pairs of features, indicating that larger apartments are more often located in lower buildings. The negative correlation between the price per square meter and the distance from the center, visible in the correlation matrix, is also confirmed. Additionally, it can be observed that apartments from the primary market are located further from the center, which naturally implies a relationship between the year of construction and the distance from the center - new apartments are built away from the center. 

Noteworthy is the strong correlation between price and market, indicating that more expensive apartments (in terms of price per square meter) come from the secondary market. This can be explained by the fact that such apartments are generally ready to move into, unlike primary market apartments, which often require finishing. The plot also shows the relationship between the market and parking, leading to the conclusion that primary market apartments are more often equipped with dedicated parking spaces.


...


## Bibliography
<a id="1">[1]</a> R. Cellmer,
Analiza przestrzenna dynamiki zmian cen nieruchomości lokalowych z wykorzystaniem regresji ważonej geograficznie.
Acta Scientiarum Polonorum. Administratio Locorum (2010) 9/3, 5-14

<a id="2">[2]</a> M. Frukacz, M. Popieluch, E. Preweda,
Korekta cen nieruchomości ze względu na upływ czasu w przypadku dużych baz danych.
Infrastruktura i ekologia terenów wiejskich (2011) 4, 213-226


