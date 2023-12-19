import pandas as pd
from utils_gap.gap.calcular_gaps import calcular_gaps
from utils_gap.gap.filtrar_gaps import filtrar_gaps
from utils_gap.fuentes_argentinas.fuentes_gap import FuentesGAP

def gaps_argentinos(gaps_expandidos, gis, api_static):
    ais_arg, gaps_arg = generar_gaps_argentinos(gaps_expandidos, gis, api_static)

    gaps_ext = gaps_expandidos\
        .loc[gaps_expandidos["flag_name"] != "Argentina"]

    return ais_arg, pd.concat([gaps_ext, gaps_arg], ignore_index=True)

def generar_gaps_argentinos(gaps_expandidos, gis, api_static):
    gaps_arg = gaps_expandidos\
        .loc[gaps_expandidos["flag_name"] == "Argentina"]\
        .reset_index(drop=True)
    
    ais_arg = obtener_ais_argentinos(gaps_arg, gis, api_static)
    gaps_arg2 = calcular_gaps(ais_arg)
    gaps_arg2 = filtrar_gaps(gaps_arg2, gis)

    return ais_arg, gaps_mergeados(gaps_arg, gaps_arg2)

def obtener_ais_argentinos(gaps_arg, gis, api_static):
    fuentes = FuentesGAP(gis, api_static)
    return fuentes.expandir_ais_gaps(gaps_arg)

def gaps_mergeados(gaps_arg, gaps_arg2):
    cols_info = [
        "mmsi", "element_id", 
        "imo", "true_mmsi", 
        "flag_code", "flag_name", 
        "vessel_type", "vessel_name"
    ]

    info_buques = gaps_arg[cols_info].drop_duplicates(subset=["mmsi"])

    return pd.merge(
        gaps_arg2, info_buques,
        how='left', left_on='mmsi',
        right_on='mmsi',
        left_index=False, right_index=False
    )