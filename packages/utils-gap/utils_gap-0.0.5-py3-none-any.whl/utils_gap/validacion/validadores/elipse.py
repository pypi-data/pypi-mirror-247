import os
from geopandas import GeoDataFrame
from shapely.geometry import Point, Polygon
from utils_pna.geom import elipse

class ValidadorElipse:
    MIN_VELOCIDAD_ILEGAL = 12 / 0.5399568
    
    def __init__(self, limite_zeea, siguiente_validador):
        self.estado_validacion = {
            "estado": "Irregular",
            "razon": "Zona de influencia peligrosa"
        }
        self.limite_zeea = limite_zeea
        self.siguiente_validador = siguiente_validador

    def validar(self, contexto):
        if self.__zona_influencia_peligrosa(contexto):
            return self.estado_validacion
        else:
            return self.siguiente_validador.validar(contexto)
        
    def __zona_influencia_peligrosa(self, contexto):
        zona_inf = self.__calcular_zona_influencia(contexto)
        if zona_inf is not None:
            #self.__escribir_zona_influencia(zona_inf, contexto)
            return zona_inf.intersects(self.limite_zeea)
        else:
            return False

    def __calcular_zona_influencia(self, contexto):
        l = ValidadorElipse.MIN_VELOCIDAD_ILEGAL * contexto.tiempo_gap
        p1 = [contexto.reporte_inicio.punto.x, contexto.reporte_inicio.punto.y]
        p2 = [contexto.reporte_fin.punto.x, contexto.reporte_fin.punto.y]

        try:
            puntos_elipse = elipse(p1, p2, l)
            zona_inf = Polygon([Point(x, y) for x, y in puntos_elipse])
        except ValueError:
            zona_inf = None
        
        return zona_inf
    
    def __escribir_zona_influencia(self, zona_inf, contexto):
        gdf = GeoDataFrame({
            "id_gap": [contexto.dict_gap["id_gap"]],
            "geometry": [zona_inf]
        })

        file = "/output/elipses.csv"
        if os.path.exists(file):
            gdf.to_csv(file, mode='a', header=False, index=False)
        else:
            gdf.to_csv(file, index=False)
