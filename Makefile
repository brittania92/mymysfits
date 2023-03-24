all: install unit-test integ-test build-frontend
.PHONY: install unit-test integ-test build-frontend

install:
	python3 -m pip install -r requirements-dev.txt
	
unit-test:
	pytest -k unit
	
integ-test:
	pytest -k integ

build-frontend:
	cd web && npm install && npm run build-only && git checkout web/build/.gitkeep