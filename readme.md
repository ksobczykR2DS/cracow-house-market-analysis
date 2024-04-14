# Analiza cen nieruchomości w Krakowie

Projekt w ramach zajęć **Eksploracja Danych** realizowany w semestrze letnim r.a. 2023/2024 na Wydziale Informatyki Akademii Górniczo-Hutniczej w Krakowie pod opieką dra Tomasza Pełecha-Pilichowskiego.


### Autorzy
Katarzyna Dębowska

Kacper Sobczyk

Piotr Urbańczyk

    
   ### Abstrakt
Projekt ma na celu zrozumienie zależności między cechami mieszkań a ich cenami ofertowymi na lokalnym rynku nieruchomości. W ramach prac przeprowadzimy statystykę opisową, regresję hedoniczną oraz analizę przestrzenną w celu zidentyfikowania najważniejszych czynników wpływających na cenę mieszkań w Krakowie.
   
- **Dane**: Wykorzystano zbiór danych zawierający informacje o ofertach sprzedaży nieruchomości.
- **Źródło danych**: Dane zostały wyekstrahowane za pomocą metod automatycznych z dwóch popularnych portali zawierających oferty sprzedaży nieruchomości.
- **Przygotowanie danych**: Zrozumienie danych, usuwanie brakujących wartości, uspójnienie, konwersja formatów, uzupełnienie danych geograficznych (koordynatów) na postawie adresu, dodanie (wektora) odległości od centrum miasta (Rynku Głównego) na podstawie danych geograficznych itp. -- do ew. uzupełnienia w trakcie prac.
- **(Proponowane) analizy i modelowanie**: Statystyka opisowa, regresja hedoniczna, macierz korelacji (identyfikacja czynników wpływających na cenę nieruchomości), analiza przestrzenna (regresja ważona geograficznie [[1]](#1)) itp.  -- do ew. uzupełnienia po konsultacjach i w trakcie prac.
- **(Oczekiwane) wyniki**: Zrozumienie, które cechy nieruchomości najbardziej wpływają na cenę ofertową mieszkań w Krakowie, wykrycie ewentualnych trendów cenowych w poszczególnych dzielnicach itp. -- do ew. uzupełnienia w trakcie prac.

### Spis treści
1. [Zrozumienie danych](#zrozumienie-danych)

	1.1. [Gromadzenie danych](#gromadzenie-danych)

	1.2. [Opis danych](#opis-danych)

	1.3. [Weryfikacja jakości danych](#weryfikacja-jakości-danych)
2. [Przygotowanie danych](#czynności-wstępne)



   
## Zrozumienie danych
W projekcie wykorzystano zbiór danych zawierający informacje o ofertach sprzedaży mieszkań w Krakowie.
### Gromadzenie danych
#### Źródło danych
Dane zostały pozyskane za pomocą metod automatycznych ze źródeł w swobodnym dostępie -- dwóch popularnych portali zawierających oferty sprzedaży nieruchomości: [nieruchomości-online.pl](nieruchomości-online.pl) oraz [otodom.pl](otodom.pl).

#### Metody pozyskania danych
Oba zbiory danych zostały pozyskane przy użyciu profesjonalnego rozwiązania do scrapingu treści z sieci Internet (pisanego w języku `Scala` a w przypadku crawli o charakterze dynamicznym wykorzystującego platformę `Selenium`).

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
Przykładowy fragment wyników crawli w formacie `json`:
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
Dane zostały następnie przekonwertowane do formatu `csv` (za pomocą prostego skryptu w języku `Python`).

### Opis danych

Dane zostały zebrane w dwóch plikach w formacie csv.
##### nieruchomosci-online_dataset_raw.csv
Plik `nieruchomosci-online_dataset_raw.csv` zawiera 3949 wierszy (bez nagłówka)  oraz 13 kolumn. 

```python
>>> nieruchomosci-online_dataset_raw.size
51337
```

```python
>>> nieruchomosci-online_dataset_raw.info
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
>>> nieruchomosci-online_dataset_raw.head(10)
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

##### otodom_dataset_raw.csv

Plik `otodom_dataset_raw.csv` zawiera 6819 wierszy (bez nagłówka) oraz 20 kolumn.

```python
>>> otodom_dataset_raw.size
136400
```

```python
>>> otodom_dataset_raw.info
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
>>> otodom_dataset_raw.head(10)
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

### Weryfikacja jakości danych

- Ponieważ serwis orodom.pl umożliwiał zebranie większej liczby informacji o oferowanych nieruchomościach, dane pochodzące z tego serwisu zawierają więcej cech (kolumn).
- Informacja o piętrze, na którym znajduje się nieruchomość, w zbiorze `nieruchomosci-online_dataset_raw.csv` zawarta jest w dwóch kolumnach *floor/store* oraz *no of floors/stores in the building*. Ta sama informacja w zbiorze `otodom_dataset_raw.csv` zawarta jest w jednej kolumnie -- *floor/store* i przybiera postać postać [piętro]/[liczba pięter], np. "1/5". W przypadku potrzeby wspólnej analizy obu zbiorów, dane powinny zostać ujednolicone.
- Z uwagi na pochodzenie danych, większość kulumn w obu zbiorach zawiera dane tekstowe, wymagające konwersji w celu dalszych analiz.
- Z uwagi na sposób pozyskania danych, zbiór `nieruchomosci-online_dataset_raw.csv` zawiera pewną liczbę niepoprawnych wierszy wynikających z nietypowego ustawienia selektorów na stronie zawierającej ogłoszenie o sprzedaży. Dotyczy to zwłaszcza nieruchomości z rynku pierwotnego. Dane w tych wierszach będą musiały zostać odtworzone lub usunięte.
- W niewielkiej liczbie przypadków dane o nieruchomościach z rynku pierwotnego nie zawierają ceny (wybrano opcję "Zapytaj o ofertę").
- W niewielkiej liczbie przypadków cena w ofercie podana jest w innej walucie​ (euro).
- Z uwagi na charakter rynku (działania pośredników i agencji) oraz stron zawierających oferty sprzedaży nieruchomości, oba zbiory zawierają potencjalnie wiele wierszy dotyczących tego samego mieszkania (potencjalne "duplikaty" ofert pochodzące od różnych pośredników).
- Z uwagi na charakter rynku (ukrywanie dokładnego adresu nieruchomości przez pośredników i agencje), informacje o położeniu nieruchomości są najczęściej niezbyt dokładne. Ta niedokładność nie będzie raczej uniemożliwiała potencjalne analizy lub modelowanie z komponentem przestrzennym/geograficznym.
- Z podobnego powodu zbiory mogą zawierać nieruchomości położone poza Krakowem (mieszkania ze Skawiny czy Wieliczki są często umieszczane w tych serwisach jako mieszkania z Krakowa/obrzeży Krakowa).


## Przygotowanie danych
Usuwanie brakujących lub błędnych wartości, ujednolicenie danych, konwersja formatów, dodanie danych geograficznych itp. -- do ew. uzupełnienia w trakcie prac.



...


## Bibliografia
<a id="1">[1]</a> R. Cellmer,
Analiza przestrzenna dynamiki zmian cen nieruchomości lokalowych z wykorzystaniem regresji ważonej geograficznie.
Acta Scientiarum Polonorum. Administratio Locorum (2010) 9/3, 5-14

<a id="2">[2]</a> M. Frukacz, M. Popieluch, E. Preweda,
Korekta cen nieruchomości ze względu na upływ czasu w przypadku dużych baz danych.
Infrastruktura i ekologia terenów wiejskich (2011) 4, 213-226

