export PATH := /snap/bin:$(PATH)

# TARGETS
lint: ## Run linter
	tox -e lint

clean: ## Remove .tox, build dirs, and charms
	rm -rf .tox/
	rm -rf venv/
	rm -rf *.charm
	rm -rf charm-nfs-client/build
	rm -rf charm-nfs-server/build

nfs-server: ## Build nfs-server charm
	@charmcraft build --from charm-nfs-server

nfs-client: ## Build nfs-client charm
	@charmcraft build --from charm-nfs-client

charms: nfs-server nfs-client ## Build nfs server and client charms

# Display target comments in 'make help'
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# SETTINGS
# Use one shell for all commands in a target recipe
.ONESHELL:
# Set default goal
.DEFAULT_GOAL := help
# Use bash shell in Make instead of sh
SHELL := /bin/bash
