name="dump_"$(date +%F)
remote="bbuser@meetbk.kntu.ac.ir"
port=44022
#docker exec -t  greenlight_db_1  pg_dumpall -c -U postgres > /home/bbuser/greenlight/scripts/dumps/${name}
docker exec -t  greenlight_db_1  pg_dump -U postgres -c  greenlight_production > /home/bbuser/greenlight/scripts/dumps/${name}
scp -P${port} /home/bbuser/greenlight/scripts/dumps/${name} ${remote}:~/greenlight/backup/
#ssh -p${port} $remote "cat  /home/bbuser/greenlight/backup/${name} | docker exec -i  greenlight_db_1 psql -U postgres"i
ssh -p${port} $remote "/home/bbuser/greenlight/scripts/dump_restore.sh"
