# GeoApp Sensors

A small full-stack Geo-ICT learning project for ingesting, storing and eventually visualising spatial sensor measurements.

The project explores how a modern geospatial application can be built from separate components: an HTTP API, a spatial database and, in a later stage, a web map frontend.

> **Project status:** work in progress.
> The current version implements the backend ingestion flow with FastAPI and PostGIS. Querying and visualising the stored measurements are the next major steps.

## Why this project?

I work with GIS and Python and built this project to better understand how the different parts of an open-source web-GIS stack fit together.

Rather than using a desktop GIS application as the centre of the architecture, the goal is to work towards a small API-first geospatial application:

```text
sensor / client
      |
      | POST GeoJSON
      v
   FastAPI
      |
      | SQL
      v
 PostgreSQL
   + PostGIS
      |
      | GeoJSON
      v
   Web map
```

The project is intentionally small. Its purpose is to learn the fundamentals behind spatial APIs, database-backed applications, containers and web GIS by building the complete data flow myself.

## Current functionality

The application currently supports:

* running the API and database with Docker Compose;
* automatically enabling PostGIS and creating the database schema;
* receiving measurements through a FastAPI endpoint;
* validating the basic structure of an incoming GeoJSON Feature;
* converting GeoJSON geometry to a PostGIS geometry;
* storing arbitrary sensor properties as `JSONB`;
* storing measurement locations as spatial data in EPSG:4326;
* creating a GiST spatial index;
* exposing a simple health endpoint.

A measurement currently follows this flow:

```text
GeoJSON Feature
      |
POST /measurements
      |
      v
   FastAPI
      |
      | psycopg
      v
   PostGIS
      |
      v
 spatial measurement
```

## Tech stack

| Component        | Technology              |
| ---------------- | ----------------------- |
| API              | Python, FastAPI         |
| API server       | Uvicorn                 |
| Database         | PostgreSQL              |
| Spatial database | PostGIS                 |
| Database driver  | psycopg                 |
| Validation       | Pydantic                |
| Containers       | Docker / Docker Compose |
| Data format      | GeoJSON                 |

A web mapping frontend is planned as a later stage of the project.

## Data model

Measurements are stored in `sensors.measurements`.

The table contains:

* `id` — generated primary key;
* `sensor_id` — identifier of the sensor;
* `measured_at` — timestamp of the measurement;
* `properties` — flexible sensor attributes stored as JSONB;
* `geometry` — PostGIS geometry in EPSG:4326.

The flexible `properties` field means different sensors can provide different attributes without requiring a database column for every measurement type.

For example:

```json
{
  "temperature": 21.7,
  "humidity": 63
}
```

The geometry is stored separately as actual PostGIS spatial data, allowing spatial indexing and spatial queries.

## API

### Health check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Create a measurement

```http
POST /measurements
Content-Type: application/json
```

Example request:

```json
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
```

GeoJSON coordinates are ordered as:

```text
[longitude, latitude]
```

The geometry is converted to a PostGIS geometry and the properties are stored as JSONB.

The current API assigns a temporary hardcoded sensor ID. Supporting sensor metadata properly is part of the planned work.

## Running locally

### Requirements

You need:

* Docker;
* Docker Compose.

No local PostgreSQL or Python installation is required when running the application through Docker.

### 1. Clone the repository

```bash
git clone https://github.com/JDVlist/geoapp-sensors.git
cd geoapp-sensors
```

### 2. Configure the environment

Copy the example environment file:

```bash
cp .env-example .env
```

Then configure the database credentials:

```env
DB_USER=postgres
DB_PASS=your-password
DB_NAME=sensors
```

The `.env` file is ignored by Git and should not contain credentials that are committed to the repository.

### 3. Start the application

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

The PostgreSQL container is exposed locally on port `54321`.

### 4. Check the API

```bash
curl http://localhost:8000/health
```

### 5. Insert a measurement

```bash
curl -X POST http://localhost:8000/measurements \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [5.1214, 52.0907]
    },
    "properties": {
      "temperature": 21.7,
      "humidity": 63
    }
  }'
```

## Project structure

```text
geoapp-sensors/
├── api/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── requirements.txt
│   └── Dockerfile
├── db/
│   └── init.sql
├── .env-example
├── docker-compose.yml
└── README.md
```

The main responsibilities are deliberately kept separate:

* `api/` contains the FastAPI application;
* `db/` contains database initialisation;
* `docker-compose.yml` connects the application services.

## Next steps

The next phase is to turn the current ingestion prototype into a small end-to-end spatial application.

### Improve the API contract

The current Pydantic model only validates the basic shape of the incoming object.

A next step is stricter validation of the supported GeoJSON structure, particularly:

* requiring a GeoJSON `Feature`;
* defining which geometry types the sensor API accepts;
* validating coordinates more explicitly;
* keeping the API's coordinate reference system contract clear.

For this project, measurements will initially use WGS84 coordinates (`EPSG:4326`), matching the coordinate model normally used by GeoJSON.

### Model sensors explicitly

`sensor-001` is currently hardcoded.

The API should eventually distinguish between sensors and measurements so that measurements can be associated with a real sensor identifier and, potentially, sensor metadata.

### Query measurements

Add read endpoints that retrieve stored measurements and expose them as GeoJSON.

The first useful version could return a GeoJSON `FeatureCollection`, followed by filters such as:

* sensor ID;
* time range;
* spatial bounding box.

This will turn the API from an ingestion-only service into a spatial data service.

### Build the web map

Once measurements can be retrieved as GeoJSON, add a small web frontend using a browser mapping library such as OpenLayers.

The frontend should consume the API rather than connect directly to the database.

That completes the intended flow:

```text
sensor
  |
  | POST GeoJSON
  v
FastAPI
  |
  v
PostGIS
  |
  | spatial query
  v
FastAPI
  |
  | GeoJSON FeatureCollection
  v
web map
```

### Continue towards a production-style architecture

After the basic end-to-end application works, possible learning topics include:

* automated API tests;
* database migrations;
* connection pooling;
* structured application configuration;
* logging and error handling;
* CI/CD;
* authentication for data ingestion;
* deployment behind a reverse proxy.

These are intentionally later steps. The current goal is first to understand and implement the complete spatial data flow.

## What I am learning

This repository is primarily a learning and portfolio project.

Topics I am using it to explore include:

* designing a small API-first geospatial application;
* working with HTTP and REST APIs;
* validating spatial JSON with FastAPI and Pydantic;
* using SQL from Python with psycopg;
* storing GeoJSON in PostGIS;
* deciding what belongs in relational columns, JSONB and geometry columns;
* spatial indexing;
* container networking and persistent volumes;
* separating database, backend and frontend responsibilities;
* serving spatial data to a browser as GeoJSON.

The emphasis is not only on making the application work, but on understanding why the individual components exist and how they communicate.

## Disclaimer

This is an educational project and is not intended for production use in its current form.
