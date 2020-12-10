requirements.txt: poetry.lock
	pip install poetry
	poetry export -f requirements.txt -o requirements.txt --dev
