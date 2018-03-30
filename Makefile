
.phony: default
default: run

# ==

.phony: init
init:
	@echo "TODO"

.phony: run
run:
	python3 project/__main__.py

.phony: test
test:
	pep8 --show-source --statistics --ignore=E402 project/

.phony: install
install:
	@echo "TODO"

# ==

.phony: help
help:
	@echo "Usage: make [init|run|install]"
