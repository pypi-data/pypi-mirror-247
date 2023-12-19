import json
from utils_pna.queries import QueryAPI

class API:
    def __init__(self, query_api, values, name):
        self.name = name
        self.query_api = query_api
        self.values = values
        self.query_idxs = {}

    def keys(self, map_keys):
        for value in self.values:
            if value in map_keys:
                self.query_idxs[value] = map_keys[value]

def formar_fuentes(gis):
    with open("./work/apis.json", "r") as archivo:
        info_apis = json.load(archivo)
    
    apis = []

    for nombre, info in info_apis.items():
        api = API(
            QueryAPI(gis, info["api"]),
            info["registros"],
            nombre
        )

        apis.append(api)

    return apis