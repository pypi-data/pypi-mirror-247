class ValidadorCantidadPosiciones:
    def __init__(self, siguiente_validador):
        self.estado_validacion = {
            "estado": "Irregular",
            "razon": "Sin posiciones para estimar trayectoria futura"
        }
        self.siguiente_validador = siguiente_validador

    def validar(self, contexto):
        if not self.__validar_posiciones_anteriores(contexto):
            return self.estado_validacion
        else:
            return self.siguiente_validador.validar(contexto)
    
    def __validar_posiciones_anteriores(self, contexto):
        return (
            len(contexto.reporte_inicio.posiciones_anteriores) > 0
        )