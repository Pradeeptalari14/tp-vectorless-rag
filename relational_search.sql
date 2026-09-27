-- PostgreSQL Full-Text Search Schema & GIN Index Configuration

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    tsv_body tsvector
);

CREATE INDEX IF NOT EXISTS doc_body_fts_idx ON documents USING GIN(tsv_body);

CREATE OR REPLACE FUNCTION documents_tsv_trigger()
RETURNS TRIGGER AS $$
BEGIN
    NEW.tsv_body := to_tsvector('english', NEW.body);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON documents FOR EACH ROW EXECUTE FUNCTION documents_tsv_trigger();

SELECT id, title, ts_rank(tsv_body, to_tsquery('english', $1)) AS rank
FROM documents
WHERE tsv_body @@ to_tsquery('english', $1)
ORDER BY rank DESC;
