start:
	docker-compose up -d

restart:
	docker-compose down
	docker-compose build
	docker-compose up -d

serve:
	docker-compose up

test:
	docker-compose exec tensorflow-back pytest $(arg)
