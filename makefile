rs:
	docker restart ai-web-1
rsdb:
	docker restart redis_test
log:
	docker logs ai-web-1
	
clearlog:
	sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' ai-web-1)

logdb:
	docker logs redis_test

e:
	docker exec -it ai-web-1 bash

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