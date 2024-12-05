.PHONY:  all build run setup

all: setup build run

setup:
	pipenv install --dev
	pipenv run pip install -r requirements.txt

build:
	npm install --prefix client-app
	npm run build --prefix client-app
	cp -r client-app/dist static

run:
	pipenv run uvicorn main:app --host 0.0.0.0 --port 8000