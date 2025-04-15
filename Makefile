.PHONY:  all build run setup

all: setup build run

setup:
	python3 -m pipenv install --dev
	python3 -m pipenv run pip install -r requirements.txt

build:
	npm install --prefix client-app
	npm run build --prefix client-app
	cp -r client-app/dist static

run:
	python3 -m pipenv run uvicorn main:app --host 0.0.0.0 --port 8000