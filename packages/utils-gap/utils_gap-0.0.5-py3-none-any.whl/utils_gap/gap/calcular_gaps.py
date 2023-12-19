import numpy as np
from uuid import uuid4
from datetime import timedelta
import pandas as pd
from geopandas import GeoDataFrame, points_from_xy

def calcular_gaps(ais_gdf):
    GAP1 = timedelta(hours=1)
    GAP2 = timedelta(hours=8)
    GAP3 = timedelta(hours=24)
    
    gap_1hs = gaps_por_tiempo(ais_gdf, GAP1, GAP2, type_gap="Moderado")
    gap_8hs = gaps_por_tiempo(ais_gdf, GAP2, GAP3, type_gap="Grave")
    gap_24hs = gaps_por_tiempo(ais_gdf, GAP3, None, type_gap="Muy grave")

    gap = pd.concat([gap_1hs, gap_8hs, gap_24hs], ignore_index=True)
    gap_gdf = GeoDataFrame(
        gap, geometry=points_from_xy(gap["longitude"], gap["latitude"])
    )

    gap_gdf["speed_group"] = gap_gdf["speedovergroud"].apply(get_speed_group)

    return gap_gdf

def get_speed_group(speed, step=2, max_value=12):
    speed_ranges = [(i, min(i+step, max_value)) for i in range(0, max_value, step)]

    for lower, upper in speed_ranges:
        if lower <= speed < upper:
            return f"{lower}-{upper} nudos"

    return f"> {max_value} nudos" if speed > max_value else "No reportada"

def gaps_por_tiempo(df, delta_time_min, delta_time_max, type_gap="Moderado"):
    if delta_time_max is not None:
        gap_or = df.loc[(df.next_msgdate >= delta_time_min) & (df.next_msgdate <= delta_time_max)]
    else:
        gap_or = df.loc[(df.next_msgdate >= delta_time_min)]

    gap_or["point_gap"] = "start"
    gap_or["id_gap"] = gap_or.apply(lambda x: str(uuid4()), axis=1)

    gap_dest = df.loc[gap_or.next_idx, :]
    gap_dest["point_gap"] = "end"
    gap_dest["id_gap"] = gap_dest["idx"].apply(lambda x: gap_or[gap_or.next_idx == x]["id_gap"].values[0])

    gap = pd.concat([gap_or, gap_dest], ignore_index=True)
    gap["type_gap"] = type_gap
    gap["secs_next_msg"] = gap["next_msgdate"].apply(lambda x: x / np.timedelta64(1, 's')).astype(int)
    gap["hs_next_msg"] = gap["next_msgdate"].apply(lambda x: round(x.total_seconds() / 3600, 2))
    gap["time_gap"] = gap["next_msgdate"].apply(lambda x: str(x))

    return gap.drop(["next_idx", "next_msgdate"], axis=1)