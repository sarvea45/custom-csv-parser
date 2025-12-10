
-----

# Custom CSV Parser from Scratch in Python

## 🎯 Project Overview

This project implements a custom streaming CSV reader (`CustomCsvReader`) and a custom CSV writer (`CustomCsvWriter`) in pure Python. The objective is to demonstrate a low-level understanding of data parsing and serialization, handling complex CSV edge cases such as **quoted fields**, **escaped quotes (`""`)**, and **embedded newline characters**.

The implementation is benchmarked against Python's built-in `csv` module to quantitatively measure and analyze the performance trade-offs inherent in building a parser from scratch.

## ⚙️ Setup and Running

### Prerequisites

This project requires a standard Python 3.x installation.

  * The `requirements.txt` file confirms no external dependencies are needed.

### File Structure

The core components are organized as follows:

```
custom-csv-parser/
├── custom_csv.py             # Custom Reader/Writer implementation
├── benchmark.py              # Performance testing script
├── test_data_generator.py    # Script to create the large test file
├── README.md                 # Project documentation and analysis

```

### Running the Benchmark

To generate the test data and run the performance comparison, execute the main benchmark script:

```bash
python benchmark.py
```

*This command first generates a 10,000-row file (`test_data.csv`) and then runs the read/write tests for both the standard and custom implementations.*

## 📝 Usage Examples

### 1\. CustomCsvReader (Streaming Data Ingestion)

The reader functions as an iterator, yielding one row at a time without loading the entire file into memory, which is essential for large datasets.

```python
from custom_csv import CustomCsvReader
import os

FILE_PATH = 'test_data.csv' # Use your generated file

if os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        reader = CustomCsvReader(f)
        
        # Read the header
        header = next(reader)
        print(f"Header: {header}")
        
        # Iterate over the first few data rows
        print("\nFirst 3 Data Rows:")
        for i, row in enumerate(reader):
            print(row)
            if i >= 2: break 
```

### 2\. CustomCsvWriter (Data Serialization)

The writer takes a list of lists (rows) and serializes it into a correctly formatted CSV file, automatically handling quoting and escaping.

```python
from custom_csv import CustomCsvWriter

data_to_write = [
    ["ID", "Description", "Comments"],
    [1, "Standard field", "Note: No special chars."],
    [2, "Field with, comma", 'Note: Must be "quoted".'],
    [3, "Field with\nnewline", 'Quote with "inner quote"'],
]

with open('output_sample.csv', 'w', encoding='utf-8') as f:
    writer = CustomCsvWriter(f)
    writer.writerows(data_to_write)
    
# output_sample.csv content:
# ID,Description,Comments
# 1,Standard field,"Note: No special chars."
# 2,"Field with, comma","Note: Must be ""quoted""."
# 3,"Field with\nnewline","Quote with ""inner quote"""
```

## 📊 Performance Benchmark and Analysis

The benchmark was executed using Python's `timeit` module on a synthetically generated file containing **10,000 rows** of complex data (including commas, quotes, and newlines).

| Operation | Standard `csv` Library (Avg. Time) | Custom Implementation (Avg. Time) | Performance Delta |
| :--- | :--- | :--- | :--- |
| **Reading** | **0.0147 seconds** | **0.6146 seconds** | **41.8 $\times$ slower** |
| **Writing** | **0.0175 seconds** | **0.0322 seconds** | **1.84 $\times$ slower** |

### Analysis of Performance Differences

The observed performance difference is substantial and confirms the expected trade-off between custom Python solutions and built-in, optimized libraries:

1.  **Reading Performance (Massive Gap):**

      * The **`CustomCsvReader`** is significantly slower because it relies on pure Python logic and requires frequent, small I/O calls (`file.read(1)`) combined with Python's overhead for state management. This character-by-character processing incurs high overhead from the Python interpreter loop.
      * The **Standard CSV Reader** is implemented entirely in optimized **C code**. It avoids Python overhead by reading large blocks of data at once (buffering) and processing the file using highly efficient low-level routines.

2.  **Writing Performance (Smaller Gap):**

      * The gap is much smaller for writing because the primary work involves string concatenation and file system output, which are less prone to state-machine complexity. However, the **Standard Writer** still holds an advantage (approx. 1.84x faster) because its internal routines for checking field content, escaping quotes, and generating the final string are C-optimized, whereas the custom solution relies on Python's built-in string methods (e.g., `.replace()`, `.join()`).

The custom implementation successfully proves correctness and robustness in handling all edge cases, but sacrifices speed for the sake of clear, low-level control.
