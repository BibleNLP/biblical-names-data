import argparse
import pandas as pd

def save_column_to_csv(df, column, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{column}\n")  # Write the header
        for value in df[column]:
            if pd.isna(value) or value == "":
                f.write("\n")  # Write an empty line for NaN, None, or empty string
            else:
                f.write(f"{value}\n")  # Write the actual value

def main():
    parser = argparse.ArgumentParser(description='Extract name pairs from a TSV file')
    parser.add_argument('source_column', nargs='?', type=str, default=None,
                    help='Name of the source column to extract')
    parser.add_argument('target_column', nargs='?', type=str, default=None,
                    help='Name of the target column to extract')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List available columns')    
    parser.add_argument('-a', '--all', action='store_true',
                        help='Output each column as a file.')
    parser.add_argument('-y', '--yes', action='store_true',
                        help='Skip confirmation messages.')

    args = parser.parse_args()
    skip = args.yes

    df = pd.read_csv("./names.tsv", encoding='utf-8', sep="\t", low_memory=False)

    # Print list of columns if --list argument is provided
    if args.list:
        print("Availabe columns:")
        # print the first cols in order (these are original language/id columns)
        for column in df.columns[:5]:
            print(f"  - {column}")
        # print the rest of the columns in alphabetical order
        for column in sorted(df.columns[5:]):
            print(f"  - {column}")
        print("See README.md for an explanation of each column.")
        exit()

    elif args.all:
        columns = [column for column in df.columns]
        
        for i, column in enumerate(columns):
            filename = f"{column}.txt"
            if skip:
                save_column_to_csv(df, column, filename)
                print(f"Saved column {column} to file {filename}")
                continue
            else:
                # Confirm output to "namelist.{col_1}.txt" and "namelist.{col_2}.txt"
                print("Preparing to save the output to files...")
                print(f" {i}. {filename} {column}")
                confirmation = input("Do you want to save this file? (y/n): ")
                while confirmation not in ["y", "n"]:
                    confirmation = input("Please enter 'y' or 'n': ")
                if confirmation == "y":
                    save_column_to_csv(df, column, filename)

    elif args.source_column is None or args.target_column is None:
        parser.error('You must provide either option --all or --list or two column names.')
    
    else: 
        # Otherwise, proceed with the extraction...
        source_col = args.source_column.lower()
        target_col = args.target_column.lower()

        # Extract the name pairs where both columns are not null
        name_pairs = df[[source_col, target_col]].dropna()
        print(name_pairs)

        # Confirm output to "namelist.{col_1}.txt" and "namelist.{col_2}.txt"
        print("Preparing to save the output to files...")
        print(f" 1. namelist.{source_col}.txt")
        print(f" 2. namelist.{target_col}.txt")

        if skip:
            name_pairs[source_col].to_csv(f"namelist.{source_col}-{target_col}.source.txt", index=False)
            name_pairs[target_col].to_csv(f"namelist.{source_col}-{target_col}.target.txt", index=False)
            print("Output saved successfully!")
        else:
            confirmation = input("Do you want to save these output to files? (y/n): ")
            while confirmation not in ["y", "n"]:
                confirmation = input("Please enter 'y' or 'n': ")

            if confirmation == "y":
                name_pairs[source_col].to_csv(f"namelist.{source_col}-{target_col}.source.txt", index=False)
                name_pairs[target_col].to_csv(f"namelist.{source_col}-{target_col}.target.txt", index=False)
                print("Output saved successfully!")

if __name__ == "__main__":
    main()