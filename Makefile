.PHONY: help install sync run test tests lint format check docs build-docs clean

help:  ## Показать справку по командам
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: sync  ## Установить зависимости
	@echo "Dependencies installed"

sync:  ## Синхронизировать зависимости через uv
	uv sync

run:  ## Запустить пример
	uv run main.py

test tests:  ## Запустить тесты
	uv run pytest -v

lint:  ## Запустить линтер (ruff)
	uv run ruff check . --fix

format:  ## Отформатировать код (black + isort)
	uv run black .
	uv run isort .

check: lint format  ## Проверить и исправить код
	@echo "Code check complete"

docs build-docs:  ## Собрать документацию Sphinx
	uv run sphinx-build -b html docs/source docs/build
	@echo "Docs built at docs/build/index.html"

clean:  ## Удалить артефакты сборки
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf docs/build/ 2>/dev/null || true
	@echo "Clean complete"
