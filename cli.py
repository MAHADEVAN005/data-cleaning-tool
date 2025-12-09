import argparse
from data_cleaner import clean_csv

def main():
    parser = argparse.ArgumentParser(
        description="Automatic CSV Cleaning Tool by Mahadevan"
    )

    parser.add_argument("--input", "-i", required=True, help="Path of input CSV file")
    parser.add_argument("--output", "-o", required=True, help="Path to save cleaned CSV")

    args = parser.parse_args()

    clean_csv(args.input, args.output)

if __name__ == "__main__":
    main()
