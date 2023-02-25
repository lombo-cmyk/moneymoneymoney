import os.path

import pandas

from money._logger import logger
from money._parser import args
from money.constants import Header

TRANSACTIONS_PATH = os.path.join(os.getcwd(), args.file)
RULES_PATH = os.path.join(os.getcwd(), args.database)


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
        [
            Header.POSTING_DATE,
            Header.ACCOUNT_NR,
            Header.BANK_NAME,
            Header.DETAILS,
            Header.TRANSACTION_NR,
            Header.BLOCKED_AMOUNT,
            Header.CURRENCY_BLOCKED,
            Header.PAYMENT_AMOUNT_IN_CURRENCY,
            Header.CURRENCY_PAYMENT_AMOUNT_IN_CURRENCY,
            Header.BALANCE_AFTER_TRANSACTION,
            Header.CURRENCY_BALANCE_AFTER_TRANSACTION,
        ],
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
    logger.info(f"Using file: {TRANSACTIONS_PATH} with rules from {RULES_PATH}")
    transactions = get_transactions_data()
    a = 1


if __name__ == "__main__":
    main()
