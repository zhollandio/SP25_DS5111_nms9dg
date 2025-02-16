.PHONY: update ygainers.csv

# create/update virtual env  and install dependencies
update:
	@echo "Setting up virtual environment and installing dependencies..."
	python3 -m venv env
	./env/bin/pip install --upgrade pip
	./env/bin/pip install -r requirements.txt
	@echo "Virtual environment setup complete."

# test headless chrome -  dump example.com content into a CSV file.
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
	. env/bin/activate && pytest -vv tests/
	@echo "Testing complete."

# runs linter 1st --> tests
lint-test: test
