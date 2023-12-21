from shapely.ops import transform
def _round_coordinates(geom, ndigits=2):    
   def _round_coords(x, y, z=None):
      x = round(x, ndigits)
      y = round(y, ndigits)
      if z is not None:
          z = round(x, ndigits)
          return (x,y,z)
      else:
          return (x,y)
   return transform(_round_coords, geom)
def _read_file_(file_path, n_deci= None, crs1="EPSG:4326"):
    import warnings, json
    warnings.simplefilter('ignore')
    from geopandas import read_file, GeoDataFrame
    if file_path.endswith('.shp'):gdf = read_file(file_path, engine='pyogrio')
    with open(file_path, 'r') as f:
        geojson_data = json.load(f)
    gdf = GeoDataFrame.from_features(geojson_data).set_crs(crs=crs1)
    if n_deci is not None: gdf['geometry'] = gdf['geometry'].apply(lambda x: _round_coordinates(x, n_deci).buffer(0))
    return gdf