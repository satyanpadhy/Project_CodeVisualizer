# Entry point for the Codebase Analysis and Visualization Tool

import os
import sys
from config import load_config
from logger import setup_logger
from error_handler import setup_error_handlers
from visualizer import DependencyVisualizer
from cli import parse_args, select_functions
import ast
from typing import Dict, List, Any

def print_flush(*args, **kwargs):
    """Print with immediate flush."""
    print(*args, **kwargs, flush=True)

def extract_function_metadata(file_path: str) -> Dict[str, List[str]]:
    """Extract function metadata from Python file."""
    metadata = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring and "Metadata:" in docstring:
                    lines = [line.strip() for line in docstring.splitlines()]
                    name = node.name
                    dependencies = []
                    
                    for line in lines:
                        if "dependencies:" in line.lower():
                            try:
                                deps_str = line.split("dependencies:")[1].strip()
                                if deps_str == "[]":
                                    dependencies = []
                                else:
                                    deps_list = deps_str.strip("[]").split(",")
                                    dependencies = [d.strip().strip("'\"") for d in deps_list if d.strip()]
                            except Exception as e:
                                print_flush(f"Warning: Could not parse dependencies for {node.name}: {e}")
                    
                    metadata[name] = dependencies
    except Exception as e:
        print_flush(f"Error extracting metadata from {file_path}: {e}")
    return metadata

def analyze_file(file_path: str) -> Dict[str, List[str]]:
    """Analyze a single file and extract function metadata."""
    print_flush(f"\nAnalyzing {file_path}...")
    return extract_function_metadata(file_path)

def main():
    try:
        # Parse command line arguments and force interactive mode unless --all is specified
        args = parse_args()
        if not args.all:
            args.interactive = True
        
        # Load configuration and setup components
        config = load_config(args.config)
        logger = setup_logger(config)
        setup_error_handlers(logger)
        
        # Analyze the file
        metadata = analyze_file(args.file_path)
        
        if metadata:
            print_flush(f"\nFound {len(metadata)} functions in the file")
            
            # Always show interactive selection unless --all is specified
            if not args.all:
                selected_functions = select_functions(list(metadata.keys()))
                if not selected_functions:
                    print_flush("\nNo functions selected for analysis")
                    return 1
                    
                # Filter metadata to include only selected functions and their dependencies
                filtered_metadata = {}
                print_flush("\nProcessing selected functions and their dependencies...")
                for func in selected_functions:
                    filtered_metadata[func] = metadata[func]
                    # Include functions that are dependencies
                    for dep in metadata[func]:
                        if dep in metadata:
                            filtered_metadata[dep] = metadata[dep]
                metadata = filtered_metadata
                
                print_flush(f"Analyzing {len(metadata)} functions (including dependencies)")
            
            # Generate visualizations
            base_name = os.path.splitext(os.path.basename(args.file_path))[0]
            visualizer = DependencyVisualizer(config)
            
            try:
                print_flush("\nGenerating visualizations...")
                visualizer.visualize_dependencies(metadata, base_name)
                print_flush(f"\nAnalysis complete! Check the visualizations in: {config.viz_directory}")
                return 0
            except Exception as viz_error:
                print_flush(f"\nError during visualization: {str(viz_error)}")
                return 1
        else:
            print_flush("\nNo functions with metadata found in the file")
            return 1
            
    except KeyboardInterrupt:
        print_flush("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print_flush(f"\nFatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())