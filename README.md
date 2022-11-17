# SarsCov2 Reporter
Dockerized version of the sc2reporter program.

## To run with dummy data:
Make sure you have docker-compose installed on your system, and then
```bash
git clone https://github.com/genomic-medicine-sweden/docker-sc2reporter
cd docker-sc2reporter
docker-compose -f docker-compose.yaml up
```

Then navigate to localhost:3000 for the front end and localhost:8000 for the back-end