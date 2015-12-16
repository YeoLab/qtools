help:
	@echo "lint - check code style with flake8"
	@echo "test - run tests only"
	@echo "coverage - run tests and check code coverage"

test:
	py.test

coverage:
	coverage run --source qtools --omit="*/test*" --module py.test
	coverage report --show-missing

lint:
	flake8 --exclude docs qtools
