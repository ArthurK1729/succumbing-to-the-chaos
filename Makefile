.PHONY: init

init:
	pip install -r requirements.txt

init-dev: init
	pip install -r requirements-dev.txt

clean:
	find . -name "*.log" -type f -delete
