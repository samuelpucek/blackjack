clean:
	rm -rf src/__pycache__/
	rm -rf src/utils/__pycache__/
	rm -rf tests/__pycache__/

run:
	python src/main.py

test:
	python -m unittest discover -s tests/ --locals

black:
	black src/*.py --line-length=79
	black src/utils/*.py --line-length=79
	black tests/*.py --line-length=79

flake:
	flake8 src/*.py
	flake8 src/utils/*.py --per-file-ignores="__init__.py:F401"
	flake8 tests/*.py

check: black flake test clean