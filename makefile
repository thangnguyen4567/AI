rs:
	docker restart webai_test

log:
	docker logs webai_test
	
clearlog:
	sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' webai_test)

logdb:
	docker logs redis_test

e:
	docker exec -it webai_test bash

edb:
	docker exec -it redis_test bash
	
down:
	docker-compose down

up:
	docker-compose up -d

ps:
	docker ps

db:
	docker cp redis:/data/dump.rdb ./