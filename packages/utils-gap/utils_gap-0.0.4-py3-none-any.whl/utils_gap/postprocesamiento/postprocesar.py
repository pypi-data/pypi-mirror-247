from geopandas import GeoDataFrame
from utils_pna.areas import AreaFinder
from utils_gap.postprocesamiento.utils import (
    generar_puntos, 
    generar_trayectorias,
    generate_gdf_areas, 
)

def postprocesar(gaps, gis, id_layer_areas):
    trayectorias_gap = generar_trayectorias(gaps)
    puntos_gap = generar_puntos(trayectorias_gap)

    finder = AreaFinder(gis, id_layer_areas)
    return geodataframes_parseados(trayectorias_gap, puntos_gap, finder)
    
def geodataframes_parseados(trayectorias_gap, puntos_gap, finder):
    trayectorias_gap, puntos_gap = generate_gdf_areas(trayectorias_gap, puntos_gap, finder)
    regulares = trayectorias_gap.loc[trayectorias_gap["validacion_recorrido"] == "Regular"]
    irregulares = trayectorias_gap.loc[trayectorias_gap["validacion_recorrido"] == "Irregular"]
    info = trayectorias_gap
    gap_apagado = puntos_gap.loc[puntos_gap["point_gap"] == "inicio"]
    gap_prendido = puntos_gap.loc[puntos_gap["point_gap"] == "fin"]

    return [
        regulares, irregulares, info, gap_apagado, gap_prendido
    ]