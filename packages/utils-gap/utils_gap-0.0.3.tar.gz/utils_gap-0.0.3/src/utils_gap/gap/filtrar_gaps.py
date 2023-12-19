from geopandas import sjoin, GeoDataFrame
from shapely.geometry import Polygon

def filtrar_gaps(gap_gdf, gis):
    idxs_to_keep = filter_points_aoi(gap_gdf, gis)
    gap_gdf = gap_gdf.loc[gap_gdf["id_gap"].isin(idxs_to_keep)].reset_index(drop=True)
    
    idxs_to_keep = filter_points_ais(gap_gdf)
    return gap_gdf.loc[gap_gdf["id_gap"].isin(idxs_to_keep)].reset_index(drop=True)

def filter_points_ais(gap_gdf):
    # 701006116: Cruz del Sur
    mmsis_to_filter = ["701006116"]
    return gap_gdf\
        .loc[~gap_gdf["mmsi"].isin(mmsis_to_filter)]["id_gap"]\
        .unique()\
        .tolist()

def filter_points_aoi(gdf, gis):
    areas_gdf = __get_areas_geodataframe(gis)
    points_in_aoi = sjoin(gdf, areas_gdf, how="inner", op='within')
    
    return gdf.loc[points_in_aoi.index]["id_gap"].unique().tolist()

def __get_areas_sdf(gis):
    id_layer = "b663644cbb97408e958250bfcda2feea"
    layer = gis.content.get(id_layer).layers[0]
    return layer.query(where="1=1").sdf

def __get_areas_geodataframe(gis):
    areas = __get_areas_sdf(gis)
    areas['geom'] = areas.SHAPE.apply(lambda r: Polygon(r["rings"][0]))
    areas_gdf = GeoDataFrame(areas.drop("SHAPE", axis=1).rename(columns={"geom": "geometry"}))

    return areas_gdf

def in_azul(row):
    top_right = [-60.02, -36.94]
    down_left = [-60.31, -37.16]
    
    return in_wrong_aoi(row, down_left, top_right)

def in_malvinas(row):
    top_right = [-59.82, -50.82]
    down_left = [-61.27, -52.22]
    
    return in_wrong_aoi(row, down_left, top_right)

def in_wrong_aoi(row, down_left, top_right):
    lat_in = (row["latitude"] >= down_left[1]) & (row["latitude"] <= top_right[1])
    lon_in = (row["longitude"] >= down_left[0]) & (row["longitude"] <= top_right[0])
    
    return lat_in and lon_in

def filter_outside_aoi(gap_gdf):
    def filter_row(row):
        return (
            in_azul(row) or
            in_malvinas(row)
        )

    return gap_gdf\
        .loc[gap_gdf.apply(lambda x: not filter_row(x), axis=1)]["id_gap"]\
        .unique()\
        .tolist()
    