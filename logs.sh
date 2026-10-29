#!/bin/bash
# Stream live logs from all ShopRaven services on AWS EC2
if docker compose version &> /dev/null; then
    docker compose logs -f --tail=100 "$@"
else
    docker-compose logs -f --tail=100 "$@"
fi
