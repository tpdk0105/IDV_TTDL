.PHONY: help setup pipeline download eda clean forecast split db export validate test lint format serve

help:
	@echo "Available commands:"
	@echo "  make setup      - Install Python & Node.js dependencies"
	@echo "  make pipeline   - Run full end-to-end pipeline (01 to 08)"
	@echo "  make test       - Run test suite with pytest"
	@echo "  make lint       - Run ruff and eslint"
	@echo "  make format     - Run black and prettier"
	@echo "  make serve      - Start local dashboard preview server"

setup:
	pip install -r requirements.txt
	npm install
	npm run vendor

pipeline:
	python src/01_download.py
	python src/02_eda.py
	python src/03_clean.py
	python src/08_predictive_model.py
	python src/04_split_tables.py
	python src/05_build_db.py
	python src/07_validate.py

download:
	python src/01_download.py

eda:
	python src/02_eda.py

clean:
	python src/03_clean.py

forecast:
	python src/08_predictive_model.py

split:
	python src/04_split_tables.py

db:
	python src/05_build_db.py

validate:
	python src/07_validate.py

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/
	npm run lint

format:
	black src/ tests/
	npm run format

serve:
	npm run start
