# Usage Examples

## Basic Analysis Examples

### 1. Analyzing a Single Python File

```python
# sample_function.py
def calculate_metrics():
    """
    Metadata:
    dependencies: [validate_input, process_data]
    """
    data = validate_input()
    return process_data(data)

def validate_input():
    """
    Metadata:
    dependencies: []
    """
    return True

def process_data(data):
    """
    Metadata:
    dependencies: [validate_input]
    """
    if validate_input():
        return data
```

Command:
```bash
python main.py analyze sample_function.py
```

This will generate:
- Static PNG visualization
- Interactive HTML graph
- Performance metrics

### 2. Analyzing Multiple Files

Project structure:
```
src/
  ├── core.py
  ├── utils.py
  └── helpers.py
```

Command:
```bash
python main.py analyze src/ --parallel
```

### 3. Cache Management

Clear old cache entries:
```bash
python main.py cache clear --older-than 7
```

View cache statistics:
```bash
python main.py cache stats
```

## Advanced Usage Examples

### 1. Custom Configuration

```yaml
# config.yaml
output_directory: "custom_output"
graph_dpi: 400
graph_format: "png"
parallel_processing: true
max_workers: 8
cache_enabled: true
```

### 2. Integration with Build Systems

#### Maven Project
```xml
<!-- pom.xml -->
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <configuration>
                <executable>python</executable>
                <arguments>
                    <argument>main.py</argument>
                    <argument>analyze</argument>
                    <argument>${project.basedir}/src/main/java</argument>
                </arguments>
            </configuration>
        </plugin>
    </plugins>
</build>
```

#### Gradle Project
```groovy
// build.gradle
task analyzeDependencies(type: Exec) {
    commandLine 'python', 'main.py', 'analyze', 'src/main/java'
}
```

### 3. CI/CD Integration

#### GitHub Actions
```yaml
name: Dependency Analysis
on: [push]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run analysis
        run: python main.py analyze src/
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: dependency-graphs
          path: output/visualizations/
```

### 4. Language-Specific Examples

#### Java Example
```java
// UserService.java
public class UserService {
    /**
     * Metadata:
     * dependencies: [validateUser, saveUser]
     */
    public void createUser(User user) {
        if (validateUser(user)) {
            saveUser(user);
        }
    }
}
```

#### C++ Example
```cpp
// processor.cpp
/**
 * Metadata:
 * dependencies: [validate_input, transform_data]
 */
void process_data() {
    if (validate_input()) {
        transform_data();
    }
}
```

### 5. Visualization Customization

Custom color scheme:
```yaml
# config.yaml
visualization:
  colors:
    recursive: "#FF5733"
    leaf: "#33FF57"
    regular: "#3357FF"
    edge: "#454545"
```

### 6. Performance Optimization

For large codebases:
```yaml
# config.yaml
parallel_processing: true
max_workers: 12
max_file_size_mb: 20
cache_enabled: true
cache_ttl_hours: 48
```

### 7. Metrics Export

Generate performance report:
```bash
python main.py metrics report --output metrics.json
```

Example metrics output:
```json
{
    "execution_time": 15.23,
    "file_count": 128,
    "total_functions": 456,
    "cache_hits": 89,
    "memory_usage_mb": 245.6
}
```

### 8. Error Handling Examples

```python
try:
    visualizer.create_graph(metadata)
except VisualizationError as e:
    logger.error(f"Failed to create visualization: {e}")
    # Fallback to simple text output
    export_text_report(metadata)
```

### 9. Batch Processing

Process multiple projects:
```bash
python main.py analyze --batch-file projects.txt
```

projects.txt:
```
/path/to/project1
/path/to/project2
/path/to/project3
```

### 10. Output Customization

Generate multiple formats:
```bash
python main.py analyze src/ --formats png,svg,html
```

These examples demonstrate common usage patterns and integration scenarios for the codebase analysis tool.