all: start

start:
		docker-compose up -d

stop:
		docker-compose down

fclean: clean
		docker rmi -f $$(docker images -q)
		docker image prune -a -f
		docker system prune -a -f

clean:
		docker-compose down -v

re:	fclean all
