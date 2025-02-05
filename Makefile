.PHONY: update ygainers.csv

# create/update virtua env  and install dependencies
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

