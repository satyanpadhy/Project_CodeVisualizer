# Codebase Analysis and Visualization Tool

A powerful Python-based utility for analyzing codebases, extracting function dependencies, and generating insightful visualizations. The tool supports multiple programming languages and provides both static and interactive visualizations of function dependencies.

## Features

- **Multi-Language Support**
  - Python
  - Java
  - C/C++
  - Easily extensible to other languages

- **Dependency Analysis**
  - Function dependency extraction
  - Recursive call detection
  - Cross-file dependency mapping
  - Metadata-based analysis

- **Visualization**
  - Static graph generation (PNG format)
  - Interactive HTML visualizations
  - Color-coded function relationships
  - Grouped function clusters
  - Intuitive dependency arrows
  - Detailed tooltips and legends

- **Performance Features**
  - Parallel file processing
  - Caching system for large codebases
  - Memory-efficient analysis
  - Progress tracking

- **Monitoring & Metrics**
  - Performance metrics collection
  - Resource usage monitoring
  - Analysis statistics
  - Export capabilities

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Unix/MacOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install additional requirements:
   - LLVM (for C/C++ support)
   - Graphviz (for visualization generation)

## Usage

### Basic Usage

```bash
python main.py analyze <path_to_file_or_directory>
```

### Command Line Interface

The tool provides several commands:

1. Analyze codebase:
   ```bash
   python main.py analyze path/to/codebase --format png
   ```

2. Cache management:
   ```bash
   python main.py cache clear  # Clear cache
   python main.py cache stats  # View cache statistics
   ```

3. Generate metrics:
   ```bash
   python main.py metrics report  # Generate performance report
   python main.py metrics export  # Export raw metrics
   ```

### Configuration

The tool can be configured through `config.yaml`:

```yaml
# Output settings
output_directory: "output"
graph_dpi: 300
graph_format: "png"

# Processing settings
parallel_processing: true
max_workers: 4
max_file_size_mb: 10

# Cache settings
cache_enabled: true
cache_directory: ".cache"
```

## Function Metadata Format

Add metadata to your functions using docstrings:

```python
def example_function():
    """
    Metadata:
    name: example_function
    dependencies: [other_function, helper_function]
    """
    pass
```

## Output Structure

The tool generates several types of output:

- `/output/visualizations/`: Contains generated graphs
  - Static PNG visualizations
  - Interactive HTML visualizations
- `/output/metrics/`: Performance and analysis metrics
- `/output/logs/`: Detailed execution logs

## Visualization Guide

### Static Visualizations

The static graphs use the following color coding:
- Red: Recursive functions
- Green: Leaf functions (no dependencies)
- Orange: Functions with dependencies
- Blue: Gradient based on complexity/connections

### Interactive Visualizations

The HTML visualizations provide:
- Zoomable interface
- Draggable nodes
- Hover tooltips with detailed information
- Click-to-focus functionality
- Dynamic layout adjustments

## Error Handling

The tool provides comprehensive error handling:
- Syntax error detection
- Missing dependency warnings
- File access issues
- Resource limitation alerts

## Performance Considerations

- Use parallel processing for large codebases
- Enable caching for repeated analyses
- Monitor resource usage through metrics
- Use appropriate file size limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Requirements

- Python 3.8+
- Graphviz
- LLVM (for C/C++ support)
- Required Python packages in `requirements.txt`

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. Missing Graphviz:
   ```bash
   # Windows (using Chocolatey)
   choco install graphviz
   ```

2. LLVM Not Found:
   - Download and install LLVM from official website
   - Add to system PATH

3. Cache Issues:
   ```bash
   python main.py cache clear
   ```

### Support

For issues and feature requests, please:
1. Check the documentation
2. Review existing issues
3. Submit a detailed bug report if needed

## Acknowledgments

- Graphviz for visualization
- LLVM project for C/C++ support
- Ollama for code analysis