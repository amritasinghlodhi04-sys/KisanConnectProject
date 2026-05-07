#!/usr/bin/env bash

set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

echo "Testing root and health endpoints"
curl -sS "${BASE_URL}/" | python3 -m json.tool
curl -sS "${BASE_URL}/health" | python3 -m json.tool

echo "Testing price engine"
curl -sS -X POST "${BASE_URL}/ml/price-engine" \
  -H "Content-Type: application/json" \
  -d '{"crop":"Tomato","state":"Madhya Pradesh","market":"Bhopal"}' | python3 -m json.tool

echo "Testing demand forecast"
curl -sS -X POST "${BASE_URL}/ml/demand-forecast" \
  -H "Content-Type: application/json" \
  -d '{"crop":"Onion","state":"Maharashtra","weeks":6}' | python3 -m json.tool

echo "Testing reputation score"
curl -sS -X POST "${BASE_URL}/ml/reputation-score" \
  -H "Content-Type: application/json" \
  -d '{"total_orders":120,"completed_orders":108,"rating":4.4}' | python3 -m json.tool

echo "Testing delivery match"
curl -sS -X POST "${BASE_URL}/ml/delivery-match" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup":{"lat":23.2599,"lon":77.4126},
    "partners":[
      {"partner_id":"d1","location":{"lat":23.2500,"lon":77.4000},"rating":4.5},
      {"partner_id":"d2","location":{"lat":23.1000,"lon":77.2000},"rating":4.8}
    ]
  }' | python3 -m json.tool

echo "Testing carbon footprint"
curl -sS -X POST "${BASE_URL}/ml/carbon-footprint" \
  -H "Content-Type: application/json" \
  -d '{"distance_km":18.5,"trips_per_day":3}' | python3 -m json.tool

echo "Testing seasonal calendar"
curl -sS -X POST "${BASE_URL}/ml/seasonal-calendar" \
  -H "Content-Type: application/json" \
  -d '{"crop":"Potato"}' | python3 -m json.tool

echo "All endpoint calls completed."
