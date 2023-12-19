import numpy as np
import pyproj
from datetime import timedelta
from shapely.geometry import Point, Polygon
from utils_pna.dist import haversine
from utils_pna.geom import elipse

# TODO: testear esta proyección
GEODESIC = pyproj.Geod(ellps='WGS84')
def estimar_curso(punto_inicial, punto_final):
    curso_estimado, _, _ = GEODESIC.inv(
        punto_inicial.x, punto_inicial.y,
        punto_final.x, punto_final.y
    )

    return curso_estimado

def estimar_velocidad(puntos, fechas):
    estimaciones = np.array([])

    for i in range(0, len(puntos)-1):
        if (fechas[i+1] - fechas[i]) == timedelta(hours=0): continue
        dist_recorrida = haversine(
            puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1],
            unidad="mn"
        )
        tiempo = (fechas[i+1] - fechas[i]).total_seconds() / 3600

        estimacion = dist_recorrida / tiempo
        estimaciones = np.append(estimaciones, estimacion)

    return np.mean(estimaciones)

def angulo(p1, p2):
    angle, _, _ = GEODESIC.inv(
        p1[0], p1[1],
        p2[0], p2[1]
    )

    return angle

def circulo_restringido(punto_central, radio, angulo_inicio, angulo_fin, n_samples=400):
    circulo = elipse(punto_central, punto_central, 2*radio)
    puntos_restringidos = []
    for punto in circulo:
        if angulo_inicio <= angulo(punto_central, punto) <= angulo_fin:
            puntos_restringidos.append(punto)

    puntos_restringidos.append(punto_central)
    return Polygon([Point(lat, lon) for lat, lon in puntos_restringidos])

def posicion_regular(punto_final, pol_menor, pol_mayor):
    intersecta_menor = punto_final.intersects(pol_menor).values[0]
    intersecta_mayor = punto_final.intersects(pol_mayor).values[0]

    return (not intersecta_menor) and (intersecta_mayor)

def area_proyeccion(
        reporte_inicio, 
        reporte_fin, 
        estimacion_velocidad, 
        estimacion_curso,
        angulo_corona,
        delta_tiempo
):
    punto_central = (reporte_inicio.punto.x, reporte_inicio.punto.y)
    angulo_inicio = estimacion_curso - angulo_corona
    angulo_fin = estimacion_curso + angulo_corona

    tiempo_gap = (reporte_fin.fecha - reporte_inicio.fecha).total_seconds() / 3600
    radio_inicio = estimacion_velocidad * (tiempo_gap - delta_tiempo)
    radio_fin = estimacion_velocidad * (tiempo_gap + delta_tiempo)

    circulo_menor = circulo_restringido(punto_central, radio_inicio, angulo_inicio, angulo_fin)
    circulo_mayor = circulo_restringido(punto_central, radio_fin, angulo_inicio, angulo_fin)

    return circulo_menor, circulo_mayor

def grupos_velocidad(velocidad, step=2, max_value=12):
    speed_ranges = [(i, min(i+step, max_value)) for i in range(0, max_value, step)]

    for lower, upper in speed_ranges:
        if lower <= velocidad < upper:
            return f"{lower}-{upper} nudos"

    return f"> {max_value} nudos" if velocidad > max_value else "Sin reporte"