# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PROJECT_NAME = dataset-football
SRC_DIR = src
TEST_DIR = tests
CRAWLER_SCRIPT = $(SRC_DIR)/main.py

# Environnement virtuel et dépendances
.PHONY: setup
setup: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

.PHONY: install
install: setup

# Nettoyage
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type f -name ".DS_Store" -delete

.PHONY: clean-venv
clean-venv: clean
	rm -rf $(VENV)

# Tests
.PHONY: test
test:
	$(PYTHON) -m pytest $(TEST_DIR) -v --cov=$(SRC_DIR)

# Linting et formatage
.PHONY: lint
lint:
	$(PYTHON) -m flake8 $(SRC_DIR)
	$(PYTHON) -m flake8 $(TEST_DIR)

.PHONY: format
format:
	$(PYTHON) -m black $(SRC_DIR)
	$(PYTHON) -m black $(TEST_DIR)

# Exécution du crawler
.PHONY: run
run:
	$(PYTHON) $(CRAWLER_SCRIPT)

# Sécurité
.PHONY: security
security:
	$(PYTHON) -m safety check
	$(PYTHON) -m bandit -r $(SRC_DIR)

# Génération des dépendances
.PHONY: freeze
freeze:
	$(PIP) freeze > requirements.txt

# Documentation
.PHONY: docs
docs:
	$(PYTHON) -m pdoc --html --output-dir docs $(SRC_DIR)

# Aide
.PHONY: help
help:
	@echo "Commandes disponibles:"
	@echo "  make setup      - Crée l'environnement virtuel et installe les dépendances"
	@echo "  make install    - Alias pour setup"
	@echo "  make clean      - Nettoie les fichiers Python compilés et les caches"
	@echo "  make clean-venv - Nettoie tout, y compris l'environnement virtuel"
	@echo "  make test       - Lance les tests avec couverture"
	@echo "  make lint       - Vérifie le style du code"
	@echo "  make format     - Formate le code avec black"
	@echo "  make run        - Lance le crawler"
	@echo "  make security   - Lance les vérifications de sécurité"
	@echo "  make freeze     - Met à jour requirements.txt"
	@echo "  make docs       - Génère la documentation"

# Par défaut
.DEFAULT_GOAL := help