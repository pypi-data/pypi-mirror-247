from shapely.geometry import Polygon

def obtener_limite_zeea(gis, id_layer_areas):
    layer = gis.content.get(id_layer_areas).layers[0]
    areas = layer.query().sdf

    area_zeea = areas.loc[areas.fna == "Interior ZEEA"]
    area_zeea['geom'] = area_zeea.SHAPE.apply(lambda r: Polygon(r["rings"][0]))
    poly_zeea = area_zeea["geom"].values[0]
    return poly_zeea.boundary