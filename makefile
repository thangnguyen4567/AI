rs:
	docker restart webai_test
log:
	docker logs webai_test
e:
	docker exec -it webai_test bash
down:
	docker-compose down
up:
	docker-compose up -d
ps:
	docker ps