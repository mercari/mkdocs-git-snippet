.PHONY: dep
dep:
	pip install -r requirements.txt

.PHONY: dep-dev
dep-dev: dep
	pip install -r requirements-dev.txt

.PHONY: bump
bump:
	bumpversion $(v)

.PHONY: test
test:
	python3 -m pytest -s -r w
