"""Tests for the code parser functionality."""
import pytest
from typing import Dict, List
import os
from codebase_analyzer.parser import CodeParser

def test_python_function_extraction(sample_python_file: str, expected_metadata: Dict[str, List[str]]):
    """Test that function dependencies are correctly extracted from Python code."""
    parser = CodeParser()
    metadata = parser.extract_metadata(sample_python_file)
    assert metadata == expected_metadata, "Extracted metadata does not match expected dependencies"

def test_empty_file_handling(temp_workspace: str):
    """Test parser behavior with empty files."""
    empty_file = os.path.join(temp_workspace, "empty.py")
    with open(empty_file, "w", encoding="utf-8") as f:
        f.write("")
    
    parser = CodeParser()
    metadata = parser.extract_metadata(empty_file)
    assert metadata == {}, "Empty file should result in empty metadata"

def test_no_dependencies(temp_workspace: str):
    """Test parsing functions with no dependencies."""
    file_path = os.path.join(temp_workspace, "no_deps.py")
    content = '''
def standalone_function():
    """A function with no dependencies."""
    return 42
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    parser = CodeParser()
    metadata = parser.extract_metadata(file_path)
    assert metadata == {"standalone_function": []}, "Function with no dependencies not handled correctly"

def test_nested_functions(temp_workspace: str):
    """Test handling of nested function definitions."""
    file_path = os.path.join(temp_workspace, "nested.py")
    content = '''
def outer_function():
    """
    Metadata:
    dependencies: [helper_function]
    """
    def inner_function():
        return helper_function()
    return inner_function()

def helper_function():
    """
    Metadata:
    dependencies: []
    """
    return 42
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    parser = CodeParser()
    metadata = parser.extract_metadata(file_path)
    expected = {
        "outer_function": ["helper_function"],
        "helper_function": []
    }
    assert metadata == expected, "Nested function handling incorrect"

def test_invalid_file_handling():
    """Test parser behavior with invalid file paths."""
    parser = CodeParser()
    with pytest.raises(FileNotFoundError):
        parser.extract_metadata("nonexistent_file.py")

def test_syntax_error_handling(temp_workspace: str):
    """Test parser behavior with invalid Python syntax."""
    file_path = os.path.join(temp_workspace, "invalid.py")
    content = '''
def invalid_function()
    """Missing colon in function definition"""
    return 42
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    parser = CodeParser()
    with pytest.raises(SyntaxError):
        parser.extract_metadata(file_path)

def test_circular_dependencies(temp_workspace: str):
    """Test handling of circular dependencies."""
    file_path = os.path.join(temp_workspace, "circular.py")
    content = '''
def function_a():
    """
    Metadata:
    dependencies: [function_b]
    """
    return function_b()

def function_b():
    """
    Metadata:
    dependencies: [function_a]
    """
    return function_a()
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    parser = CodeParser()
    metadata = parser.extract_metadata(file_path)
    expected = {
        "function_a": ["function_b"],
        "function_b": ["function_a"]
    }
    assert metadata == expected, "Circular dependencies not handled correctly"