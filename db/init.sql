CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS sensors;

CREATE TABLE IF NOT EXISTS sensors.measurements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,         -- generated primary key
    sensor_id TEXT NOT NULL DEFAULT 'sensor-001',               -- sensor id optional, 'sensor-001' if not delivered
    measured_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),             -- timestamp optional, now if not delivered
    properties JSONB NOT NULL DEFAULT '{}'::jsonb,              -- column for only the properties from the geojson
    geometry geometry(Geometry, 4326) NOT NULL                  -- WGS84
);

-- create a spatial index
CREATE INDEX IF NOT EXISTS measurements_geometry_idx
ON sensors.measurements
USING GIST (geometry);