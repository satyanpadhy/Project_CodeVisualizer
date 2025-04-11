"""Shared test fixtures and configuration."""
import os
import tempfile
import shutil
from typing import Dict, List, Generator
import pytest

@pytest.fixture
def temp_workspace() -> Generator[str, None, None]:
    """Create a temporary workspace for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_python_file(temp_workspace: str) -> str:
    """Create a sample Python file with known dependencies."""
    file_path = os.path.join(temp_workspace, "sample.py")
    content = '''
def main_function():
    """
    Metadata:
    dependencies: [helper_function, utility_function]
    """
    result = helper_function()
    return utility_function(result)

def helper_function():
    """
    Metadata:
    dependencies: [utility_function]
    """
    return utility_function(42)

def utility_function(value):
    """
    Metadata:
    dependencies: []
    """
    return value * 2
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

@pytest.fixture
def expected_metadata() -> Dict[str, List[str]]:
    """Return expected metadata for the sample Python file."""
    return {
        "main_function": ["helper_function", "utility_function"],
        "helper_function": ["utility_function"],
        "utility_function": []
    }

@pytest.fixture
def test_config():
    """Create a test configuration object."""
    class Config:
        def __init__(self):
            self.viz_directory = tempfile.mkdtemp()
            self.graph_format = "png"
            self.graph_dpi = 300
            self.log_level = "INFO"
            self.parallel_processing = True
            self.cache_enabled = True
            self.cache_dir = tempfile.mkdtemp()
            
        def cleanup(self):
            """Clean up temporary directories."""
            shutil.rmtree(self.viz_directory, ignore_errors=True)
            shutil.rmtree(self.cache_dir, ignore_errors=True)
            
    config = Config()
    yield config
    config.cleanup()