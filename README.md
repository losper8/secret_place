docker build -t distributor-service .
docker run -d -p 50443:50443 --name distributor distributor-service

docker network connect distributor-network distributor
