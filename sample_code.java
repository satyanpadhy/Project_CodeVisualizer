public class Calculator {
    /**
     * Recursive factorial calculation
     * Metadata:
     * name: factorial
     * dependencies: [factorial]
     */
    public int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    /**
     * Performs addition
     * Metadata:
     * name: add
     * dependencies: [validate]
     */
    public int add(int a, int b) {
        if (validate(a) && validate(b)) {
            return a + b;
        }
        return 0;
    }

    /**
     * Validates input
     * Metadata:
     * name: validate
     * dependencies: []
     */
    private boolean validate(int n) {
        return n >= 0;
    }
}