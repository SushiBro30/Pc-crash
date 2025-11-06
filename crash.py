import multiprocessing
import numpy as np
import math
import random
import time

# === ADJUSTABLE STRESS PARAMETERS ===
# Modify these values to control the stress level
# Higher values = more stress, lower values = less stress

STRATEGY = {
    'matrix_size': 2000,          # Matrix multiplication size (O(n³) impact)
    'primality_min': 10**20,      # Lower bound for primality testing
    'primality_max': 10**25,      # Upper bound for primality testing
    'factorial_limit': 10000,     # Iterations for factorial calculation
    'sample_count': 100000,       # Number of random samples per loop
    'cores': None,                # None = use all cores, or set a specific number
    'sleep_time': 0.1,            # Delay between iterations (lower = more stress)
}

def cpu_intensive_worker():
    """Performs CPU-heavy operations based on global STRATEGY parameters"""
    while True:
        # Task 1: Large matrix multiplication
        matrix_size = STRATEGY['matrix_size']
        a = np.random.rand(matrix_size, matrix_size)
        b = np.random.rand(matrix_size, matrix_size)
        c = np.matmul(a, b)  # GPU acceleration may reduce CPU load
        
        # Task 2: Primality test
        primality_min = STRATEGY['primality_min']
        primality_max = STRATEGY['primality_max']
        num = random.randint(primality_min, primality_max)
        limit = int(math.isqrt(num)) + 1
        for i in range(2, limit):
            if num % i == 0:
                break
        
        # Task 3: Factorial calculation
        factorial_limit = STRATEGY['factorial_limit']
        fact = 1
        for i in range(1, factorial_limit):
            fact *= i
            if fact > 1e100:  # Prevent overflow
                fact = 1
        
        # Task 4: Statistical analysis
        sample_count = STRATEGY['sample_count']
        samples = [random.gauss(0, 1) for _ in range(sample_count)]
        avg = sum(samples) / len(samples)
        
        
        # Sleep to control loop frequency
        time.sleep(STRATEGY['sleep_time'])

if __name__ == '__main__':
    # Set core usage
    num_cores = STRATEGY['cores'] if STRATEGY['cores'] is not None else multiprocessing.cpu_count()
    
    processes = []
    print(f"Starting {num_cores} core stress test with config:")
    print(f"Matrix: {STRATEGY['matrix_size']}x{STRATEGY['matrix_size']}")
    print(f"Primality range: {STRATEGY['primality_min']}-{STRATEGY['primality_max']}")
    print(f"Factorial limit: {STRATEGY['factorial_limit']}")
    print(f"Samples: {STRATEGY['sample_count']}")
    print(f"Loop delay: {STRATEGY['sleep_time']}s")
    
    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_intensive_worker)
        processes.append(p)
        p.start()
    
    try:
        while True:
            time.sleep(1)  # Keep main process alive
    except KeyboardInterrupt:
        print("\nStopping crash...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        print("Program completed. Your PC didn't crash.")
