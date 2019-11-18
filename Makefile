clean:
	.venv/bin/pre-commit uninstall
	rm -rf .venv/
coverage:
	.venv/bin/py.test -s --verbose --cov-report term-missing --cov-report xml --cov=aionotion tests
init:
	python3 -m venv .venv
	.venv/bin/pip3 install poetry
	.venv/bin/poetry lock
	.venv/bin/poetry install
	.venv/bin/pre-commit install
lint:
	.venv/bin/black --check --fast aionotion
	.venv/bin/flake8 aionotion
	.venv/bin/pydocstyle aionotion
	.venv/bin/pylint aionotion
publish:
	.venv/bin/poetry build
	.venv/bin/poetry publish
	rm -rf dist/ build/ .egg *.egg-info/
test:
	.venv/bin/py.test
typing:
	.venv/bin/mypy --ignore-missing-imports aionotion
