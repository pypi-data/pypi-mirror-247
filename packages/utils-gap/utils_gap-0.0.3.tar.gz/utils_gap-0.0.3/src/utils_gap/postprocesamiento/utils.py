from geopandas import GeoDataFrame
from shapely.geometry import Point

def generate_gdf_areas(tracks_expanded, points_expanded, finder):
    points_areas = finder.find_areas(points_expanded, join_type="left")

    idxs_gaps = points_expanded["id_gap"].unique().tolist()

    dict_idxs = {}

    for idx in idxs_gaps:
        start = points_areas.loc[(points_areas.id_gap == idx) & (points_areas.point_gap == "inicio")]
        end = points_areas.loc[(points_areas.id_gap == idx) & (points_areas.point_gap == "fin")]

        if not isinstance(start["area_name"].values[0], float):
            dict_idxs[idx] = start["area_name"].values[0]
        else:
            dict_idxs[idx] = end["area_name"].values[0]

    def map_area_name(row):
        return dict_idxs[row["id_gap"]]

    points_areas["area_name"] = points_areas.apply(map_area_name, axis=1)
    tracks_expanded["area_name"] = tracks_expanded.apply(map_area_name, axis=1)

    return tracks_expanded, points_areas

def generar_trayectorias(gaps):
    trayectorias_gap = GeoDataFrame(gaps)
    
    trayectorias_gap = trayectorias_gap.rename(
        columns={
            "hs_next_msg": "hs_ais_off", 
            "razon": "razon_validacion",
            "estado": "validacion_recorrido"
        }
    )

    trayectorias_gap["nacionalidad"] = trayectorias_gap["flag_name"].apply(mapear_nacionalidad)
    
    return trayectorias_gap

def generar_puntos(trayectorias_gap):
    filas = []
    for _, row in trayectorias_gap.iterrows():
        comienzo = row.copy()
        comienzo["geometry"] = Point(comienzo["geometry"].coords[0])
        comienzo["point_gap"] = "inicio"
        comienzo["msgdate"] = comienzo["start_date"]
        filas.append(comienzo.to_dict())

        fin = row.copy()
        fin["geometry"] = Point(fin["geometry"].coords[1])
        fin["point_gap"] = "fin"
        fin["msgdate"] = fin["end_date"]
        filas.append(fin.to_dict())

    puntos_gap = GeoDataFrame(filas)

    puntos_gap = puntos_gap.rename(
        columns={
            "validacion_recorrido": "validacion",
            "start_date": "start_date_event",
            "end_date": "end_date_event"
        }
    )

    return puntos_gap

def mapear_nacionalidad(pais):
    if pais == "Argentina":
        return "Buque argentino"
    else:
        return "Buque extranjero"