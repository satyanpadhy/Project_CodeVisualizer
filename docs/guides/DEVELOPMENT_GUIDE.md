# Development Guide

## Setting Up Development Environment

### Prerequisites
1. Python 3.8+
2. Graphviz installation
3. LLVM for C/C++ support
4. Git for version control

### Development Setup Steps

1. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Unix/MacOS
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Install Development Tools**
   ```bash
   pip install black pylint mypy pytest pytest-cov
   ```

## Development Workflow

### 1. Code Organization

```
project_root/
├── docs/                 # Documentation
├── src/                 # Source code
├── tests/              # Test files
├── examples/           # Example code
└── scripts/           # Development scripts
```

### 2. Testing Workflow

1. **Running Tests**
   ```bash
   pytest tests/
   pytest tests/ --cov=src/  # With coverage
   ```

2. **Test Categories**
   - Unit tests: `tests/unit/`
   - Integration tests: `tests/integration/`
   - Visual regression tests: `tests/visual/`

3. **Writing Tests**
   ```python
   def test_function_analysis():
       metadata = analyze_file("test_sample.py")
       assert "main_function" in metadata
       assert len(metadata["main_function"]) == 2  # Two dependencies
   ```

### 3. Code Quality

1. **Code Formatting**
   ```bash
   black src/ tests/
   ```

2. **Static Type Checking**
   ```bash
   mypy src/
   ```

3. **Linting**
   ```bash
   pylint src/
   ```

### 4. Adding New Features

#### Adding a New Parser

1. Create parser class:
   ```python
   class NewLanguageParser(BaseParser):
       def parse_file(self, file_path: str) -> Dict[str, List[str]]:
           # Implementation
           pass
   ```

2. Add unit tests:
   ```python
   def test_new_language_parser():
       parser = NewLanguageParser()
       result = parser.parse_file("example.ext")
       assert result is not None
   ```

3. Update configuration:
   ```python
   SUPPORTED_LANGUAGES = {
       "new_ext": NewLanguageParser
   }
   ```

#### Adding Visualization Features

1. Add visualization method:
   ```python
   def create_custom_visualization(self, metadata: Dict[str, List[str]]):
       # Implementation
       pass
   ```

2. Add configuration options:
   ```yaml
   visualization:
     custom_feature:
       enabled: true
       options:
         color_scheme: "dark"
   ```

### 5. Performance Optimization

1. **Profiling Code**
   ```python
   from cProfile import Profile
   profiler = Profile()
   profiler.enable()
   # Code to profile
   profiler.disable()
   profiler.print_stats()
   ```

2. **Memory Profiling**
   ```python
   from memory_profiler import profile
   
   @profile
   def memory_intensive_function():
       # Implementation
       pass
   ```

### 6. Debugging Tips

1. **Using Debug Logging**
   ```python
   import logging
   logging.debug(f"Processing file: {file_path}")
   logging.debug(f"Metadata: {metadata}")
   ```

2. **Visual Debugging**
   - Use `debug_graph()` for intermediate visualizations
   - Export partial results for inspection

### 7. Release Process

1. **Version Update**
   - Update version in `__init__.py`
   - Update CHANGELOG.md
   - Tag release in git

2. **Documentation Update**
   - Update API documentation
   - Add release notes
   - Update examples if needed

3. **Release Testing**
   ```bash
   pytest tests/ --runslow  # Run all tests including slow ones
   ```

### 8. Troubleshooting Development Issues

#### Common Issues

1. **Parser Errors**
   - Check file encoding
   - Verify syntax compatibility
   - Enable debug logging

2. **Visualization Issues**
   - Verify Graphviz installation
   - Check file permissions
   - Validate metadata format

3. **Performance Issues**
   - Profile the code
   - Check memory usage
   - Review cache settings

### 9. Best Practices

1. **Code Style**
   - Follow PEP 8
   - Use type hints
   - Write descriptive docstrings

2. **Testing**
   - Write tests first (TDD)
   - Use meaningful test names
   - Cover edge cases

3. **Documentation**
   - Document public APIs
   - Include examples
   - Keep README updated

4. **Version Control**
   - Write clear commit messages
   - Use feature branches
   - Review before merging

### 10. Contributing

1. **Pull Request Process**
   - Create feature branch
   - Write/update tests
   - Update documentation
   - Submit PR

2. **Code Review**
   - Address review comments
   - Update PR as needed
   - Keep discussions focused

3. **Documentation**
   - Update relevant docs
   - Add example code
   - Update CHANGELOG