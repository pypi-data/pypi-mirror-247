from utils_pna.dist import haversine

class ValidadorVelocidad:
    MIN_VELOCIDAD = 12
    def __init__(self, siguiente_validador):
        self.estado_validacion = {
            "estado": "Regular",
            "razon": "Evento suficientemente rápido"
        }
        self.siguiente_validador = siguiente_validador

    def validar(self, contexto):
        if self.__recorrido_veloz(contexto):
            return self.estado_validacion
        else:
            return self.siguiente_validador.validar(contexto)
        
    def __recorrido_veloz(self, contexto):
        dist_recorrida = haversine(
            contexto.reporte_inicio.punto, 
            contexto.reporte_fin.punto,
            unidad="mn"
        )
        return (
            (dist_recorrida / contexto.tiempo_gap) >= ValidadorVelocidad.MIN_VELOCIDAD
        )