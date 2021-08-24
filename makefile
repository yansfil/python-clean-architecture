project := app

install:
	pip install -r requirements.txt

freeze:
	pip list --not-required --format=freeze > requirements.txt

test:
	PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 py.test --tb short -rxs \
    --cov-config .coveragerc --cov ./app tests

local:
	uvicorn app.entrypoints.main:app --port 8000 --reload
