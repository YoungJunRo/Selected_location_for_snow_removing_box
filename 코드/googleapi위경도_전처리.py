import googlemaps
from datetime import datetime
from pyproj import Proj, transform
import pandas  as pd

csv = pd.read_csv('C:/test.csv',
                   encoding='cp949',
                   sep=",",)


lat_list = []
lon_list = []

df = csv.copy()
gmaps = googlemaps.Client(key='******************************')

for idx, row in df.iterrows():
    addr = row['juso']
    geocode_result = gmaps.geocode(addr)   
    n_lat = geocode_result[0]['geometry']['location']['lat']
    n_lon = geocode_result[0]['geometry']['location']['lng']
    loc = {'lat':n_lat, 'lon':n_lon}
    lat_list.append(n_lat)
    lon_list.append(n_lon)

csv['lat'] = lat_list
csv['lon'] = lon_list

csv.to_csv('test.csv', encoding='cp949')
