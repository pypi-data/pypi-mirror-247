from arcgis.features import GeoAccessor

def update_layer(gdf, gis, id_layer, initial_cols=["mmsi", "geometry"], delete=False):
    layer = gis.content.get(id_layer).layers[0]
    if len(gdf) > 0:
        gdf.crs = "EPSG:4326"
        sdf = GeoAccessor.from_geodataframe(gdf[initial_cols])

        for col in gdf.columns:
            if col not in sdf.columns and col != 'geometry':
                sdf[col.lower()] = gdf[col]
        fset = sdf.spatial.to_featureset()
        
        if delete:
            layer.delete_features(where="1=1")
        print(layer.edit_features(adds = fset))