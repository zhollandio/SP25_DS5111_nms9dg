.PHONY: update lint test lint-test gainers gainers-strategy ygainers.csv clean

# create/update virtual environment and install dependencies
update:
	@echo "Setting up virtual environment and installing dependencies..."
	@test -d env || python3 -m venv env
	./env/bin/pip install --upgrade pip
	./env/bin/pip install -r requirements.txt
	@echo "Virtual environment setup complete."

# run pylint on Python source files
lint:
	@echo "Running pylint..."
	- ./env/bin/pylint bin/*.py || true
	@echo "Linting complete."

# run tests using pytest
test:
	@echo "Running linter first..."
	make lint
	@echo "Running tests..."
	PYTHONPATH=$(PWD) ./env/bin/pytest -vv tests/
	@echo "Testing complete."

# lint + test
lint-test: test

# run get_gainer.py with specified source
# nice use of the if/fi block for providing feedback
gainers:
	@if [ -z "$(SRC)" ]; then \
                echo "Error: SRC parameter is required. Use 'make gainers SRC=yahoo'"; \
                exit 1; \
	fi
	@echo "Fetching gainers from $(SRC)..."
	PYTHONPATH=$(PWD) TIME_OF_DAY=$(TIME_OF_DAY) ./env/bin/python get_gainer.py $(SRC)
	@echo "Gainers fetched from $(SRC)."

# run get_gainer_strategy.py with specified source
gainers-strategy:
	@if [ -z "$(SRC)" ]; then \
		echo "Error: SRC parameter is required. Use 'make gainers-strategy SRC=wsj'"; \
		exit 1; \
	fi
	@echo "Fetching gainers using strategy pattern from $(SRC)..."
	PYTHONPATH=$(PWD) ./env/bin/python get_gainer_strategy.py $(SRC)
	@echo "Gainers fetched from $(SRC) using strategy pattern."

# test headless Chrome and dump DOM to CSV
ygainers.csv:
	@echo "Testing headless Chrome on example.com..."
	google-chrome --headless --disable-gpu --dump-dom https://example.com > sample_data/ygainers.csv
	@echo "Output saved to sample_data/ygainers.csv"

# clean the virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf env
	@echo "Virtual environment removed."
