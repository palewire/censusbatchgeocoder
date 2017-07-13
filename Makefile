.PHONY: ship

test:
	flake8 censusbatchgeocoder
	coverage run setup.py test
	coverage report -m

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing
