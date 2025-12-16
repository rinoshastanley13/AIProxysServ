#!/bin/bash

echo "Starting Infrastructure (Postgres, Botpress)..."
docker compose up -d

echo "Infrastructure started."
docker compose ps
