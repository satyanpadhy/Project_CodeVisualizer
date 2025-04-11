import concurrent.futures
from typing import List, Dict, Tuple, Any
import os
from logger import setup_logger

class ParallelAnalyzer:
    def __init__(self, config, cache_manager):
        self.config = config
        self.cache_manager = cache_manager
        self.logger = setup_logger(config)
        self.max_workers = config.max_workers

    def analyze_files_parallel(self, file_list: List[str], analyze_func) -> List[Tuple[str, Dict[str, Any]]]:
        """Analyze multiple files in parallel."""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all files for analysis
            future_to_file = {
                executor.submit(self._analyze_single_file, file_path, analyze_func): file_path
                for file_path in file_list
            }
            
            # Process completed analyses as they finish
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    metadata = future.result()
                    if metadata:
                        results.append((file_path, metadata))
                        self.logger.info(f"Successfully analyzed {file_path}")
                except Exception as e:
                    self.logger.error(f"Error analyzing {file_path}: {str(e)}")
        
        return results

    def _analyze_single_file(self, file_path: str, analyze_func) -> Dict[str, Any]:
        """Analyze a single file with caching."""
        try:
            # Check cache first
            cached_result = self.cache_manager.get_cached_metadata(file_path)
            if cached_result is not None:
                self.logger.debug(f"Cache hit for {file_path}")
                return cached_result

            # Analyze file
            result = analyze_func(file_path)
            
            # Cache the result
            if result:
                self.cache_manager.cache_metadata(file_path, result)
            
            return result
        except Exception as e:
            self.logger.error(f"Error in _analyze_single_file for {file_path}: {str(e)}")
            raise

    def get_file_batch(self, directory: str) -> List[str]:
        """Get a list of files to analyze, respecting size limits."""
        files_to_process = []
        max_size = self.config.max_file_size_mb * 1024 * 1024  # Convert to bytes
        
        for root, _, files in os.walk(directory):
            if any(excluded in root for excluded in self.config.excluded_directories):
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if os.path.getsize(file_path) <= max_size:
                        files_to_process.append(file_path)
                    else:
                        self.logger.warning(f"Skipping {file_path}: exceeds size limit")
                except OSError as e:
                    self.logger.error(f"Error checking {file_path}: {str(e)}")
        
        return files_to_process