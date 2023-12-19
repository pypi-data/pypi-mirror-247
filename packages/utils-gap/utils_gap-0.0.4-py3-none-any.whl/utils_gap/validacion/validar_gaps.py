import pandas as pd
from shapely.geometry import LineString
from tqdm import tqdm
from datetime import timedelta
from collections import namedtuple
from utils_gap.validacion.pipeline_validacion import crear_pipeline_validacion

def validar_gaps(gaps, posiciones, limite_zeea):
    validador = crear_pipeline_validacion(limite_zeea)
    eventos = []

    for i in tqdm(range(0, len(gaps), 2)):
        row1 = gaps.iloc[i]
        row2 = gaps.iloc[i+1]

        gap = GAP.crear_evento(posiciones, row1, row2)
        gap.validar_ausencia_reporte(validador)
        eventos.append(gap)

    return convertir_eventos(eventos)

def convertir_eventos(eventos):
    filas = []

    for evento in eventos:
        dict_evento = {**evento.dict_buque, **evento.dict_gap, **evento.estado_validacion}
        dict_evento["start_date"] = evento.reporte_inicio.fecha
        dict_evento["end_date"] = evento.reporte_fin.fecha
        dict_evento["geometry"] = LineString([
            evento.reporte_inicio.punto,
            evento.reporte_fin.punto,
        ])

        filas.append(pd.DataFrame([dict_evento]))

    return pd.concat(filas, ignore_index=True)

Reporte = namedtuple("Reporte", "tipo punto fecha posiciones_anteriores")

class GAP:
    def __init__(self, dict_buque, dict_gap, reporte_inicio, reporte_fin):
        self.dict_buque = dict_buque
        self.dict_gap = dict_gap
        self.reporte_inicio = reporte_inicio
        self.reporte_fin = reporte_fin
        self.tiempo_gap = (reporte_fin.fecha - reporte_inicio.fecha).total_seconds() / 3600

    def validar_ausencia_reporte(self, validador):
        self.estado_validacion = validador.validar(self)

    @classmethod
    def crear_evento(cls, posiciones, row1, row2):
        mmsi = row1["mmsi"]
        fecha = row1["msgdate"]

        posiciones_anteriores = posiciones.loc[(
            (posiciones["mmsi"] == mmsi) &
            (posiciones["msgdate"] >= fecha - timedelta(hours=1)) &
            (posiciones["msgdate"] < fecha - timedelta(minutes=5))
        )]

        reporte_inicio = Reporte("comienzo", row1["geometry"], row1["msgdate"], posiciones_anteriores)
        reporte_fin = Reporte("fin", row2["geometry"], row2["msgdate"], "")

        dict_buque = row1[[
            "mmsi", "vessel_name",
            "flag_name", "flag_code",
            "imo", "vessel_type"
        ]].to_dict()

        dict_gap = row1[[
            "id_gap", "type_gap",
            "hs_next_msg"
        ]].to_dict()
        dict_gap["speed_group"] = "Sin reporte"

        return cls(
            dict_buque,
            dict_gap,
            reporte_inicio,
            reporte_fin,
        )