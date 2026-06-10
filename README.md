# XR Trading - Python Assessment

## Overview
This is a command-line Python application designed to process and aggregate daily sales data. It reads from three input CSV files (Team Map, Product Master, and Sales) and produces two summarized output CSV reports (Team Report and Product Report). 

Per the project constraints, this application is built entirely using Python's built-in standard libraries (`argparse`, `csv`) and does not rely on third-party packages like `pandas`.

## Prerequisites
* Python 3.x or higher
* No external libraries or virtual environments are required.

## Usage
The application is executed from the command line. It requires three input files to be specified and accepts optional filenames for the generated reports.

**Standard Run Command:**
```
python main.py -t TeamMap.csv -p ProductMaster.csv -s Sales.csv --team-report TeamReport.csv --product-report ProductReport.csv
```

### Command-Line Arguments
| Argument | Short | Required | Description |
| :--- | :--- | :--- | :--- |
| `--team` | `-t` | **Yes** | Path to the Team Map CSV file. |
| `--product` | `-p` | **Yes** | Path to the Product Master CSV file. |
| `--sales` | `-s` | **Yes** | Path to the Sales CSV file. |
| `--team-report` | | No | Name of the output Team Report CSV file. *(Defaults to `TeamReport.csv`)* |
| `--product-report` | | No | Name of the output Product Report CSV file. *(Defaults to `ProductReport.csv`)* |

## Architecture & Design Decisions

To ensure this application meets **production-ready** standards, it was designed with memory efficiency and scalability in mind:

1. **Streaming Data Processing:** Rather than loading the potentially massive `Sales.csv` file entirely into memory, the application utilizes a streaming accumulator pattern. It reads the sales data row-by-row, computes the gross revenue and discounts on the fly, updates the reference dictionaries, and immediately discards the row. This ensures the application maintains an O(1) memory footprint regarding the sales data, preventing memory overflows regardless of file size.
2. **O(1) Dictionary Lookups:** The smaller reference files (Teams and Products) are loaded into dictionaries. This guarantees quick constant-time lookups while iterating through the sales.
3. **Defensive Programming:** The code includes safety checks to gracefully handle bad data (e.g., verifying that a `team_id` or `product_id` found in the sales logs actually exists in the master reference dictionaries before attempting calculations).
4. **Argparse Implementation:** Built-in `argparse` is used to handle command-line interfaces robustly, providing automatic type checking, help menus, and fallback default values for optional report outputs.

## Outputs
1. **Team Report:** Total gross revenue per team. Sorted in descending order by gross revenue.
2. **Product Report:** Gross revenue, total units sold, and total discount costs per product. Sorted in descending order by gross revenue. Gross revenue calculations reflect the pre-discount totals.