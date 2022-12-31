import pandas as pd
import numpy as np
import requests
import json
from tqdm import tqdm
from time import sleep

import geopandas as gpd
from shapely.geometry.point import Point

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pyproj import Proj, transform


def round(lat: str, lon: str, dataset, r: int = 50):
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


def chrome_setting():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(r'c:\chromedriver', options=chrome_options)
    return driver


def find_xy(dataframe, key: str, name: str):
    driver = chrome_setting()
    driver.get("https://address.dawul.co.kr/")

    input_site = EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#input_juso'))
    coord_site = EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#insert_data_5'))

    get_coord = list()
    for juso, name in zip(tqdm(dataframe[key]), dataframe[name]):
        try:
            WebDriverWait(driver, 3).until(input_site).clear()
            WebDriverWait(driver, 3).until(input_site).click()
            WebDriverWait(driver, 3).until(input_site).send_keys(juso)
            WebDriverWait(driver, 3).until(input_site).send_keys(Keys.RETURN)
            sleep(1)
            coord = WebDriverWait(driver, 3).until(coord_site).text.split(",")
            get_coord.append([name, coord[1][4:], coord[0][3:]])
        except:
            get_coord.append([name, '', ''])

    return pd.DataFrame(get_coord, columns=['name', 'lat', 'lon'])


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
    proj_wtm = Proj(init='epsg:5186')
    proj_wgs84 = Proj(init='epsg:4326')

    df_list = []
    for i, j, k in zip(tqdm(dataframe["X 좌표 최소값"]), dataframe["Y 좌표 최소값"], dataframe["관리기관명"]):
        trans = transform(proj_wtm, proj_wgs84, i, j)
        df_list.append([k, trans[1], trans[0]])

    return pd.DataFrame(df_list, columns=['관리기관명', 'lat', 'lon'])
