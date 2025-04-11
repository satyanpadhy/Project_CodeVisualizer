import os
import sys
import pytest

if __name__ == "__main__":
    # Add project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Run the specific test file
    test_file = os.path.join(project_root, "tests", "unit", "test_visualizer.py")
    print(f"Running tests from: {test_file}")
    pytest.main(["-v", "--no-cov", "--capture=no", test_file])