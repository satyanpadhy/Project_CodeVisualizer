"""Integration tests for the complete codebase analyzer workflow."""
import os
import pytest
import tempfile
from codebase_analyzer.parser import CodeParser
from codebase_analyzer.visualizer import DependencyVisualizer
from codebase_analyzer.cache_manager import CacheManager

@pytest.fixture
def sample_codebase():
    """Create a temporary codebase for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample Python files
        files = {
            "main.py": """
def main():
    result = process_data()
    visualize_results(result)
    return result
""",
            "processor.py": """
def process_data():
    data = fetch_data()
    return transform_data(data)

def fetch_data():
    return [1, 2, 3, 4, 5]

def transform_data(data):
    return [x * 2 for x in data]
""",
            "visualizer.py": """
def visualize_results(data):
    plot_data(data)
    save_plot()

def plot_data(data):
    # Plotting logic here
    pass

def save_plot():
    # Saving logic here
    pass
"""
        }
        
        for filename, content in files.items():
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        
        yield temp_dir

def test_complete_workflow(sample_codebase, test_config):
    """Test the complete workflow from parsing to visualization."""
    # Initialize components
    parser = CodeParser()
    cache_manager = CacheManager(test_config)
    visualizer = DependencyVisualizer(test_config)
    
    # Parse all Python files
    metadata = {}
    for file in os.listdir(sample_codebase):
        if file.endswith('.py'):
            filepath = os.path.join(sample_codebase, file)
            file_metadata = parser.extract_metadata(filepath)
            metadata.update(file_metadata)
    
    # Verify parsed metadata
    assert 'main' in metadata, "Main function not found"
    assert 'process_data' in metadata, "Process data function not found"
    assert 'visualize_results' in metadata, "Visualize results function not found"
    
    # Check dependencies
    assert 'process_data' in metadata['main'], "Main should depend on process_data"
    assert 'visualize_results' in metadata['main'], "Main should depend on visualize_results"
    assert 'fetch_data' in metadata['process_data'], "process_data should depend on fetch_data"
    assert 'transform_data' in metadata['process_data'], "process_data should depend on transform_data"
    assert 'plot_data' in metadata['visualize_results'], "visualize_results should depend on plot_data"
    assert 'save_plot' in metadata['visualize_results'], "visualize_results should depend on save_plot"
    
    # Test caching
    cache_manager.save_metadata(metadata)
    cached_metadata = cache_manager.load_metadata()
    assert metadata == cached_metadata, "Cached metadata should match original"
    
    # Test visualization
    output_base = os.path.join(test_config.viz_directory, "integration_test")
    visualizer.visualize_dependencies(metadata, "integration_test")
    
    # Verify visualization outputs
    assert os.path.exists(f"{output_base}.png"), "Static visualization not created"
    assert os.path.exists(f"{output_base}.html"), "Interactive visualization not created"
    assert os.path.exists(f"{output_base}_metrics.json"), "Metrics file not created"

def test_workflow_with_changes(sample_codebase, test_config):
    """Test the workflow when codebase changes occur."""
    parser = CodeParser()
    cache_manager = CacheManager(test_config)
    
    # Initial parse
    initial_metadata = {}
    for file in os.listdir(sample_codebase):
        if file.endswith('.py'):
            filepath = os.path.join(sample_codebase, file)
            file_metadata = parser.extract_metadata(filepath)
            initial_metadata.update(file_metadata)
    
    # Cache initial state
    cache_manager.save_metadata(initial_metadata)
    
    # Modify a file
    processor_path = os.path.join(sample_codebase, "processor.py")
    with open(processor_path, "a", encoding="utf-8") as f:
        f.write("""
def new_function():
    return transform_data(fetch_data())
""")
    
    # Parse again
    updated_metadata = {}
    for file in os.listdir(sample_codebase):
        if file.endswith('.py'):
            filepath = os.path.join(sample_codebase, file)
            file_metadata = parser.extract_metadata(filepath)
            updated_metadata.update(file_metadata)
    
    # Verify changes
    assert 'new_function' in updated_metadata, "New function not detected"
    assert 'transform_data' in updated_metadata['new_function'], "New function dependencies not detected"
    assert 'fetch_data' in updated_metadata['new_function'], "New function dependencies not detected"
    
    # Verify cache update
    cache_manager.save_metadata(updated_metadata)
    cached_metadata = cache_manager.load_metadata()
    assert cached_metadata == updated_metadata, "Cache not updated correctly"

def test_workflow_error_handling(sample_codebase, test_config):
    """Test workflow error handling with invalid code."""
    parser = CodeParser()
    
    # Create file with syntax error
    error_file = os.path.join(sample_codebase, "error.py")
    with open(error_file, "w", encoding="utf-8") as f:
        f.write("""
def invalid_function()  # Missing colon
    return None
""")
    
    # Verify error handling
    with pytest.raises(SyntaxError):
        parser.extract_metadata(error_file)
    
    # Create file with circular dependencies
    circular_file = os.path.join(sample_codebase, "circular.py")
    with open(circular_file, "w", encoding="utf-8") as f:
        f.write("""
def function_a():
    return function_b()

def function_b():
    return function_a()
""")
    
    # Verify circular dependency handling
    metadata = parser.extract_metadata(circular_file)
    assert 'function_a' in metadata
    assert 'function_b' in metadata
    assert 'function_b' in metadata['function_a']
    assert 'function_a' in metadata['function_b']