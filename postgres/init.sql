CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE ships (

    mmsi VARCHAR(20) PRIMARY KEY,

    name VARCHAR(100),

    imo VARCHAR(20),

    ship_type VARCHAR(50),

    flag VARCHAR(50)

);

CREATE TABLE canal_area (

    id SERIAL PRIMARY KEY,

    name VARCHAR(100),

    geom GEOMETRY(POLYGON,4326)

);

CREATE TABLE position_reports (

    id SERIAL PRIMARY KEY,

    mmsi VARCHAR(20) NOT NULL,

    canal_area_id INT,

    latitude DOUBLE PRECISION NOT NULL,

    longitude DOUBLE PRECISION NOT NULL,

    speed DOUBLE PRECISION,

    course DOUBLE PRECISION,

    report_time TIMESTAMP,

    geom geometry(Point,4326)
        GENERATED ALWAYS AS (
            ST_SetSRID(
                ST_MakePoint(longitude, latitude),
                4326
            )
        ) STORED,

    CONSTRAINT fk_ship
        FOREIGN KEY (mmsi)
        REFERENCES ships(mmsi),

    CONSTRAINT fk_canal
        FOREIGN KEY (canal_area_id)
        REFERENCES canal_area(id)

);