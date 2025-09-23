#! /bin/bash

echo "Starting data pipeline..."
python3 data_pipeline.py
echo "Finished data pipeline."

docker-compose down
echo "Moving data..."
cp -r data/ ../YoyoMut_data/
echo "Finished moving data."
docker-compose up -d
