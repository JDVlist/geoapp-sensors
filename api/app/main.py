import json
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import get_connection

"""
FastAPI verwerkt HTTP en JSON.
Uvicorn laat de API continu draaien.
Psycopg laat Python met PostgreSQL praten.

post request:
Sensor stuurt JSON
        ↓
FastAPI controleert de basisvorm
        ↓
Python zet delen om naar JSON-tekst
        ↓
SQL slaat de properties en geometrie op
        ↓
PostgreSQL geeft het nieuwe ID en tijdstip terug
        ↓
FastAPI stuurt een antwoord naar de sensor
"""


app = FastAPI(title="Sensor API")


class GeoJSONFeature(BaseModel):
    """
    Basemodel shape (GeoJSON complient)
    Pydantic uses this basemodel to verify incoming data
    """

    #TODO: make this more specific GeoJSON complient: https://geojson.org/ 
    type: str
    geometry: dict[str, Any]
    properties: dict[str, Any] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/measurements", status_code=201)
def create_measurement(feature: GeoJSONFeature):    # FastAPI automatically uses the BaseModel to verify the input and create feature of type GeoJSONFeature

    if feature.type != "Feature":
        # this means the creation of feature faild; the input is not according to the standard in BaseModel
        raise HTTPException(
            status_code=400,
            detail="Body must be a valid GeoJSON",
        )

    #TODO: hardcoded for now, make this more dynamic in the future
    #TODO: assumes WGS84, make more dynamic in the future
    sql = """
        INSERT INTO sensors.measurements (
            sensor_id,
            properties,
            geometry
        )
        VALUES (
            'sensor-001',               
            %(properties)s::jsonb,
            ST_SetSRID(
                ST_GeomFromGeoJSON(%(geometry)s),
                4326                    
            )
        )
        RETURNING id, measured_at;
    """

    with get_connection() as connection:    # connect to db
        with connection.cursor() as cursor:     # cursor to execute SQL
            cursor.execute(
                sql,
                {
                    "properties": json.dumps(feature.properties),   # python dict to text
                    "geometry": json.dumps(feature.geometry),
                },
            )
            measurement_id, measured_at = cursor.fetchone()  # get the 2 values of the resulting db entry

    return {
        "id": measurement_id,
        "sensor_id": "sensor-001",
        "measured_at": measured_at,
    }

#TODO: create get request