.PHONY: install shortcut today clean secrets

install:
	@pre-commit install || echo "hint:\n\nuv tool install pre-commit"

shortcut:
	@echo "alias aoc='cd "'"'$(shell pwd)'"'" && source ./shell/aliases'"

today:
	@bash ./shell/doday

secrets:
	cp ./-secrets.example.json ./--secrets.json

clean:
	ruff check --extend-select I --fix # lint + isort
	ruff format                        # fmt
