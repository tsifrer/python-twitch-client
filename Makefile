test:
	py.test -v -s $(ARGS)

cov:
	py.test --cov=./