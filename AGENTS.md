# Repository Guidelines

## Project Structure & Module Organization
This repository currently exposes a single CLI module `ascii_art.py` and a minimal `README`. Keep banner rendering logic inside `ascii_art.py` until it outgrows a single file, then promote reusable helpers into `ascii_art/` and load patterns from `resources/letters.json`. Place automated tests under `tests/` mirroring the module names, and store any future sample banners or fixtures under `tests/fixtures/`.

## Build, Test, and Development Commands
Use `python3 ascii_art.py` to run the generator interactively; the script only depends on the standard library, so no installation step is required. Create an isolated environment when adding dependencies: `python3 -m venv .venv && source .venv/bin/activate`. Run checks with `python3 -m pytest` once tests exist, and `python3 -m black ascii_art.py tests` to keep formatting consistent.

## Coding Style & Naming Conventions
Target Python 3.10+. Follow PEP 8: 4-space indentation, snake_case for functions, and ALL_CAPS for pattern constants (`LETTER_PATTERNS`, `LETTER_HEIGHT`). Add type hints for all new functions and prefer small, pure helpers so pattern generation stays testable. Run `black` before committing; pair it with `ruff` for linting if you introduce it.

## Testing Guidelines
Prefer `pytest` with simple function-scoped fixtures that supply sample words. Name test files `test_<module>.py` and test functions `test_<scenario>`. Cover edge cases such as unsupported characters, mixed case input, and spacing rules. Keep an eye on console formatting by asserting against multi-line strings; use `textwrap.dedent` to keep expectations readable.

## Commit & Pull Request Guidelines
Existing history uses short, imperative subjects (`Add ASCII art banner generator`); continue that format and keep bodies for context. Reference issue IDs in the first line when applicable, and note platform-specific behavior for contributors without Swedish locales. Pull requests should describe user impact, include before/after output snippets, list manual test commands, and note any follow-up TODOs or debt introduced.
