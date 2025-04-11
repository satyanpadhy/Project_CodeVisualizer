# Contributing to Codebase Analysis and Visualization Tool

Thank you for your interest in contributing to our project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository
2. Set up your development environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Unix/MacOS
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Install development dependencies
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Maintain test coverage above 80%

## Adding New Features

### Supporting a New Programming Language

1. Create a new parser module in `parsers/`
2. Implement the required interfaces:
   - `parse_file()`
   - `extract_metadata()`
   - `get_dependencies()`
3. Update the language detection in `config.py`
4. Add appropriate tests
5. Update documentation

### Enhancing Visualizations

1. Maintain backward compatibility
2. Follow the existing color scheme
3. Document new visual elements
4. Consider accessibility guidelines

## Testing

1. Run the test suite:
   ```bash
   pytest tests/
   ```

2. Add tests for new features:
   - Unit tests for individual components
   - Integration tests for language parsers
   - Visual regression tests for graphs

## Pull Request Process

1. Create a feature branch from `main`
2. Write clear commit messages
3. Update documentation
4. Add tests
5. Submit PR with:
   - Description of changes
   - Screenshots for visual changes
   - Test results
   - Documentation updates

## Code Review Process

- All PRs require at least one review
- Address review comments promptly
- Keep discussions focused and professional
- Update PR based on feedback

## Development Best Practices

### Error Handling

- Use appropriate exception types
- Provide meaningful error messages
- Log errors with proper context
- Handle resource cleanup

### Performance

- Profile code changes
- Consider memory usage
- Test with large codebases
- Use caching appropriately

### Documentation

- Update README.md for user-facing changes
- Document configuration options
- Provide examples
- Update API documentation

## Release Process

1. Version bump following semver
2. Update CHANGELOG.md
3. Create release notes
4. Tag release
5. Update documentation

## Community

- Be respectful and inclusive
- Help others contribute
- Share knowledge
- Report issues constructively

## Questions?

- Open a discussion
- Check existing issues
- Read the documentation
- Contact maintainers