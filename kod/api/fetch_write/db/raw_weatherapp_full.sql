CREATE TABLE raw__weatherapp_full (
  ingestion_timestamp timestamptz NOT NULL,
  params jsonb NOT NULL,
  data   jsonb NOT NULL
);