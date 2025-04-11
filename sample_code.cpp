/**
 * Calculator class for mathematical operations
 */
class Calculator {
private:
    /**
     * Validates input numbers
     * Metadata:
     * name: validateInput
     * dependencies: [logError]
     */
    bool validateInput(double x) {
        if (std::isnan(x)) {
            logError("Invalid number");
            return false;
        }
        return true;
    }

    /**
     * Logs errors
     * Metadata:
     * name: logError
     * dependencies: []
     */
    void logError(const std::string& msg) {
        std::cerr << "Error: " << msg << std::endl;
    }

public:
    /**
     * Performs recursive power calculation
     * Metadata:
     * name: power
     * dependencies: [power, validateInput]
     */
    double power(double x, int n) {
        if (!validateInput(x)) return 0;
        if (n == 0) return 1;
        if (n < 0) return 1.0 / power(x, -n);
        return x * power(x, n-1);
    }

    /**
     * Calculates square root using Newton's method
     * Metadata:
     * name: sqrt
     * dependencies: [validateInput]
     */
    double sqrt(double x) {
        if (!validateInput(x) || x < 0) return 0;
        double guess = x / 2;
        for(int i = 0; i < 10; i++) {
            guess = (guess + x/guess) / 2;
        }
        return guess;
    }
};