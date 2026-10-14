#!/bin/sh
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -v app_password="$APP_DB_PASSWORD" -v evaluator_password="$EVALUATOR_DB_PASSWORD" <<'SQL'
CREATE ROLE aml_app LOGIN PASSWORD :'app_password';
CREATE ROLE aml_evaluator LOGIN PASSWORD :'evaluator_password';
CREATE DATABASE aml_test OWNER aml_owner;
SQL
