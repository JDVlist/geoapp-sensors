db → PostGIS
api → FastAPI
web → simpele OpenLayers frontend via nginx

sensor
  │ POST /measurements
  │ GeoJSON Feature
  ▼
FastAPI
  │ INSERT met SQL
  ▼
PostGIS
  │
  │ SELECT + ST_AsGeoJSON
  ▼
FastAPI → GeoJSON FeatureCollection


Geojson example:
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [5.1214, 52.0907]
  },
  "properties": {
    "temperature": 21.7,
    "humidity": 63
  }
}

[longitude, latitude]