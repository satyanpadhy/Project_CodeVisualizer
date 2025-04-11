/**
 * Recursive fibonacci implementation
 * Metadata:
 * name: fibonacci
 * dependencies: [fibonacci]
 */
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

/**
 * Data validation function
 * Metadata:
 * name: validate_data
 * dependencies: [log_error]
 */
int validate_data(int* data, int size) {
    if (!data || size <= 0) {
        log_error("Invalid input");
        return 0;
    }
    return 1;
}

/**
 * Error logging utility
 * Metadata:
 * name: log_error
 * dependencies: []
 */
void log_error(const char* message) {
    printf("Error: %s\n", message);
}