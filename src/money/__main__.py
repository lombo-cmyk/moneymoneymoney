import argparse
import os.path

parser = argparse.ArgumentParser(
    prog="MoneyMoneyMoney",
    description="Count income vs outcome and categorize it " "a bit",
)
parser.add_argument(
    "-f",
    "--file",
    help="Relative path to the .csv file to " "parse",
    required=True,
    type=str,
)
parser.add_argument(
    "-db --database",
    help="Relative path to the .csv "
    "'database' file with tips how to classify transactions",
)
args = parser.parse_args()

transaction_file = os.path.join(f"{args.file}")
