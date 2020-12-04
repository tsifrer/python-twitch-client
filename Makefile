test:
	py.test -vsx $(ARGS)

cov:
	py.test --cov=./

cov-html:
	py.test --cov=./ --cov-report html

format:
	isort .
	black .

lint:
	flake8 .
	black --check .
