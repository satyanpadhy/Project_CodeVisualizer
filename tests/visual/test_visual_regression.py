import pytest
import os
import tempfile
import hashlib
from PIL import Image, ImageChops
from typing import Dict, List, Tuple

def get_image_hash(image_path: str) -> str:
    """Calculate a hash of an image file for comparison."""
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def compare_images(img1_path: str, img2_path: str) -> Tuple[bool, float]:
    """
    Compare two images and return if they are similar and the difference percentage.
    Returns (is_similar, difference_percentage)
    """
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    
    # Convert images to same size and mode
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    img2 = img2.resize(img1.size)
    
    # Calculate difference
    diff = ImageChops.difference(img1, img2)
    # Convert difference to grayscale for comparison
    diff_gray = diff.convert('L')
    diff_pixels = sum(x > 0 for x in diff_gray.getdata())
    total_pixels = img1.size[0] * img1.size[1]
    difference_percentage = (diff_pixels / total_pixels) * 100
    
    # Consider images similar if difference is less than 1%
    return difference_percentage < 1.0, difference_percentage

@pytest.fixture
def sample_metadata() -> Dict[str, List[str]]:
    """Create sample metadata for visualization testing."""
    return {
        "main": ["helper1", "helper2"],
        "helper1": ["utility"],
        "helper2": ["utility"],
        "utility": []
    }

@pytest.fixture
def reference_graph(sample_metadata, tmp_path) -> str:
    """Generate a reference graph for comparison."""
    from visualizer import DependencyVisualizer
    from config import load_config
    
    config = load_config()
    config.viz_directory = str(tmp_path)
    
    visualizer = DependencyVisualizer(config)
    visualizer.visualize_dependencies(sample_metadata, "reference")
    
    return os.path.join(config.viz_directory, f"reference.{config.graph_format}")

def test_visual_consistency(sample_metadata, reference_graph, tmp_path):
    """Test that graph generation remains visually consistent."""
    from visualizer import DependencyVisualizer
    from config import load_config
    
    # Generate new graph with same metadata
    config = load_config()
    config.viz_directory = str(tmp_path)
    
    visualizer = DependencyVisualizer(config)
    visualizer.visualize_dependencies(sample_metadata, "test")
    
    test_graph = os.path.join(config.viz_directory, f"test.{config.graph_format}")
    
    # Compare graphs
    is_similar, difference = compare_images(reference_graph, test_graph)
    
    assert is_similar, f"Visual regression detected! Difference: {difference:.2f}%"
    assert difference < 1.0, f"Graph difference ({difference:.2f}%) exceeds threshold"

def test_layout_stability():
    """Test that node positions remain stable for the same input."""
    from visualizer import DependencyVisualizer
    from config import load_config
    
    metadata = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": []
    }
    
    # Generate two graphs with the same input
    temp_dir = tempfile.mkdtemp()
    config = load_config()
    config.viz_directory = temp_dir
    
    visualizer = DependencyVisualizer(config)
    
    # Generate first graph
    visualizer.visualize_dependencies(metadata, "stability1")
    graph1_path = os.path.join(temp_dir, f"stability1.{config.graph_format}")
    
    # Generate second graph
    visualizer.visualize_dependencies(metadata, "stability2")
    graph2_path = os.path.join(temp_dir, f"stability2.{config.graph_format}")
    
    # Compare hashes - they should be identical for stable layout
    hash1 = get_image_hash(graph1_path)
    hash2 = get_image_hash(graph2_path)
    
    assert hash1 == hash2, "Layout is not stable between identical graph generations"