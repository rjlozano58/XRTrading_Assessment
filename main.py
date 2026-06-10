import argparse
import csv
import json

def team_report(team_dict,output_filename):

    csv_headers = ["Team","GrossRevenue"]

    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)

        writer.writeheader()

        for team_id, team in team_dict.items():
            row_to_write = {
                "Team": team["name"],
                "GrossRevenue": team["gross_revenue"]
            }
            writer.writerow(row_to_write)

def product_report(product_dict, output_filename):
    csv_headers = ["Name","GrossRevenue","TotalUnits","DiscountCost"]

    sorted_products = list(product_dict.values())
    sorted_products.sort(key=lambda x: x["gross_revenue"], reverse=True)

    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)

        writer.writeheader()

        for product in sorted_products:
            row_to_write = {
                "Name": product["name"],
                "GrossRevenue": product["gross_revenue"],
                "TotalUnits": product["total_units"],
                "DiscountCost": product["discount_cost"]
            }
            writer.writerow(row_to_write)


def main():
    parser = argparse.ArgumentParser(description="This application will read from 3 input files and use the data within to produce 2 output files") 

    parser.add_argument("-t", "--team", type=str, help="This should be a CSV of the team data", required=True)
    parser.add_argument("-p", "--product", type=str, help="This should be a CSV of the product master data", required=True)
    parser.add_argument("-s", "--sales", type=str, help="This should be a CSV of the sales data", required=True)
    parser.add_argument("--team-report", type=str, help="Name of team report output CSV file", required=False)
    parser.add_argument("--product-report", type=str, help="Name of product report output CSV file", required=False)

    args = parser.parse_args()

    # Save input files name inorder to traverse them
    input_files = [args.team, args.product, args.sales]

    # 
    team_out = args.team_report if args.team_report else "TeamReport.csv"
    product_out = args.product_report if args.product_report else "ProductReport.csv"

    team_dict = {}
    product_master_dict = {}

    # Read each input file, process team data, product data, and sale data
    for filename in input_files:

        print(f"Processing file: {filename}")

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

                    # extract sales details in order to calculate gross revenue of each team
                    product_id = row[1].strip()
                    team_id = row[2].strip()
                    quantity = int(row[3])
                    discount = float(row[4])

                    # extract product details to calculate the gross revenue of each team
                    name = product_master_dict[product_id]["name"]
                    price_per_unit = float(product_master_dict[product_id]["price"])
                    lot_size = float(product_master_dict[product_id]["lot_size"])

                    gross_revenue_sale = price_per_unit * quantity * lot_size
                    discount_cost = gross_revenue_sale * (discount / 100) 

                    # using sale and product details, append revenue from each sale to gross sale of each team
                    if team_id in team_dict:
                        team_dict[team_id]["gross_revenue"] += gross_revenue_sale

                        # using sale and product details, append the revenue from this product's sale to it's gross revenue in products dictionary
                        product_master_dict[product_id]["gross_revenue"] += gross_revenue_sale
                        product_master_dict[product_id]["total_units"] += quantity * lot_size
                        product_master_dict[product_id]["discount_cost"] += discount_cost

    # for debugging
    # print(team_dict)
    # print()
    # print(product_master_dict)

    # Create team report and product report csv files
    team_report(team_dict,team_out)
    product_report(product_master_dict,product_out)


if __name__ == "__main__":
    main()