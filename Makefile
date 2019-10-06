.PHONY: FORCE

install: FORCE
	pip install -e .

install-dev: FORCE
	pip install -e ".[develop]"

test: FORCE
	pytest tests -v --durations=5 --lf

test-detail: FORCE
	pytest tests -vv -s --durations=5

lint: FORCE
	flake8 ./awslogs_watch; mypy --config-file .mypy.ini ./awslogs_watch

format: FORCE
	black awslogs_watch tests

upload: FORCE
	python setup.py bdist_wheel
	twine upload dist/*
	rm -rf dist
