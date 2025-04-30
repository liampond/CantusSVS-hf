.PHONY: help setup clean run

# Default command: show help
help:
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Set up virtual environment (use 'make setup reset=1' to force rebuild)"
	@echo "  make clean        - Remove the virtual environment"
	@echo "  make run          - Launch the Streamlit app"
	@echo ""

# Set up the environment
setup:
ifeq ($(reset),1)
	rm -rf venv
endif
	bash scripts/setup_env.sh

# Remove the virtual environment
clean:
	rm -rf venv

# Run the Streamlit app
run:
	source venv/bin/activate && streamlit run webapp/app.py

