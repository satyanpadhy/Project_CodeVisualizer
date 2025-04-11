def sample_function_one():
    """
    Metadata:
    name: sample_function_one
    dependencies: []
    """
    print("This is sample function one.")

def sample_function_two():
    """
    Metadata:
    name: sample_function_two
    dependencies: [sample_function_one]
    """
    print("This is sample function two.")

def sample_function_three():
    """
    Metadata:
    name: sample_function_three
    dependencies: [sample_function_two]
    """
    print("This is sample function three.")

def factorial(n):
    """
    Recursive function to calculate factorial
    Metadata:
    name: factorial
    dependencies: [factorial]
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """
    Recursive function for fibonacci sequence
    Metadata:
    name: fibonacci
    dependencies: [fibonacci, calculate_sequence]
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def calculate_sequence(length):
    """
    Calculates various sequences
    Metadata:
    name: calculate_sequence
    dependencies: [fibonacci, factorial, format_output]
    """
    fib_seq = [fibonacci(i) for i in range(length)]
    fact_seq = [factorial(i) for i in range(length)]
    return format_output(fib_seq, fact_seq)

def format_output(seq1, seq2):
    """
    Formats sequences for display
    Metadata:
    name: format_output
    dependencies: [validate_input]
    """
    if validate_input(seq1) and validate_input(seq2):
        return {
            'fibonacci': seq1,
            'factorial': seq2
        }
    return None

def validate_input(sequence):
    """
    Validates input sequences
    Metadata:
    name: validate_input
    dependencies: [log_error]
    """
    if not sequence:
        log_error("Empty sequence")
        return False
    return True

def log_error(message):
    """
    Error logging utility
    Metadata:
    name: log_error
    dependencies: [get_timestamp]
    """
    print(f"[{get_timestamp()}] Error: {message}")

def get_timestamp():
    """
    Gets current timestamp
    Metadata:
    name: get_timestamp
    dependencies: []
    """
    from datetime import datetime
    return datetime.now().isoformat()

def process_data(data):
    """
    Main data processing function
    Metadata:
    name: process_data
    dependencies: [validate_input, transform_data, analyze_results]
    """
    if validate_input(data):
        transformed = transform_data(data)
        return analyze_results(transformed)
    return None

def transform_data(data):
    """
    Transforms input data
    Metadata:
    name: transform_data
    dependencies: [validate_input, log_error]
    """
    try:
        return [x * 2 for x in data]
    except Exception as e:
        log_error(str(e))
        return None

def analyze_results(results):
    """
    Analyzes transformed results
    Metadata:
    name: analyze_results
    dependencies: [calculate_statistics, generate_report]
    """
    stats = calculate_statistics(results)
    return generate_report(stats)

def calculate_statistics(data):
    """
    Calculates statistical measures
    Metadata:
    name: calculate_statistics
    dependencies: [validate_input]
    """
    if not validate_input(data):
        return None
    return {
        'sum': sum(data),
        'len': len(data),
        'avg': sum(data) / len(data)
    }

def generate_report(stats):
    """
    Generates final report
    Metadata:
    name: generate_report
    dependencies: [format_output, get_timestamp]
    """
    if stats:
        return format_output(
            [stats['sum'], stats['avg']],
            [stats['len'], get_timestamp()]
        )
    return None 