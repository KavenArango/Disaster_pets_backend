createDock:
	docker build --tag pets:1.0 .
runDock:
	docker run --publish 5000:5000 --detach --name pet pets:1.0
rmDock:
	docker rm --force pet
fullDock:
	make createDock
	docker run --publish 5000:5000 --detach --name pet pets:1.0
getDep:
	pip3 freeze > requirements.txt
installDep:
	pip3 install -r requirements.txt
runcomp:
	docker-compose up
runflask:
	Flask run
restartDock:
	make rmDock
	make createDock
	make runDock

