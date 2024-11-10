#!/usr/bin/env python3

import json
import csv
import sys
from datetime import datetime

# Check if the input file is provided
if len(sys.argv) < 2:
    print("Usage: python empower-finance-export-util.py <input_file.json> [--monthly]")
    sys.exit(1)

input_file = sys.argv[1]
output_file = 'output_data.tsv'

# Check for the '--monthly' argument
monthly = '--monthly' in sys.argv

try:
    # Load JSON data from the specified file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Extract date and totalAssets (or aggregateBalance) from the JSON structure
    history = data['spData'].get('histories', [])
    output_data = []
    for entry in history:
        date_str = entry.get('date')
        if date_str is None:
            continue  # Skip entries without a date

        # Parse the date string into a datetime object
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            continue  # Skip entries with invalid date format

        # If '--monthly' is specified, include only the first day of the month
        if monthly and date_obj.day != 1:
            continue

        # Try to get 'totalAssets' directly
        total_assets = entry.get('totalAssets')

        # If 'totalAssets' is not available, try 'aggregateBalance'
        if total_assets is None:
            total_assets = entry.get('aggregateBalance')

        # If 'aggregateBalance' is not available, try to sum balances
        if total_assets is None and 'balances' in entry:
            balances = entry['balances']
            # Exclude any keys that are annotations
            total_assets = sum(
                value for key, value in balances.items()
                if not key.endswith('Annotation') and isinstance(value, (int, float))
            )

        # If we found a total assets value, add it to the output data
        if total_assets is not None:
            output_data.append((date_str, total_assets))

    if not output_data:
        print("No data with 'date' and asset values found in the input file.")
        sys.exit(1)

    # Write to TSV file
    with open(output_file, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerow(['Date', 'Total Assets'])
        writer.writerows(output_data)

    print(f"TSV file '{output_file}' has been created.")

except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    sys.exit(1)
except KeyError as e:
    print(f"Missing expected data: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
