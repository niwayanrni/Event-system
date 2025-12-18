CREATE TABLE IF NOT EXISTS processed_events (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    event_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ,
    source TEXT,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (topic, event_id)
);

CREATE TABLE IF NOT EXISTS stats (
    key TEXT PRIMARY KEY,
    value BIGINT
);

INSERT INTO stats (key, value)
VALUES
('received', 0),
('unique_processed', 0),
('duplicate_dropped', 0)
ON CONFLICT DO NOTHING;
