from utils_gap.validacion.utils import (
    estimar_curso, 
    estimar_velocidad, 
    area_proyeccion, 
    grupos_velocidad
)

class ValidadorTrayectoria:
    def __init__(self, siguiente_validador):
        self.estado_validacion = {
            "estado": "Regular",
            "razon": "Trayectoria coincide con su proyección"
        }
        self.siguiente_validador = siguiente_validador

    def validar(self, contexto):
        if self.__posicion_regular(contexto):
            return self.estado_validacion
        else:
            return self.siguiente_validador.validar(contexto)
        
    def __posicion_regular(self, contexto):
        estimacion_curso = estimar_curso(contexto.reporte_inicio.punto, contexto.reporte_fin.punto)

        puntos, fechas = self.__lista_posiciones_fechas(contexto.reporte_inicio, contexto.reporte_fin)
        estimacion_velocidad = estimar_velocidad(puntos, fechas)
        contexto.dict_gap["speed_group"] = grupos_velocidad(estimacion_velocidad)

        area_menor, area_mayor = area_proyeccion(
            contexto.reporte_inicio,
            contexto.reporte_fin,
            estimacion_velocidad,
            estimacion_curso,
            5,
            0.3
        )

        intersecta_menor = contexto.reporte_fin.punto.intersects(area_menor)
        intersecta_mayor = contexto.reporte_fin.punto.intersects(area_mayor)

        return (not intersecta_menor) and (intersecta_mayor)
    
    def __lista_posiciones_fechas(self, reporte_inicio, reporte_fin):
        lats = reporte_inicio.posiciones_anteriores["latitude"].tolist()
        lats.append(reporte_inicio.punto.y)
        lats.append(reporte_fin.punto.y)

        lons = reporte_inicio.posiciones_anteriores["longitude"].tolist()
        lons.append(reporte_inicio.punto.x)
        lons.append(reporte_fin.punto.x)

        puntos = [(lon_i, lats[i]) for i, lon_i in enumerate(lons)]

        fechas = reporte_inicio.posiciones_anteriores["msgdate"].tolist()
        fechas.append(reporte_inicio.fecha)
        fechas.append(reporte_fin.fecha)

        return puntos, fechas