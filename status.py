import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster

j_map = json.load(
    open('./data/org/skorea_municipalities_geo_simple.json', encoding='utf-8'))

people = pd.read_csv('./data/seoul_people.csv', encoding='utf-8')

# 서울 위경도
lat_c, lon_c = 37.53165351203043, 126.9974246490573

m = folium.Map(location=[lat_c, lon_c], zoom_start=11)

m.choropleth(geo_data=j_map,
             data=people,
             columns=['법정구명', '총생활인구수'],
             fill_color='PuRd',
             key_on='feature.id')

jaeseorham = pd.read_csv('./data/seoul_jaeseorham.csv',
                  encoding='cp949',
                  sep=",",)

marker_cluster = MarkerCluster().add_to(m)

for idx, row in jaeseorham.iterrows():

    lat_ = row['lat']
    lon_ = row['lon']

    folium.Marker(location=[lat_, lon_],
                  radius=10
                  ).add_to(marker_cluster)

m.save("../map/status.html")