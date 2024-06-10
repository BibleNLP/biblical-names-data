import pandas as pd
import argparse

df = pd.read_csv("./names.tsv", sep="\t", low_memory=False)

parser = argparse.ArgumentParser(description='Extract name pairs from a TSV file')
parser.add_argument('column_one', nargs='?', type=str, default=None,
                    help='Name of the first column to extract')
parser.add_argument('column_two', nargs='?', type=str, default=None,
                    help='Name of the second column to extract')
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
elif args.column_one is None or args.column_two is None:
    parser.error('You must provide either -l/--list or two column names.')

# Otherwise, proceed with the extraction...
col1 = args.column_one.lower()
col2 = args.column_two.lower()

# Extract the name pairs where both columns are not null
name_pairs = df[[col1, col2]].dropna()

print(name_pairs)

# Confirm output to "namelist.{col_1}.txt" and "namelist.{col_2}.txt"
print("Preparing to save the output to files...")
print(" 1. namelist.{}.txt".format(col1))
print(" 2. namelist.{}.txt".format(col2))

confirmation = input("Do you want to save these output to files? (y/n): ")
while confirmation not in ["y", "n"]:
    confirmation = input("Please enter 'y' or 'n': ")

if confirmation == "y":
    name_pairs[col1].to_csv("namelist.{}-{}.source.txt".format(col1, col2), index=False)
    name_pairs[col2].to_csv("namelist.{}-{}.target.txt".format(col1, col2), index=False)
    print("Output saved successfully!")
