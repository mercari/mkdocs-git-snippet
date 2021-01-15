.PHONY: dep
dep:
	pip install -r requirements.txt

.PHONY: bump
bump:
	pip install bumpversion
	bumpversion $(v)

.PHONY: test
test:
	python3 -m pytest -s -r w
