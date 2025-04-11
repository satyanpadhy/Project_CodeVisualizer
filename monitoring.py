import time
import psutil
import os
from datetime import datetime
from typing import Dict, Any
import json
from functools import wraps
from dataclasses import dataclass, asdict
import threading
import logging

@dataclass
class PerformanceMetrics:
    execution_time: float
    memory_usage: float
    cpu_usage: float
    file_count: int
    total_functions: int
    cache_hits: int
    cache_misses: int
    errors_count: int

class MetricsCollector:
    def __init__(self, config):
        self.config = config
        self.metrics_dir = os.path.join(config.output_directory, 'metrics')
        os.makedirs(self.metrics_dir, exist_ok=True)
        self._metrics = {}
        self._lock = threading.Lock()
        self.logger = logging.getLogger('metrics')

    def track_execution_time(self, func_name: str):
        """Decorator to track function execution time."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self.record_metric(f"{func_name}_execution_time", execution_time)
                    return result
                except Exception as e:
                    self.record_metric(f"{func_name}_errors", 1)
                    raise
            return wrapper
        return decorator

    def record_metric(self, name: str, value: Any):
        """Record a metric with thread safety."""
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = []
            self._metrics[name].append((datetime.now().isoformat(), value))

    def get_system_metrics(self) -> Dict[str, float]:
        """Get current system metrics."""
        process = psutil.Process()
        return {
            'memory_usage': process.memory_info().rss / 1024 / 1024,  # MB
            'cpu_usage': process.cpu_percent(),
            'system_cpu': psutil.cpu_percent(),
            'system_memory': psutil.virtual_memory().percent
        }

    def export_metrics(self):
        """Export collected metrics to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metrics_file = os.path.join(self.metrics_dir, f'metrics_{timestamp}.json')
        
        system_metrics = self.get_system_metrics()
        
        with open(metrics_file, 'w') as f:
            json.dump({
                'system_metrics': system_metrics,
                'application_metrics': self._metrics
            }, f, indent=2)
        
        self.logger.info(f"Metrics exported to {metrics_file}")

    def generate_performance_report(self) -> PerformanceMetrics:
        """Generate a comprehensive performance report."""
        metrics = PerformanceMetrics(
            execution_time=sum(v[1] for v in self._metrics.get('total_execution_time', [])),
            memory_usage=self.get_system_metrics()['memory_usage'],
            cpu_usage=self.get_system_metrics()['cpu_usage'],
            file_count=len(self._metrics.get('files_processed', [])),
            total_functions=sum(v[1] for v in self._metrics.get('functions_found', [])),
            cache_hits=sum(v[1] for v in self._metrics.get('cache_hits', [])),
            cache_misses=sum(v[1] for v in self._metrics.get('cache_misses', [])),
            errors_count=sum(v[1] for v in self._metrics.get('total_errors', []))
        )
        
        report_file = os.path.join(
            self.metrics_dir,
            f'performance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        with open(report_file, 'w') as f:
            json.dump(asdict(metrics), f, indent=2)
        
        return metrics

    def monitor_resources(self, interval: int = 60):
        """Start monitoring system resources periodically."""
        def _monitor():
            while True:
                metrics = self.get_system_metrics()
                for name, value in metrics.items():
                    self.record_metric(name, value)
                time.sleep(interval)

        thread = threading.Thread(target=_monitor, daemon=True)
        thread.start()
        return thread