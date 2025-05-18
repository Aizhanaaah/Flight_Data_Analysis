import requests
import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt
import folium
from IPython.display import display
from folium.plugins import HeatMap


filename = 'flight_data.csv'
url = "https://opensky-network.org/api/states/all"

response = requests.get(url)

if response.status_code == 200:
    data = response.json().get('states', [])
    
    columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
        "spi", "position_source"
    ]

    df = pd.DataFrame(data, columns=columns)

    if not os.path.exists(filename):
        df.to_csv(filename, index=False)
        print('csv file created')

    else:
        df = df[df['origin_country'] == 'Hungary']
        df["time_position"] = pd.to_datetime(df["time_position"], unit="s")
        df["last_contact"] = pd.to_datetime(df["last_contact"], unit="s")
        df = df.dropna(subset=["longitude", "latitude", "icao24", "callsign"])
        df.to_csv(filename, mode="a", header=False, index=False)
        print('Data successfully appended to existing file.')
else:
    print(f"Failed to retrieve data: {response.status_code}")



gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude),crs="EPSG:4326"  
)



print(gdf.head())
gdf.plot(marker="o", color="blue", markersize=5, figsize=(10, 6))
plt.title("Aircraft Positions")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
'''
'''

on_ground_counts = df['on_ground'].value_counts()
print(on_ground_counts)
on_ground = on_ground_counts.get(True, 0)
above_ground = on_ground_counts.get(False, 0)
labels = ['On Ground', 'In Air']
sizes = [on_ground, above_ground]
colors = ['#ff9999', '#66b3ff']
explode = (0.05, 0)
plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
        colors=colors, explode=explode, shadow=True)
plt.title('Aircraft Status: On Ground vs In Air')
plt.axis('equal') 
plt.show()



m = folium.Map(location=[50, 10], zoom_start=4)
gdf_clean = gdf.dropna(subset=["latitude", "longitude"])
heat_data = [[row.latitude, row.longitude] for _, row in gdf_clean.iterrows()]
HeatMap(heat_data).add_to(m)


for _, row in gdf_clean.iterrows():
    folium.Marker(
        location=[row.latitude, row.longitude],
        popup=f"{row.callsign} ({row.origin_country})",
        icon=folium.Icon(color="blue", icon="plane", prefix="fa")
    ).add_to(m)


m.save("aircraft_map.html")
print("Map successfully generated without NaN locations!")
display(m)


'''def clear_csv_file(filename):
    with open(filename, "w") as file:
        file.write("")  # Overwrites the file with nothing
    print(f"All data removed from {filename}.")

clear_csv_file("flight_data.csv")'''
