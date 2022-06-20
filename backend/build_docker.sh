echo "Build backend..."
docker build -t huionlune_backend:v0.0.1 -f Dockerfile .

echo "Composing..."

echo "============"
echo "Visit http://localhost:8088/ to intereact with API"
echo "============"

sleep 5

docker-compose up $1