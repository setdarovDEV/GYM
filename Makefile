pg_con:
	run -it --name pg -e POSTGRES_PASSWORD=1 -p 5433:5432 -d postgres:alpine

build:
	docker build -t gymbot:alpine .
	docker run -it --name gym_bot_con gymbot:alpine


restart:
	docker container stop gym_bot_con
	docker container rm gym_bot_con
	docker image rm gymbot:alpine
	docker build -t gymbot:alpine .
	docker run -it --name gym_bot_con gymbot:alpine



