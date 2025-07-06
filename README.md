# Tower Game

A Python-based tower defense game.

## Description

Tower is an engaging tower defense game where players strategically place towers to defend against waves of enemies.

## Development Tools

This project uses modern Python development tools to ensure code quality and fast dependency management:

### UV (Ultra-fast Version)

UV is a fast Python package installer and resolver, written in Rust. It serves as a drop-in replacement for pip and can be used with requirements.txt or pyproject.toml.

Key benefits:
- Much faster than pip
- Compatible with all Python package formats
- Built-in dependency resolver
- Can generate lock files for reproducible builds

Usage:
```bash
# Install dependencies
uv sync

# Install a specific package
uv add <package_name>

# Remove a package
uv remove <package_name>

# Update all packages
uv update

# Generate a lock file
uv lock

# Run a Python script
uv run tower
```

### Ruff

Ruff is an extremely fast Python linter and code formatter, also written in Rust. It replaces multiple tools like flake8, black, isort, and more.

Key features:
- Code linting
- Code formatting
- Import sorting
- Much faster than traditional Python linters
- Highly configurable

Usage:
```bash 
# Run linter
uv tool run ruff check ./src

# Format code
uv tool run ruff format ./src
```

## Getting Started

1. Clone the repository
2. Install dependencies using UV:
   ```bash
   uv sync
   ```
3. Run the game:
   ```bash
   uv run tower
   ```

## Contributing

Before submitting changes:
1. Format your code using Ruff:
   ```bash
   uv tool run ruff format ./src
   ```
2. Run the linter:
   ```bash
   ruff tool run ruff check ./src
   ```
