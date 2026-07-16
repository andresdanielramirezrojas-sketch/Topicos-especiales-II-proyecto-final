-- Tabla de áreas de canal (opcional)
CREATE TABLE IF NOT EXISTS canal_area (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY
);

-- Tabla de barcos
CREATE TABLE IF NOT EXISTS ships (
    id SERIAL PRIMARY KEY,
    mmsi BIGINT UNIQUE,
    name VARCHAR(100),
    type VARCHAR(50),
    flag VARCHAR(50)
);

-- Crear tabla de reportes de posición
CREATE TABLE IF NOT EXISTS position_reports (
    id SERIAL PRIMARY KEY,
    mmsi BIGINT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    speed DOUBLE PRECISION,
    course DOUBLE PRECISION,
    report_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    geom GEOMETRY(Point, 4326)
);

