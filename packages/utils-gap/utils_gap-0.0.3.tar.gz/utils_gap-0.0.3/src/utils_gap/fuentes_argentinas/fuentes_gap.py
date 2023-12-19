import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from utils_pna.queries import parse_positions
from src.utils_gap.utils.fechas import from_pd_date
from src.utils_gap.fuentes_argentinas.consulta_api import formar_fuentes
from src.utils_gap.extraccion.extraer_posiciones import parse_features

class FuentesGAP:
    def __init__(self, gis, api_static):
        self.gis = gis
        self.token = self.gis._con.token
        self.api_static = api_static
        self.apis = formar_fuentes(self.gis)

    def __api_static_request(self, mmsi):
        url = f'{self.api_static}/elements/search?f=json&token={self.token}'

        headers = {'Content-Type': 'application/json'}
        data = {
            "criteria": {
                "MMSI": mmsi,
                "elementType": "buque"
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            r = response.json()
            return r
        return None

    def __try_get_keys(self, mmsi):
        results_mmsi = self.__api_static_request(mmsi)
        if results_mmsi is not None:
            return results_mmsi[0]["keys"]
        else:
            return None
    
    def consultar_registros(self, mmsi):
        tries = 0
        results_mmsi = None

        while tries < 5 and results_mmsi is None:
            results_mmsi = self.__try_get_keys(mmsi)
            tries += 1

        results_mmsi = {k:v for k, v in results_mmsi.items() if v is not None}
        results_mmsi["MMSI"] = mmsi

        return results_mmsi

    def fuentes_gap(self, gap_row):
        map_keys = self.consultar_registros(gap_row["mmsi"])
        horas_sig = max(gap_row["hs_next_msg"], 1)
        mins = int(horas_sig * 60)
        results = []

        for api in self.apis:
            api.keys(map_keys)
            query_str = ' OR '.join([f"{k}='{v}'" for k, v in api.query_idxs.items()])
            query_str = f"({query_str})"
            results_api = api.query_api.query(
                dates=[
                    from_pd_date(gap_row["msgdate"]),
                    from_pd_date(gap_row["msgdate"] + timedelta(hours=horas_sig)),
                ],
                step_dates=mins,
                custom_query=query_str
            )

            results.extend(results_api)

        return results
    
    def consultar_fuentes_gaps(self, gaps_arg):
        resultados = []

        cant_gaps = len(gaps_arg)
        start_time = datetime.now()

        for i, gap_row in gaps_arg.iterrows():
            print(f"Iteración: {i+1} / {cant_gaps} \t\t[{datetime.now()-start_time}]")

            resultados_mmsi = self.fuentes_gap(gap_row)
            for r in resultados_mmsi:
                r["attributes"]["MMSI"] = gap_row["mmsi"]

            resultados.extend(resultados_mmsi)
            
            os.system('cls' if os.name == 'nt' else 'clear')

        if len(resultados) > 0:
            return parse_positions(resultados).reset_index(drop=True)
        else:
            return None
        
    def expandir_ais_gaps(self, gaps_arg):
        cols = [
            "mmsi", "msgdate", 
            "longitude", "latitude",
            "speedovergroud", "courseoverground",
            "geometry"
        ]
        ais_args = self.consultar_fuentes_gaps(gaps_arg)
        if ais_args is None:
            return parse_features(gaps_arg[cols])
        ais_args["msgdate"] = ais_args["msgtime"].apply(lambda x: datetime.fromtimestamp(int(x/1000)))
        
        cols = [
            "mmsi", "msgdate", 
            "longitude", "latitude",
            "speedovergroud", "courseoverground",
            "geometry"
        ]
        ais_args = ais_args[cols]

        ais_args = pd.concat([
            ais_args,
            gaps_arg[cols]
        ], ignore_index=True)
        
        return parse_features(ais_args)