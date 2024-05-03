all:
		docker-compose up --build -d

fclean: clean
		docker rmi -f $$(docker images -q)
		docker image prune -a -f
		docker system prune -a -f

clean:	
		docker-compose down -v 


start:	
		docker-compose up -d

re:	fclean all