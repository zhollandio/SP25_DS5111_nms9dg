.PHONY: update ygainers.csv lint test lint-test gainers gainers-strategy
# create/update virtual env and install dependencies
update:
	@echo "Setting up virtual environment and installing dependencies..."
	python3 -m venv env
	./env/bin/pip install --upgrade pip
	./env/bin/pip install -r requirements.txt
	@echo "Virtual environment setup complete."
# test headless chrome - dump example.com content into a CSV file.
ygainers.csv:
	@echo "Testing headless Chrome on example.com..."
	google-chrome --headless --disable-gpu --dump-dom https://example.com > sample_data/ygainers.csv
	@echo "Output saved to sample_data/ygainers.csv"
# run pylint on .py files (prevents failure from stopping make)
lint:
	@echo "Running pylint..."
	- . env/bin/activate && pylint bin/*.py || true
	@echo "Linting complete."
# run pytest after linting (run even if lint fail)
test:
	@echo "Running linter first..."
	make lint
	@echo "Running tests..."
	. env/bin/activate && PYTHONPATH=$(PWD) pytest -vv tests/
	@echo "Testing complete."
# runs linter 1st --> tests
lint-test: test
# run gainers script with specified source
gainers:
	@if [ -z "$(SRC)" ]; then \
		echo "Error: SRC parameter is required. Use 'make gainers SRC=yahoo', 'make gainers SRC=wsj', 'make gainers SRC=mock', or 'make gainers SRC=cnbc'"; \
		exit 1; \
	fi
	@echo "Fetching gainers from $(SRC)..."
	. env/bin/activate && PYTHONPATH=$(PWD) python get_gainer.py $(SRC)
	@echo "Gainers fetched from $(SRC)."

# run gainers with strategy pattern (extra credit)
gainers-strategy:
	@if [ -z "$(SRC)" ]; then \
		echo "Error: SRC parameter is required. Use 'make gainers-strategy SRC=yahoo' or 'make gainers-strategy SRC=wsj'"; \
		exit 1; \
	fi
	@echo "Fetching gainers using strategy pattern from $(SRC)..."
	. env/bin/activate && PYTHONPATH=$(PWD) python get_gainer_strategy.py $(SRC)
	@echo "Gainers fetched from $(SRC) using strategy pattern."
