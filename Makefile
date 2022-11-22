clean:
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/

run:
	python src/main.py

test:
	python -m unittest discover -s tests/ --locals

black:
	black src/*.py --line-length=79
	black tests/*.py --line-length=79

flake:
	flake8 src/*.py
	flake8 tests/*.py

check: black flake test clean