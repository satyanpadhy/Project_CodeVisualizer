import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from cachetools import TTLCache

class CacheManager:
    def __init__(self, config):
        self.config = config
        self.cache_dir = config.cache_directory
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # In-memory cache for frequently accessed items
        self.memory_cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes TTL
    
    def _get_cache_key(self, file_path: str) -> str:
        """Generate a cache key based on file path and modification time."""
        mtime = os.path.getmtime(file_path)
        content = f"{file_path}:{mtime}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_cached_metadata(self, file_path: str) -> Optional[Dict]:
        """Retrieve metadata from cache if available and valid."""
        if not self.config.cache_enabled:
            return None
            
        cache_key = self._get_cache_key(file_path)
        
        # Try memory cache first
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]
        
        # Try file cache
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    self.memory_cache[cache_key] = cached_data
                    return cached_data
            except Exception:
                return None
        return None
    
    def cache_metadata(self, file_path: str, metadata: Dict) -> None:
        """Cache metadata for future use."""
        if not self.config.cache_enabled:
            return
            
        cache_key = self._get_cache_key(file_path)
        
        # Update memory cache
        self.memory_cache[cache_key] = metadata
        
        # Update file cache
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(metadata, f)
        except Exception:
            pass
    
    def clear_cache(self, older_than_days: Optional[int] = None) -> None:
        """Clear cached data."""
        if older_than_days is not None:
            cutoff = datetime.now() - timedelta(days=older_than_days)
            for cache_file in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, cache_file)
                if os.path.getctime(file_path) < cutoff.timestamp():
                    os.remove(file_path)
        else:
            for cache_file in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, cache_file))
        self.memory_cache.clear()