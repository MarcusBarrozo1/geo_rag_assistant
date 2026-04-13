CREATE TABLE field_metrics (
    id SERIAL PRIMARY KEY,
    field_id VARCHAR(50) NOT NULL,
    record_date DATE NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    ndvi_score DECIMAL(3, 2),
    soil_moisture DECIMAL(5, 2),
    temperature DECIMAL(5, 2),
    agronomic_alert BOOLEAN DEFAULT FALSE
);

INSERT INTO field_metrics (field_id, record_date, crop_type, ndvi_score, soil_moisture, temperature, agronomic_alert) 
VALUES
    ('FIELD_ALPHA_01', '2026-04-01', 'Soybean', 0.82, 45.5, 28.1, FALSE),
    ('FIELD_ALPHA_01', '2026-04-02', 'Soybean', 0.81, 42.0, 29.5, FALSE),
    ('FIELD_ALPHA_01', '2026-04-03', 'Soybean', 0.75, 28.5, 33.2, TRUE), -- Drought alert
    ('FIELD_BETA_02', '2026-04-01', 'Corn', 0.65, 55.0, 25.4, FALSE),
    ('FIELD_BETA_02', '2026-04-02', 'Corn', 0.68, 54.2, 26.1, FALSE),
    ('FIELD_GAMMA_03', '2026-04-01', 'Cotton', 0.45, 22.0, 35.5, TRUE); -- Heat stress alert