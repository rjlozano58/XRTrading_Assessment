import argparse
import csv
import json

def team_report(team_dict,output_filename):

    # Headers for ouput TeamReport.csv file
    csv_headers = ["Team","GrossRevenue"]

    # Sort teams by 'gross_revenue' in decreasing order
    sorted_teams = list(team_dict.values())
    sorted_teams.sort(key=lambda x: x["gross_revenue"], reverse=True)

    try:

        with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_headers)

            writer.writeheader()

            # Iterate through all products, output necessary product details to report csv file
            for team in sorted_teams:
                row_to_write = {
                    "Team": team["name"],
                    "GrossRevenue": team["gross_revenue"]
                }
                writer.writerow(row_to_write)
                
    except Exception as e:
        print(f"An error occurred writing '{output_filename}': {e}")

def product_report(product_dict, output_filename):

    # Headers for ouput ProductReport.csv file
    csv_headers = ["Name","GrossRevenue","TotalUnits","DiscountCost"]

    # Sort products by 'gross_revenue' in decreasing order
    sorted_products = list(product_dict.values())
    sorted_products.sort(key=lambda x: x["gross_revenue"], reverse=True)

    try:
        with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_headers)

            writer.writeheader()

            # iterate through all products, output necessary product details to report csv file
            for product in sorted_products:
                row_to_write = {
                    "Name": product["name"],
                    "GrossRevenue": product["gross_revenue"],
                    "TotalUnits": product["total_units"],
                    "DiscountCost": product["discount_cost"]
                }
                writer.writerow(row_to_write)

    except Exception as e:
        print(f"An error occurred writing '{output_filename}': {e}")


def main():

    parser = argparse.ArgumentParser(description="This application will read from 3 input files and use the data within to produce 2 output files") 

    # Set up arguments
    parser.add_argument("-t", "--team", type=str, help="This should be a CSV of the team data", required=True)
    parser.add_argument("-p", "--product", type=str, help="This should be a CSV of the product master data", required=True)
    parser.add_argument("-s", "--sales", type=str, help="This should be a CSV of the sales data", required=True)
    parser.add_argument("--team-report", type=str, help="Name of team report output CSV file", required=False)
    parser.add_argument("--product-report", type=str, help="Name of product report output CSV file", required=False)

    args = parser.parse_args()

    # Save input files name inorder to traverse them
    input_files = [args.team, args.product, args.sales]

    # If output filenames are provided, use them. If no filenames provided, default output filenames are use.
    team_out = args.team_report if args.team_report else "TeamReport.csv"
    product_out = args.product_report if args.product_report else "ProductReport.csv"

    team_dict = {}
    product_master_dict = {}

    # Read each input file, process team data, product data, and sale data
    for filename in input_files:

        print(f"Processing file: {filename}")
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)

                if filename == args.team:    # Create a dictionary holding all team data, leaving room for team report calculations
                    next(reader)
                    for row in reader:
                        team_dict[row[0]] = {
                            "name" : row[1].strip(),
                            "gross_revenue" : 0.0
                            }

                elif filename == args.product:    # Create a dictionary holding all product data, leaving room for product report calculations
                    for row in reader:
                        product_master_dict[row[0]] = {
                            "name": row[1].strip(),
                            "price": row[2],
                            "lot_size": row[3],
                            "gross_revenue": 0.0,
                            "total_units": 0,
                            "discount_cost": 0.0
                            }
                elif filename == args.sales:
                    for row in reader:

                        # Extract sales details in order to calculate gross revenue of each team
                        product_id = row[1].strip()
                        team_id = row[2].strip()
                        quantity = int(row[3])
                        discount = float(row[4])

                        # Extract product details to calculate the gross revenue of each team
                        name = product_master_dict[product_id]["name"]
                        price_per_unit = float(product_master_dict[product_id]["price"])
                        lot_size = float(product_master_dict[product_id]["lot_size"])

                        gross_revenue_sale = price_per_unit * quantity * lot_size
                        discount_cost = gross_revenue_sale * (discount / 100) 

                        # Using sale and product details, append revenue from each sale to gross sale of each team
                        if team_id in team_dict:
                            team_dict[team_id]["gross_revenue"] += gross_revenue_sale

                            # Using sale and product details, append the revenue from this product's sale to it's gross revenue in products dictionary
                            product_master_dict[product_id]["gross_revenue"] += gross_revenue_sale
                            product_master_dict[product_id]["total_units"] += quantity * lot_size
                            product_master_dict[product_id]["discount_cost"] += discount_cost

        except FileNotFoundError:
            print(f"CRITICAL ERROR: The input file '{filename}' could not be found.")
            print("Please check your file paths and try again.")
            sys.exit(1) # Exits the script immediately with an error code

        except Exception as e:
            print(f"An unexpected error occurred while reading '{filename}': {e}")
            sys.exit(1)

    # Create team report and product report csv files
    team_report(team_dict,team_out)
    product_report(product_master_dict,product_out)


if __name__ == "__main__":
    main()