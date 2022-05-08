all: build

run:
	python main.py

run2:
	python main2.py

pack:
	zip stylight.zip .gitignore *.sql *.py *.md Makefile

build:
	python3 -m venv venv; \
	pip3 install -r requirements.txt


clean:
	rm -rf venv