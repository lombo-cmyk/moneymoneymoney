import os

import pandas

from money._logger import logger
from money._parser import args
from money.constants import Header, IrrelevantHeader
from money.rules import create_rules

TRANSACTIONS_PATH = os.path.join(os.getcwd(), args.file)
RULES_PATH = os.path.join(os.getcwd(), args.database)
CREATE_DATABASE = args.create_rules


def create_files_structure():
    cwd = os.getcwd()
    results_dir = os.path.join(cwd, "output")
    rules = os.path.join(results_dir, "rules.csv")
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    if not os.path.exists(rules):
        with open(rules, "x"):
            pass
    return rules


def _drop_unnamed_columns(transactions: pandas.DataFrame):
    cols = transactions.columns
    for col in cols:
        try:
            Header(col)
        except ValueError:
            logger.info(f"{col} is not a known column header. Dropping.")
            transactions.drop(col, axis=1, inplace=True)
    return transactions


def get_transactions_data():
    transactions = pandas.read_csv(
        TRANSACTIONS_PATH, sep=";", encoding="ANSI", header=11
    )
    transactions.drop(transactions.tail(1).index, inplace=True)
    transactions.drop(
        [el for el in IrrelevantHeader],
        axis=1,
        inplace=True,
    )
    transactions = _drop_unnamed_columns(transactions)
    logger.info(
        f"Data headers: {list(transactions.columns)}.\n"
        f"Number of rows: {len(transactions.index)}"
    )
    return transactions


def main():
    default_rules_path = create_files_structure()
    if CREATE_DATABASE:
        create_rules(default_rules_path)
    else:
        logger.info(f"Using file: {TRANSACTIONS_PATH} with rules from {RULES_PATH}")
        # _transactions = get_transactions_data()


if __name__ == "__main__":
    main()
