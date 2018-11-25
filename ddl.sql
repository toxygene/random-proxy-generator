CREATE TABLE IF NOT EXISTS cards (id TEXT, name TEXT, description TEXT, illustration BLOB, value TEXT)
CREATE INDEX IF NOT EXISTS card_ids_index ON cards (id)
CREATE INDEX IF NOT EXISTS card_values_index ON cards (value)
