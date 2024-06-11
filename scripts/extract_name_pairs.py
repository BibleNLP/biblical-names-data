import pandas as pd
import argparse

df = pd.read_csv("./names.tsv", sep="\t", low_memory=False)

parser = argparse.ArgumentParser(description='Extract name pairs from a TSV file')
parser.add_argument('source_column', nargs='?', type=str, default=None,
                    help='Name of the source column to extract')
parser.add_argument('target_column', nargs='?', type=str, default=None,
                    help='Name of the target column to extract')
parser.add_argument('-l', '--list', action='store_true',
                    help='List available columns')    
args = parser.parse_args()


# Print list of columns if --list argument is provided
if args.list:
    print("Availabe columns:")
    # print the first cols in order (these are original language/id columns)
    for col in df.columns[:5]:
        print("  - {}".format(col))
    # print the rest of the columns in alphabetical order
    for col in sorted(df.columns[5:]):
        print("  - {}".format(col))
    print("See README.md for an explanation of each column.")
    exit()
elif args.source_column is None or args.target_column is None:
    parser.error('You must provide either -l/--list or two column names.')

# Otherwise, proceed with the extraction...
source_col = args.source_column.lower()
target_col = args.target_column.lower()

# Extract the name pairs where both columns are not null
name_pairs = df[[source_col, target_col]].dropna()

print(name_pairs)

# Confirm output to "namelist.{col_1}.txt" and "namelist.{col_2}.txt"
print("Preparing to save the output to files...")
print(" 1. namelist.{}.txt".format(source_col))
print(" 2. namelist.{}.txt".format(target_col))

confirmation = input("Do you want to save these output to files? (y/n): ")
while confirmation not in ["y", "n"]:
    confirmation = input("Please enter 'y' or 'n': ")

if confirmation == "y":
    name_pairs[source_col].to_csv("namelist.{}-{}.source.txt".format(source_col, target_col), index=False)
    name_pairs[target_col].to_csv("namelist.{}-{}.target.txt".format(source_col, target_col), index=False)
    print("Output saved successfully!")
