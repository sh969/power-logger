Repo to monitor different power meters in my local network and save readings to csv on a Synology using Docker.

To run the power-logger in a Docker container:
1) Download ubuntu:lastest from the Synology Docker container manager
2) SSH into Synology and run the following:
`sudo docker run -d --name power-logger --mount type=bind,source=/volume1/homes/sehor101/Drive/Code/Python/Power\ monitoring,target=/app ubuntu:latest sh /app/setup.sh`
3) if something does not work the Docker will stop, check the log and retry, remove old instance like so:
`sudo docker rm 8b0d65c69226099001b79901cbbb743c9c2bf5800ea201d84c627cb1dd49c0d3`

This will mount the right folder und run a setup which finally runs the script.