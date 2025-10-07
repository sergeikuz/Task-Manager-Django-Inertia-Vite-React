build:
	./build.sh

render-start:
	gunicorn backend.wsgi

install-backend:
	uv sync

install-frontend:
	cd frontend && npm install && npm run build

# Convert static asset files
collectstatic:
	uv run python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
migrate:
	uv run python3 manage.py migrate

lint:
	uv run ruff check

lint-fix: 	
	uv run ruff check --fix

run:
	uv run python3 manage.py runserver

shell:
	uv run python3 manage.py shell_plus --ipython

test:
	uv run python3 manage.py test

test-pytest:
	uv run pytest

test-coverage:
	uv run pytest --cov=backend --cov-report=xml:coverage.xml

start-backend:
	uv run manage.py runserver

start-frontend:
	cd frontend && uv run npm run dev