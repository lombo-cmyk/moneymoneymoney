import argparse
import os.path

parser = argparse.ArgumentParser(
    prog="MoneyMoneyMoney",
    description="Count income vs outcome and categorize it " "a bit",
)
parser.add_argument("-f", "--file", type=str)
args = parser.parse_args()


transaction_file = os.path.join("transactions/", f"{args.file}")
