# Contributing

## Development Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Code Quality

All Python code must pass:

```bash
ruff check .
ruff format --check .
mypy .
```

## Project Structure

- `app/` — core viewer (vanilla JS, no framework). Keep generic.
- `examples/` — region-specific implementations. Keep data separate from code.
- `scripts/` — generic Python utilities. No hardcoded region paths.
- `docs/` — general documentation.

## Pull Request Guidelines

1. One feature per PR.
2. If modifying `app/`, verify with both `config.sample.js` and a region config.
3. If adding region-specific data, put it in `examples/<region>/`.
4. No hardcoded API keys or secrets.

## Acceptance Testing

Before submitting:

- [ ] `app/` opens with sample config (no JS errors)
- [ ] At least 2 lensa can be active simultaneously
- [ ] Custom GeoJSON URL loads successfully
- [ ] Invalid GeoJSON URL shows user-friendly error
- [ ] Share URL preserves map state + custom layers
- [ ] Removing custom layer cleans up map + URL
- [ ] `ruff check .` passes
- [ ] `mypy .` passes
