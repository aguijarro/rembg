# rembg
#### Remove services
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml down --volumes --remove-orphans

#### Start the services
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml up -d --build

#### See logs
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml logs -f rembg_mongodb_dev

#### Execute pytest
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml exec -u appuser rembg_mongodb_dev python -m pytest -v

#### Test the health endpoint
curl http://localhost:8005/api/v1/health

curl -X POST "http://localhost:8005/api/v1/health_db?name=test_item" -H "Content-Type: application/json"

curl -X POST "http://localhost:8005/api/v1/health_db" -H "Content-Type: application/json" -d '{"name": "test_item"}'

curl http://localhost:8005/api/v1/health_db
