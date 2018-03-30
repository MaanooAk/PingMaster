
.phony: default
default: run

# ==

.phony: init
init:
	@echo "TODO"
	
.phony: run
run:
	python3 project/__main__.py

.phony: install
install:
	@echo "TODO"

# ==

.phony: help
help:
	@echo "Usage: make [init|run|install]"
