from pyvis.network import Network
import networkx as nx
from graphviz import Digraph
import os
from typing import Dict, List, Optional, Set
import json
import colorsys
import logging
import traceback
from debug_logger import debug
import imageio
import tempfile
import shutil
from PIL import Image
import numpy as np
from error_handler import VisualizationError, with_error_handling

logger = logging.getLogger(__name__)

class DependencyVisualizer:
    def __init__(self, config):
        self.config = config
        self.metrics_cache = {}
        # Enhanced color scheme using color theory
        self.colors = {
            'no_deps': '#4a90e2',      # Professional blue
            'has_deps': '#f5a623',     # Warm orange
            'recursive': '#d0021b',     # Attention-grabbing red
            'leaf': '#7ed321',         # Fresh green
            'background': '#ffffff',    # Clean white
            'edge': '#2d3436',         # Dark gray
            'text': '#2c3e50'          # Dark blue-gray
        }
        
    def _calculate_node_importance(self, func: str, metadata: Dict[str, List[str]]) -> float:
        """Calculate node importance based on connections."""
        incoming = len([f for f, deps in metadata.items() if func in deps])
        outgoing = len(metadata.get(func, []))
        return incoming + outgoing
    
    def _generate_gradient_color(self, importance: float, max_importance: float) -> str:
        """Generate a color gradient based on node importance."""
        if max_importance == 0:
            return self.colors['no_deps']
            
        ratio = importance / max_importance
        hue = 0.6 - (ratio * 0.4)  # Shift from blue to red
        saturation = 0.6 + (ratio * 0.4)
        value = 0.9
        
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
    
    @with_error_handling((Exception,), max_retries=2)
    def create_interactive_graph(self, metadata: Dict[str, List[str]], output_path: str):
        """Create an interactive HTML visualization using pyvis."""
        try:
            # Ensure output path is absolute
            output_path = os.path.abspath(output_path)
            html_path = f"{output_path}.html"
            
            # Initialize network
            net = Network(height="900px", width="100%", bgcolor=self.colors['background'])
            net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100)
            
            # Calculate node importance
            importance_values = {func: self._calculate_node_importance(func, metadata) for func in metadata}
            max_importance = max(importance_values.values()) if importance_values else 1
            
            # Add nodes
            for func in metadata:
                importance = importance_values[func]
                size = 25 + (importance * 5)
                color = self._generate_gradient_color(importance, max_importance)
                
                net.add_node(
                    func,
                    label=func,
                    title=self._create_node_tooltip(func, metadata),
                    size=size,
                    color=color
                )
            
            # Add edges
            for func, deps in metadata.items():
                for dep in deps:
                    if dep in metadata:
                        net.add_edge(dep, func)
            
            # Save the network
            net.save_graph(html_path)
            logger.info(f"Interactive visualization saved to {html_path}")
            
        except Exception as e:
            logger.error(f"Error in interactive graph creation: {str(e)}", exc_info=True)
            raise VisualizationError(f"Failed to create interactive graph: {str(e)}")
    
    @with_error_handling((Exception,), max_retries=2)
    def create_static_graph(self, metadata: Dict[str, List[str]], output_path: str):
        """Create a static visualization using Graphviz."""
        if not metadata:
            logger.warning("No metadata to visualize")
            return None
            
        try:
            # Create graph
            dot = Digraph(comment='Function Dependencies')
            dot.attr(rankdir='LR', splines='ortho')
            
            # Add nodes
            for func in metadata:
                self._add_node_to_graph(dot, func, metadata)
            
            # Add edges
            for func, deps in metadata.items():
                for dep in deps:
                    if dep in metadata:
                        dot.edge(dep, func)
            
            # Set output path
            output_path = os.path.abspath(output_path)
            dot.render(output_path, format=self.config.graph_format, cleanup=True)
            logger.info(f"Static visualization saved to {output_path}.{self.config.graph_format}")
            return dot
            
        except Exception as e:
            logger.error(f"Error in static graph creation: {str(e)}", exc_info=True)
            raise VisualizationError(f"Failed to create static graph: {str(e)}")

    def _group_related_functions(self, metadata: Dict[str, List[str]]) -> List[Set[str]]:
        """Group related functions based on their dependencies."""
        groups: List[Set[str]] = []
        processed = set()

        def get_related_functions(func: str, related: Optional[Set[str]] = None) -> Set[str]:
            if related is None:
                related = set()
            related.add(func)
            
            # Add dependencies
            for dep in metadata.get(func, []):
                if dep not in related and dep in metadata:
                    get_related_functions(dep, related)
            
            # Add functions that depend on this one
            for f, deps in metadata.items():
                if func in deps and f not in related and f in metadata:
                    get_related_functions(f, related)
                    
            return related

        # Process all functions
        for func in metadata:
            if func not in processed:
                related = get_related_functions(func)
                groups.append(related)
                processed.update(related)

        return groups

    def _add_node_to_graph(self, graph, func: str, metadata: Dict[str, List[str]]):
        """Add a node to the graph with appropriate styling."""
        try:
            # Calculate metrics
            metrics = {
                'in_degree': len([f for f, d in metadata.items() if func in d]),
                'out_degree': len(metadata.get(func, [])),
                'is_recursive': func in metadata.get(func, [])
            }
            self.metrics_cache[func] = metrics
            
            # Set node attributes
            attrs = {
                'shape': 'box',
                'style': 'filled',
                'fontname': 'Arial'
            }
            
            if metrics['is_recursive']:
                attrs['fillcolor'] = self.colors['recursive']
                attrs['fontcolor'] = 'white'
            elif metrics['out_degree'] == 0:
                attrs['fillcolor'] = self.colors['leaf']
            else:
                attrs['fillcolor'] = self.colors['has_deps']
                
            graph.node(func, self._create_node_label(func, metadata), **attrs)
            
        except Exception as e:
            logger.error(f"Error adding node {func}: {str(e)}", exc_info=True)

    def _create_node_label(self, func: str, metadata: Dict[str, List[str]]) -> str:
        """Create a formatted node label."""
        return f"{func}\n({len(metadata[func])} deps)"

    def _create_node_tooltip(self, func: str, metadata: Dict[str, List[str]]) -> str:
        """Create a detailed node tooltip."""
        metrics = self.metrics_cache.get(func, {
            'in_degree': len([f for f, d in metadata.items() if func in d]),
            'out_degree': len(metadata.get(func, [])),
            'is_recursive': func in metadata.get(func, [])
        })
        
        return (
            f"Function: {func}\n"
            f"Dependencies: {metrics['out_degree']}\n"
            f"Used by: {metrics['in_degree']}\n"
            f"Type: {'Recursive' if metrics['is_recursive'] else 'Normal'}"
        )
    
    def export_metrics(self, output_path: str):
        """Export node metrics as JSON."""
        try:
            metrics_file = f"{output_path}_metrics.json"
            
            if not self.metrics_cache:
                logger.warning("No metrics to export")
                return
                
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.metrics_cache, f, indent=2)
            logger.info(f"Metrics exported to {metrics_file}")
            
        except Exception as e:
            logger.error(f"Error exporting metrics: {str(e)}", exc_info=True)

    def visualize_dependencies(self, metadata: Dict[str, List[str]], base_name: str):
        """Create static, interactive, and animated flow visualizations."""
        if not metadata:
            logger.warning("No metadata to visualize")
            return
            
        # Ensure we have absolute paths
        output_base = os.path.abspath(os.path.join(self.config.viz_directory, base_name))
        os.makedirs(os.path.dirname(output_base), exist_ok=True)
        
        logger.info(f"Creating visualizations in: {output_base}")
        
        try:
            # Create static visualization
            static_graph = self.create_static_graph(metadata, output_base)
            if not static_graph:
                logger.error("Failed to create static visualization")
            
            # Create interactive visualization
            self.create_interactive_graph(metadata, output_base)
            
            # Create animated flow visualization
            self.create_animated_flow(metadata, output_base)
            
            # Export metrics
            self.export_metrics(output_base)
            
        except Exception as e:
            logger.error(f"Error in visualization process: {str(e)}", exc_info=True)
            raise VisualizationError(f"Failed to create visualizations: {str(e)}")

    def create_animated_flow(self, metadata: Dict[str, List[str]], output_path: str):
        """Create an animated GIF showing the flow of function calls."""
        try:
            frames_dir = tempfile.mkdtemp()
            frames = []
            target_size = (800, 500)  # Fixed size for all frames
            
            # Create a base graph with all nodes but no edges
            dot = Digraph(comment='Function Flow Animation')
            dot.attr(rankdir='LR', splines='ortho')
            
            # Add all nodes first
            for func in metadata:
                self._add_node_to_graph(dot, func, metadata)
            
            # Generate frames by progressively adding edges
            processed_edges = set()
            frame_count = 0
            
            def add_frame(graph, frame_path):
                # Render the graph
                graph.render(frame_path, format='png', cleanup=True)
                
                # Open with PIL and resize to target size
                with Image.open(f"{frame_path}.png") as img:
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                    # Convert to RGB to ensure consistent format
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    # Convert to numpy array for imageio
                    frame_array = np.array(img)
                    frames.append(frame_array)
            
            # Add initial frame with just nodes
            base_frame = os.path.join(frames_dir, f"frame_{frame_count:03d}")
            add_frame(dot, base_frame)
            frame_count += 1
            
            # Create frames for each edge addition
            for func, deps in metadata.items():
                for dep in deps:
                    if dep in metadata and (dep, func) not in processed_edges:
                        # Create new graph with current edge highlighted
                        flow_dot = dot.copy()
                        
                        # Add all previously processed edges in normal style
                        for processed_edge in processed_edges:
                            flow_dot.edge(processed_edge[0], processed_edge[1], color='gray')
                        
                        # Add new edge with highlight
                        flow_dot.edge(dep, func, color='red', penwidth='2.0')
                        
                        # Save frame
                        frame_path = os.path.join(frames_dir, f"frame_{frame_count:03d}")
                        add_frame(flow_dot, frame_path)
                        
                        frame_count += 1
                        processed_edges.add((dep, func))
            
            # Generate final frame showing complete graph
            final_dot = dot.copy()
            for edge in processed_edges:
                final_dot.edge(edge[0], edge[1], color='gray')
            final_frame = os.path.join(frames_dir, f"frame_{frame_count:03d}")
            add_frame(final_dot, final_frame)
            
            # Save the animation
            output_path = f"{output_path}_flow.gif"
            imageio.mimsave(output_path, frames, duration=1.0)  # 1 second per frame
            logger.info(f"Animated flow visualization saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating animation: {str(e)}", exc_info=True)
            raise VisualizationError(f"Failed to create animation: {str(e)}")
        finally:
            # Cleanup temporary files
            try:
                shutil.rmtree(frames_dir)
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary directory {frames_dir}: {str(e)}")