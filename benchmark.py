import timeit
import csv
import os
import sys
import test_data_generator
from custom_csv import CustomCsvReader, CustomCsvWriter

# --- Global Constants ---
FILE_NAME = test_data_generator.FILE_NAME
OUTPUT_FILE = "output_bench.csv"
N_REPEATS = 5  # Number of times to run the test and average the result
NUMBER = 1     # Run the function once per repeat

# --- Setup: Load Data ---
def load_data_for_write(filename):
    """Loads all data from the test file using the standard library."""
    data = []
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
    return data

# --- Benchmarking Functions ---

def benchmark_std_read():
    """Times the standard csv.reader."""
    with open(FILE_NAME, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        list(reader) 

def benchmark_custom_read():
    """Times the custom CustomCsvReader."""
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        reader = CustomCsvReader(f)
        list(reader)

def benchmark_std_write(data_to_write):
    """Times the standard csv.writer."""
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data_to_write)

def benchmark_custom_write(data_to_write):
    """Times the custom CustomCsvWriter."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        writer = CustomCsvWriter(f)
        writer.writerows(data_to_write)

# --- Execution Logic ---

def run_benchmarks(data_to_write):
    print(f"\n--- Running Benchmarks ({len(data_to_write)} rows, Repeats: {N_REPEATS}) ---\n")

    # Read Benchmarks
    read_std_times = timeit.repeat(benchmark_std_read, repeat=N_REPEATS, number=NUMBER)
    read_custom_times = timeit.repeat(benchmark_custom_read, repeat=N_REPEATS, number=NUMBER)
    
    avg_std_read = sum(read_std_times) / N_REPEATS
    avg_custom_read = sum(read_custom_times) / N_REPEATS

    print(f"Time to Read:")
    print(f"  Standard CSV Reader: {avg_std_read:.4f} seconds")
    print(f"  Custom CSV Reader:   {avg_custom_read:.4f} seconds")
    print("-" * 30)

    # Write Benchmarks (using lambda to pass the data argument)
    write_std_times = timeit.repeat(lambda: benchmark_std_write(data_to_write), repeat=N_REPEATS, number=NUMBER)
    write_custom_times = timeit.repeat(lambda: benchmark_custom_write(data_to_write), repeat=N_REPEATS, number=NUMBER)

    avg_std_write = sum(write_std_times) / N_REPEATS
    avg_custom_write = sum(write_custom_times) / N_REPEATS

    print(f"Time to Write:")
    print(f"  Standard CSV Writer: {avg_std_write:.4f} seconds")
    print(f"  Custom CSV Writer:   {avg_custom_write:.4f} seconds")
    print("-" * 30)
    
    # Clean up benchmark output file
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

if __name__ == "__main__":
    try:
        # 1. Ensure test data exists (GENERATION)
        test_data_generator.generate_test_data() 
        
        # 2. LOAD data from the now-existing file
        data_for_write = load_data_for_write(FILE_NAME)
        
        # 3. Run the comparison tests, passing the data
        run_benchmarks(data_for_write)
        
    except Exception as e:
        # Catch any remaining errors and print a useful message
        print(f"\nAn error occurred during execution: {e}", file=sys.stderr)
        print("Please verify your 'custom_csv.py' logic and ensure 'test_data_generator.py' is working.")