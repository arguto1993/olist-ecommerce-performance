import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from .constants import COLOR_GREEN, DIR_CLEAN_DATASET

# Load Dataset
df_customers = pd.read_csv(DIR_CLEAN_DATASET + "customers_clean.csv")
df_sellers = pd.read_csv(DIR_CLEAN_DATASET + "sellers_clean.csv")
df_geolocation = pd.read_csv(DIR_CLEAN_DATASET + "geolocation_clean.csv")


def get_map_data(choice="customers"):
    geolocation_fields = ['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state']

    # Choose fields based on the choice parameter
    if choice == "customers":
        customers_fields = ['customer_unique_id', 'customer_zip_code_prefix']
        df_geolocation_data = df_customers[customers_fields].rename(columns={'customer_zip_code_prefix': 'zip_code_prefix'})
    elif choice == "sellers":
        sellers_fields = ['seller_id', 'seller_zip_code_prefix']
        df_geolocation_data = df_sellers[sellers_fields].rename(columns={'seller_zip_code_prefix': 'zip_code_prefix'})
    else:
        raise ValueError("Invalid choice. Please use 'customers' or 'sellers'.")

    # Merge with geolocation data
    df_merged = pd.merge(
        df_geolocation_data,
        df_geolocation[geolocation_fields],
        left_on='zip_code_prefix',
        right_on='geolocation_zip_code_prefix',
        how='left',
    )

    return df_merged


def map(choice="customers"):
    """Map customers/sellers Geolocation with Folium"""

    df = get_map_data(choice)

    key_field = 'customer_unique_id' if choice == 'customers' else 'seller_id'
    prefix = choice.title()

    state_aggregation = df.groupby(['geolocation_state', 'geolocation_city']).agg({
        'geolocation_lat': 'mean',
        'geolocation_lng': 'mean',
        key_field: 'count'
    }).reset_index()

    map_ = folium.Map(location=[state_aggregation['geolocation_lat'].mean(),
                                state_aggregation['geolocation_lng'].mean()],
                      zoom_start=4)

    marker_cluster = MarkerCluster().add_to(map_)

    # Add circle markers to the cluster
    for _, row in state_aggregation.iterrows():
        radius = max(row[key_field] / 50, 5)  # Minimum radius
        folium.CircleMarker(
            location=[row['geolocation_lat'], row['geolocation_lng']],
            radius=radius,
            popup=f"City: {row['geolocation_city']}\nState: {row['geolocation_state']}\n{prefix} count: {row[key_field]}",
            color=COLOR_GREEN,
            fill=True,
            fillColor=COLOR_GREEN,
            fill_opacity=0.5
        ).add_to(marker_cluster)

    return map_