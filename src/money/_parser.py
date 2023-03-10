import argparse
import os

from money.common._parser import parser as common_parser

parser = argparse.ArgumentParser(
    prog="MoneyMoneyMoney",
    description="Count income vs outcome and categorize it " "a bit",
    parents=[common_parser],
    conflict_handler="resolve",
)
parser.add_argument(
    "-f",
    "--file",
    dest="file",
    default="",
    help="Relative path to the .csv file to " "parse",
    type=str,
)
parser.add_argument(
    "-db --database",
    dest="database",
    default=os.path.join("output", "rules.csv"),
    help="Relative path to the .csv "
    "'database' file with rules on how to classify transactions",
)

parser.add_argument(
    "--create-rules",
    dest="create_rules",
    action="store_true",
    default=False,
    help="Create local rules entries",
)

args = parser.parse_args()
