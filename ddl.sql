CREATE TABLE IF NOT EXISTS proxies (id TEXT, name TEXT, description TEXT, illustration BLOB, value TEXT)
CREATE INDEX IF NOT EXISTS proxy_ids_index ON proxies (id)
CREATE INDEX IF NOT EXISTS proxy_values_index ON proxies (value)
