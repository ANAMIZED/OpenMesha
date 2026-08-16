.PHONY: run build up down verify test mcp cli

run:
	OM_LLM_MODE=mock PYTHONPATH=src python -c "from openmesha.main import run; run()"

mcp:
	PYTHONPATH=src python -m openmesha.mcp.server

cli:
	PYTHONPATH=src python -m openmesha.cli --help

build:
	docker compose build

up:
	docker compose up --build -d

down:
	docker compose down

verify:
	bash scripts/verify.sh

test:
	PYTHONPATH=src pytest -q
