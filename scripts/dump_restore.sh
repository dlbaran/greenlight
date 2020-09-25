#!/bin/bash
dump_name=$1
cat /greenlight/backup/${dump_name} | sudo docker exec -i   greenlight_db_1 psql -U postgres
