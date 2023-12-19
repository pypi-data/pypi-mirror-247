class ValidadorSeveridad:
    def __init__(self, siguiente_validador):
        self.estado_validacion = {
            "estado": "Irregular",
            "razon": "Severidad alta"
        }
        self.siguiente_validador = siguiente_validador

    def validar(self, contexto):
        severidad = contexto.dict_gap["type_gap"]
        if severidad != "Moderado":
            est = self.estado_validacion.copy()
            est["razon"] = f"Severidad {severidad}"
            return est
        else:
            return self.siguiente_validador.validar(contexto)