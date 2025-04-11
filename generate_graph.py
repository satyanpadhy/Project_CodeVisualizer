import ast
import networkx as nx
import matplotlib.pyplot as plt

def extract_function_metadata(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read())
    
    metadata = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if docstring and "Metadata:" in docstring:
                lines = docstring.splitlines()
                name = None
                dependencies = []
                for line in lines:
                    if "name:" in line:
                        name = line.split("name:")[1].strip()
                    elif "dependencies:" in line:
                        dependencies = eval(line.split("dependencies:")[1].strip())
                if name:
                    metadata[name] = dependencies
    return metadata

def build_dependency_graph(metadata):
    graph = nx.DiGraph()
    for function, dependencies in metadata.items():
        graph.add_node(function)
        for dependency in dependencies:
            graph.add_edge(dependency, function)
    return graph

def visualize_graph(graph, output_path):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=10, font_weight="bold")
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    filepath = "c:\\Users\\teladmin\\Documents\\Proj_como\\sample_code.py"
    output_path = "c:\\Users\\teladmin\\Documents\\Proj_como\\function_dependencies.png"
    
    metadata = extract_function_metadata(filepath)
    graph = build_dependency_graph(metadata)
    visualize_graph(graph, output_path)
    print(f"Dependency graph saved as {output_path}")
