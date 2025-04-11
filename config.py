import os
from dataclasses import dataclass
from typing import List, Optional
import yaml

@dataclass
class AnalyzerConfig:
    supported_languages: List[str]
    output_directory: str
    cache_enabled: bool
    cache_directory: str
    log_level: str
    max_file_size_mb: int
    parallel_processing: bool
    max_workers: int
    ollama_model: str
    graph_dpi: int
    graph_format: str
    excluded_directories: List[str]

    def __post_init__(self):
        # Ensure output directory is absolute path
        if not os.path.isabs(self.output_directory):
            self.output_directory = os.path.abspath(self.output_directory)
        
        # Create visualization subdirectory
        self.viz_directory = os.path.join(self.output_directory, 'visualizations')
        os.makedirs(self.viz_directory, exist_ok=True)

def load_config(config_path: str = "config.yaml") -> AnalyzerConfig:
    """Load configuration from YAML file with fallback to defaults."""
    defaults = {
        "supported_languages": ["python", "java", "c", "cpp"],
        "output_directory": "output",
        "cache_enabled": True,
        "cache_directory": ".cache",
        "log_level": "INFO",
        "max_file_size_mb": 10,
        "parallel_processing": True,
        "max_workers": os.cpu_count() or 4,
        "ollama_model": "codellama",
        "graph_dpi": 300,
        "graph_format": "png",
        "excluded_directories": [".git", "__pycache__", "venv", ".venv"]
    }

    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    defaults.update(user_config)
    except Exception as e:
        print(f"Warning: Could not load config file: {e}")

    return AnalyzerConfig(**defaults)