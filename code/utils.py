import pandas as pd
import numpy as np
import requests
import json

import geopandas as gpd
from shapely.geometry.point import Point

import googlemaps
from pyproj import Proj, transform


def round(lat: float, lon: float, dataset, r: int = 50):
    dataset['geom'] = dataset.apply(lambda r: Point(r[lon], r[lat]), axis=1)
    gdf = gpd.GeoDataFrame(dataset, geometry='geom', crs='epsg:4326')
    gdf_flat = gdf.to_crs('epsg:6347')
    gdf_flat['geom'] = gdf_flat.geometry.buffer(r)
    gdf = gdf_flat.to_crs('epsg:4326')

    site = gdf.geom[0]
    for point in gdf.geom:
        site = site.union(point)
    return site


def cal_area(poly, file):
    area = poly.area
    intersection = poly.intersection(file).area
    return intersection / area


def generate_candidate_sites(df, M):
    sites = []
    df_sorted = df.sort_values(by='weight', ascending=False)
    for _, row in df_sorted[:M].iterrows():
        sites.append([row['geo'].centroid.coords[0][0],
                     row['geo'].centroid.coords[0][1]])
    return np.array(sites)


def find_xy(dataframe, key: str):
    coord = []
    # geocoding api https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com
    gmaps = googlemaps.Client(key='******************************')

    for juso in dataframe[key]:
        geocode_result = gmaps.geocode(juso)
        lat = geocode_result[0]['geometry']['location']['lat']
        lon = geocode_result[0]['geometry']['location']['lng']
        coord.append([juso, lat, lon])

    return pd.DataFrame(coord, columns=['주소', 'lat', 'lon'])


def get_api():
    url = 'http://apis.data.go.kr/B552061/frequentzoneFreezing/getRestFrequentzoneFreezing'
    params = {'serviceKey': '****',  # API decoded key
              'searchYearCd': '2017',
              'siDo': '11',  # 서울특별시
              'guGun': '380',  # 은평구
              'type': 'json',
              'numOfRows': '5',
              'pageNo': '1'}

    response = requests.get(url, params=params)
    data = json.loads(response.content)

    return pd.DataFrame(data['items']['item'])


def trans_wtm2wgs84(dataframe):
    proj_wtm = Proj(init='epsg:5181')
    proj_wgs84 = Proj(init='epsg:4326')

    df_list = []
    for i, j, k in zip(dataframe["X 좌표 최소값"], dataframe["Y 좌표 최소값"], dataframe["관리기관명"]):
        trans = transform(proj_wtm, proj_wgs84, i, j)
        df_list.append([k, trans[1], trans[0]])

    return pd.DataFrame(df_list, columns=['관리기관명', 'lat', 'lon'])
