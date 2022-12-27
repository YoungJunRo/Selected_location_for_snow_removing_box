from shapely.geometry.point import Point
import numpy as np
import geopandas as gpd

def round(r: int, lon: str, lat: str, dataset):
    dataset['geom'] = dataset.apply(lambda r: Point(r[lon], r[lat]), axis=1)
    gdf = gpd.GeoDataFrame(dataset, geometry='geom', crs='epsg:4326')
    gdf_flat = gdf.to_crs('epsg:6347')
    gdf_flat['geom'] = gdf_flat.geometry.buffer(r)

    u = dataset.geom[0]
    for point in gdf.geom:
        u = u.union(point)
    return u

def cal_area(poly, file):
    area = poly.area
    intersection = poly.intersection(file).area
    return intersection / area

def generate_candidate_sites(df, M):
    sites = []
    df_sorted = df.sort_values(by='weight', ascending=False)
    for _, row in df_sorted[:M].iterrows():
        sites.append([row['geo'].centroid.coords[0][0], row['geo'].centroid.coords[0][1]])
    return np.array(sites)