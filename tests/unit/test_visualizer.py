"""Tests for the graph visualization functionality."""
import os
import sys
import pytest
import tempfile
import shutil
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use absolute import path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
from visualizer import DependencyVisualizer

@pytest.fixture(scope="module")
def test_output_dir():
    """Create and cleanup a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp(prefix='test_visualizer_')
    logger.info(f"Created temporary test directory: {temp_dir}")
    yield temp_dir
    try:
        shutil.rmtree(temp_dir)
        logger.info(f"Cleaned up temporary test directory: {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to cleanup temporary directory: {e}")

@pytest.fixture
def sample_metadata() -> Dict[str, List[str]]:
    """Create sample metadata for testing."""
    return {
        "main": ["helper1"],
        "helper1": ["utility"],
        "utility": []
    }

@pytest.fixture
def test_config(test_output_dir):
    """Create test configuration."""
    return type('Config', (), {
        'viz_directory': test_output_dir,
        'graph_format': 'png'
    })

def test_visualization_creation(sample_metadata, test_config, caplog):
    """Test that visualizations are created correctly."""
    caplog.set_level(logging.DEBUG)
    logger.info("Starting visualization creation test")
    
    try:
        visualizer = DependencyVisualizer(test_config)
        output_base = os.path.join(test_config.viz_directory, "test_graph")
        
        logger.info("Generating visualizations...")
        visualizer.visualize_dependencies(sample_metadata, "test_graph")
        
        # Check if files were created
        files_to_check = [
            (f"{output_base}.{test_config.graph_format}", "Static graph"),
            (f"{output_base}.html", "Interactive graph"),
            (f"{output_base}_flow.gif", "Animated flow"),
            (f"{output_base}_metrics.json", "Metrics file")
        ]
        
        for file_path, file_desc in files_to_check:
            logger.info(f"Checking for {file_desc} at {file_path}")
            assert os.path.exists(file_path), f"{file_desc} not created"
            assert os.path.getsize(file_path) > 0, f"{file_desc} is empty"
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}", exc_info=True)
        raise

def test_empty_metadata_handling(test_config):
    """Test handling of empty metadata."""
    logger.debug("Starting empty metadata handling test")
    visualizer = DependencyVisualizer(test_config)
    visualizer.visualize_dependencies({}, "empty_test")
    
    logger.debug("Checking that no files were created for empty metadata")
    # No files should be created for empty metadata
    output_base = os.path.join(test_config.viz_directory, "empty_test")
    assert not os.path.exists(f"{output_base}.{test_config.graph_format}")
    assert not os.path.exists(f"{output_base}.html")
    assert not os.path.exists(f"{output_base}_flow.gif")
    assert not os.path.exists(f"{output_base}_metrics.json")

def test_metrics_generation(sample_metadata, test_config):
    """Test that metrics are generated correctly."""
    logger.debug("Starting metrics generation test")
    visualizer = DependencyVisualizer(test_config)
    
    logger.debug("Generating visualizations to populate metrics")
    visualizer.visualize_dependencies(sample_metadata, "metrics_test")
    
    logger.debug("Checking generated metrics")
    metrics = visualizer.metrics_cache
    
    # Check main function metrics
    assert metrics["main"]["out_degree"] == 1, "Main should have 1 dependency"
    assert metrics["main"]["in_degree"] == 0, "Main should not be dependent on anything"
    assert not metrics["main"]["is_recursive"], "Main should not be recursive"
    
    # Check utility function metrics
    assert metrics["utility"]["out_degree"] == 0, "Utility should have no dependencies"
    assert metrics["utility"]["in_degree"] == 1, "Utility should be used by 1 function"
    assert not metrics["utility"]["is_recursive"], "Utility should not be recursive"

def test_recursive_function(test_config):
    """Test visualization of recursive functions."""
    logger.debug("Starting recursive function test")
    metadata = {
        "recursive_func": ["recursive_func", "helper"],
        "helper": []
    }
    
    visualizer = DependencyVisualizer(test_config)
    visualizer.visualize_dependencies(metadata, "recursive_test")
    
    logger.debug("Checking recursive function metrics")
    metrics = visualizer.metrics_cache
    assert metrics["recursive_func"]["is_recursive"], "Function should be marked as recursive"
    assert not metrics["helper"]["is_recursive"], "Helper should not be recursive"

def test_error_handling(test_config):
    """Test error handling for invalid metadata."""
    logger.debug("Starting error handling test")
    visualizer = DependencyVisualizer(test_config)
    
    # Test with invalid function reference
    metadata = {
        "main": ["nonexistent_function"]
    }
    
    logger.debug("Testing visualization with invalid function reference")
    # Should not raise an exception
    visualizer.visualize_dependencies(metadata, "error_test")
    
    logger.debug("Checking that graph was created despite invalid references")
    output_base = os.path.join(test_config.viz_directory, "error_test")
    assert os.path.exists(f"{output_base}.{test_config.graph_format}"), "Graph should be created even with invalid references"