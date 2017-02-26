test:
	py.test -v -s $(ARGS)

cov:
	py.test --cov=./

cov-html:
	py.test --cov=./ --cov-report html