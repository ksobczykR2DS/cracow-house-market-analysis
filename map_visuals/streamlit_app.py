import os

import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
from pydeck.types import String
import streamlit as st

st.set_page_config(layout="wide", page_title="Ceny mieszkań w Krakowie | ED 23/24", page_icon=":house:")


# LOAD DATA ONCE
@st.cache_resource
def load_data():
    directory = "../datasets/"
    filename = "apartments_collective.csv"
    path = os.path.join(directory, filename)
    if not os.path.isfile(path):
        path = f"https://github.com/ksobczykR2DS/ED2024/tree/main/datasets/{filename}"

    data = pd.read_csv(
        path,
        usecols=["price", 'price-per-area', "no of floors/stores in the building", "year of construction",
                 "parking space", "distance", "location", "latitude", "longitude"]
    )
    data['parking space'] = data['parking space'].astype(int)*100
    data['number of offers'] = 1

    aggregation_methods = {
        'price': 'mean',
        'price-per-area': 'mean',
        "no of floors/stores in the building": 'mean',
        'year of construction': 'mean',
        'parking space': 'mean',
        'distance': 'mean',
        'location': 'first',
        'number of offers': 'size'
    }
    aggregated_df = data.groupby(['latitude', 'longitude']).agg(aggregation_methods).reset_index()
    aggregated_df['building age'] = aggregated_df['year of construction'].max() - aggregated_df['year of construction']
    aggregated_df['distance_plot'] = aggregated_df['distance']

    # aggregated_df["distance"] = aggregated_df["distance"] * 100
    # aggregated_df['price-per-area'] = aggregated_df['price-per-area'] * 100
    # aggregated_df["price"] = aggregated_df["price"] / 1000

    return aggregated_df


data = load_data()


def add_color_based_on_metric(df, metric):
    min_val = df[metric].min()
    max_val = df[metric].max()

    norm = (df[metric] - min_val) / (max_val - min_val)

    df['color'] = norm.apply(lambda x: [255, int(255 * (1 - x)), 0]).tolist()

    return df


def get_elevation_scale(metric):
    if metric == 'building age':
        return 1 / 20
    elif metric == 'parking space':
        return 1 / 3
    else:
        return 2


def adjust_elevation(data, metric):
    if metric == 'distance':
        scale_factor = 200
    elif metric == 'price':
        scale_factor = 1 / 1000
    elif metric == 'price-per-area':
        scale_factor = 1 / 10
    elif metric == 'number of offers':
        scale_factor = 10
    elif metric == 'no of floors/stores in the building':
        scale_factor = 200
    elif metric == 'parking space':
        scale_factor = 200
    elif metric == 'building age':
        scale_factor = 200
    else:
        scale_factor = 1

    data['adjusted_elevation'] = data[metric] * scale_factor
    return data


def map(data, lat, lon, zoom, radius, selected_metric):
    data = add_color_based_on_metric(data, selected_metric)
    data = adjust_elevation(data, selected_metric)
    elevation_scale = get_elevation_scale(selected_metric)
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=zoom,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ColumnLayer",
                data=data,
                get_position=["longitude", "latitude"],
                get_elevation="adjusted_elevation",
                auto_highlight=True,
                opacity=0.5,
                radius=radius,
                elevation_scale=elevation_scale,
                get_fill_color="color",
                pickable=True,
                extruded=True,
                aggregation=String('MEAN')
            ),
        ],
        tooltip={
            "html": f"<b>Location:</b> {{location}}<br><b>Mean {selected_metric}:</b> {{{selected_metric}}}"
                    f"<br><b>Offers:</b> {{number of offers}}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }
    ))


@st.cache_data
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))


midpoint = mpoint(data["latitude"], data["longitude"])

st.title("Apartment Prices and Market Statistics in Kraków | Eksploracja Danych 2023/2024")
st.subheader("Katarzyna Dębowska, Kacper Sobczyk, Piotr Urbańczyk")

selected_metric = st.selectbox(
    "Select metric to display",
    ["price", "price-per-area", "building age", "no of floors/stores in the building", "parking space",
     "number of offers", "distance"],
    index=0
)

radius = st.slider("Select bar radius in meters:", min_value=50, max_value=1000, value=300, step=50)

map(data, midpoint[0], midpoint[1], 10, radius, selected_metric)

hist_data = data[['distance_plot', selected_metric]]

# Histogram that shows distribution of the selected metric by distance
st.write(f"**Breakdown of {selected_metric} by distance:**")
chart = alt.Chart(hist_data).mark_bar().encode(
    x=alt.X('distance_plot:Q', title='Distance from city center (km)',
            scale=alt.Scale(domain=(0, hist_data['distance_plot'].max()))),
    y=alt.Y(f'mean({selected_metric}):Q', title=f'Mean {selected_metric}'),
    tooltip=['distance_plot', f'mean({selected_metric})']
).interactive()
st.altair_chart(chart, use_container_width=True)

# Scatter plot that shows raw data points
st.write(f"Distribution of {selected_metric} by Distance")
chart2 = alt.Chart(hist_data).mark_circle(size=60).encode(
    x=alt.X('distance_plot:Q', title='Distance from city center (km)'),
    y=alt.Y(f'{selected_metric}:Q', title=f'Mean {selected_metric}'),
    tooltip=['distance_plot', selected_metric]
).interactive()
st.altair_chart(chart2, use_container_width=True)
