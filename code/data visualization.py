import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster

j_map = json.load(
    open('../data/skorea_municipalities_geo_simple.json', encoding='utf-8'))

df = pd.read_csv('../data/서울시_생활인구_정리.csv', encoding='utf-8')

#서울 위경도
lat_c = 37.53165351203043
lon_c = 126.9974246490573

m = folium.Map(location=[lat_c, lon_c], zoom_start=11)

m.choropleth(geo_data=j_map,
             data=df,
             columns=['시군구명', '총생활인구수'],
             fill_color='PuRd',
             key_on='feature.id')

csv = pd.read_csv('../data/conv_seoul_jae-seor-ham.csv',
                  encoding='cp949',
                  sep=",",)

marker_cluster = MarkerCluster().add_to(m)

for idx, row in csv.iterrows():

    lat_ = row['lat']
    lon_ = row['lon']

    folium.Marker(location=[lat_, lon_],
                  radius=10
                  ).add_to(marker_cluster)

m.save('map.html')