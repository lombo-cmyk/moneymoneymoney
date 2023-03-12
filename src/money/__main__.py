import os

import pandas
import pytesseract

from money._logger import logger
from money._parser import args
from money.common.receipt import Receipt
from money.constants import Header, IrrelevantHeader
from money.rules import create_rules
from money.transaction import TransactionConsumer

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


def get_rules(rules_path: str):
    return pandas.read_csv(rules_path, delimiter=";").fillna("")


def check_receipts():
    if args.tesseract:
        pytesseract.pytesseract.tesseract_cmd = args.tesseract
    poppler_path = args.poppler if args.poppler else None
    receipt_path = os.path.join(os.getcwd(), args.receipt)

    receipt = Receipt(receipt_path, args.city, poppler_path)
    receipt.create_receipt()

    print(f"Including {receipt.total} in k on {receipt.date}")


def main():
    default_rules_path = create_files_structure()
    if CREATE_DATABASE:
        create_rules(default_rules_path)
    else:
        logger.info(f"Using file: {TRANSACTIONS_PATH} with rules from {RULES_PATH}")
        transactions = get_transactions_data()
        rules = get_rules(default_rules_path)
        consumer = TransactionConsumer(transactions, rules)
        consumer.run()
        if args.receipt and args.city:
            check_receipts()


if __name__ == "__main__":
    main()
