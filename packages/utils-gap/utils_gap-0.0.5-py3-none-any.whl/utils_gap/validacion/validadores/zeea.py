from utils_pna.dist import haversine

class ValidadorZEEA:
    DELTA_DISTANCIA = 20 # 20 mn

    def __init__(self, limite_zeea, siguiente_validador):
        self.limite_zeea = limite_zeea
        self.estado_validacion = {
            "estado": "Irregular",
            "razon": "Cercano al limite ZEEA"
        }
        self.siguiente_validador = siguiente_validador

    def validar(self, contexto):
        if contexto.dict_buque["flag_name"] == "Argentina":
            return self.__validar_argentino(contexto)
        else:
            return self.__validar_extranjero(contexto)
        
    def __validar_argentino(self, contexto):
        """
        Por ahora lo dejo como polémico si ya es Argentino y hace GAP.
        """
        return self.estado_validacion
    
    def __validar_extranjero(self, contexto):
        if (
            self.__cercania_zeea(contexto.reporte_inicio.punto) or
            self.__cercania_zeea(contexto.reporte_fin.punto)
        ):
            return self.estado_validacion
        else:
            return self.siguiente_validador.validar(contexto)

    def __cercania_zeea(self, punto):
        punto_cercano = self.limite_zeea.interpolate(
            self.limite_zeea.project(punto)
        )
        return (
            haversine(
                punto, 
                punto_cercano, 
                unidad="mn"
            ) <= ValidadorZEEA.DELTA_DISTANCIA
        )