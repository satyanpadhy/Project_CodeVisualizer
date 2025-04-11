import argparse
from typing import List, Optional
import os
import sys

def get_file_path() -> str:
    """Prompt for and validate file path."""
    print("\n=== Function Dependency Analyzer ===")
    print("Please enter the path to the file you want to analyze.")
    print("Available sample files:")
    print("- sample_code.py  (Python example)")
    print("- sample_code.java  (Java example)")
    print("- sample_code.cpp  (C++ example)")
    print("- sample_code.c  (C example)")
    print("\nOr enter the path to your own source file.")
    
    while True:
        try:
            file_path = input("\nFile path: ").strip()
            if file_path:
                if os.path.exists(file_path):
                    return file_path
                else:
                    print(f"Error: File '{file_path}' not found. Please try again.")
            else:
                print("Error: File path cannot be empty. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze code dependencies and generate visualizations')
    parser.add_argument('file_path', nargs='?', help='Path to the file to analyze')
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    parser.add_argument('--interactive', '-i', action='store_true', default=True,
                       help='Enable interactive function selection (enabled by default)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Analyze all functions (overrides interactive mode)')
    
    args = parser.parse_args()
    
    # If file_path is not provided, prompt for it
    if not args.file_path:
        args.file_path = get_file_path()
    
    return args

def print_menu(functions: List[str]) -> None:
    """Print the function selection menu."""
    print("\n" + "="*50)
    print("Function Dependency Analyzer - Interactive Selection")
    print("="*50 + "\n")
    
    print("Available functions:")
    for i, func in enumerate(functions, 1):
        print(f"{i:2d}. {func}")
    
    print("\nOptions:")
    print("- Enter numbers (e.g., 1 2 3) to select specific functions")
    print("- Type 'a' to select all functions")
    print("- Type 'q' to quit")

def get_user_selection(functions: List[str]) -> Optional[List[str]]:
    """Get user's function selection."""
    while True:
        try:
            choice = input("\nYour selection: ").strip().lower()
            
            if choice == 'q':
                print("\nOperation cancelled.")
                return None
            elif choice == 'a':
                print("\nAll functions selected.")
                return functions
                
            try:
                indices = [int(x) - 1 for x in choice.split()]
                selected = [functions[i] for i in indices if 0 <= i < len(functions)]
                
                if not selected:
                    print("No valid functions selected. Please try again.")
                    continue
                    
                return selected
                
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid function numbers.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None

def select_functions(functions: List[str]) -> Optional[List[str]]:
    """Present an interactive selection of functions to the user."""
    if not functions:
        print("\nNo functions found in the file.")
        return None

    # Sort functions for consistent display
    functions = sorted(functions)
    
    # Print initial menu
    print_menu(functions)
    
    # Get user selection
    selected = get_user_selection(functions)
    if not selected:
        return None
        
    # Show selection summary and confirm
    print("\nSelected functions:")
    for func in selected:
        print(f"• {func}")
        
    while True:
        confirm = input("\nProceed with these functions? (y/n): ").strip().lower()
        if confirm == 'y':
            return selected
        elif confirm == 'n':
            print("\nSelection cancelled. Please try again.")
            print_menu(functions)
            return get_user_selection(functions)
        else:
            print("Please enter 'y' for yes or 'n' for no.")