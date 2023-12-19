from utils_gap.validacion.validadores.severidad import ValidadorSeveridad
from utils_gap.validacion.validadores.zeea import ValidadorZEEA
from utils_gap.validacion.validadores.velocidad import ValidadorVelocidad
from utils_gap.validacion.validadores.elipse import ValidadorElipse
from utils_gap.validacion.validadores.cantidad_posiciones import ValidadorCantidadPosiciones
from utils_gap.validacion.validadores.trayectoria import ValidadorTrayectoria

class Validador:
    def __init__(self):
        self.estado_validacion = {
            "estado": "Irregular",
            "razon": "Sin validación"
        }

    def validar(self, contexto):
        return self.estado_validacion

def crear_validador(instancia, siguiente_validador):
    if isinstance(instancia, tuple):
        instancia_validador, *args = instancia
        return instancia_validador(*args, siguiente_validador)
    else:
        return instancia(siguiente_validador)
    

def crear_pipeline_validacion(limite_zeea):
    orden_validacion = [
        ValidadorSeveridad,
        (ValidadorZEEA, limite_zeea),
        ValidadorVelocidad,
        (ValidadorElipse, limite_zeea),
        ValidadorCantidadPosiciones,
        ValidadorTrayectoria, 
        Validador
    ]

    validador = None
    for i in reversed(range(len(orden_validacion))):
        if i == len(orden_validacion)-1:
            validador = orden_validacion[i]()
        else:
            aux = crear_validador(orden_validacion[i], validador)
            validador = aux

    return validador