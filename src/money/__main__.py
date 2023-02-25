import os
from datetime import datetime

import pandas

from money._logger import logger
from money._parser import args
from money.constants import Header, IrrelevantHeader, RelevantHeader, Rules
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


def get_rules(rules_path: str):
    return pandas.read_csv(rules_path, delimiter=";").fillna("")


def process_transactions(transactions: pandas.DataFrame, rules: pandas.DataFrame):
    default_sum = "General"
    results_dir = os.path.join(os.getcwd(), "output")
    current_working_dir = os.path.join(
        results_dir, datetime.now().strftime("%Y_%m_%d_%H_%M_%S/")
    )
    types = [default_sum] + list(set(rules[Rules.WHERE]))
    output = pandas.DataFrame(columns=["sum"], index=types).fillna(0)
    for _, transaction in transactions.iterrows():
        for index, rule in rules.iterrows():
            if (
                rule[Rules.TITLE] in transaction[RelevantHeader.TITLE].lower()
                and rule[Rules.RECEIVER_DATA]
                in transaction[RelevantHeader.RECEIVER_DATA].lower()
            ):
                prev_sum = output["sum"][rule[Rules.WHERE]]
                new_sum = prev_sum + float(
                    transaction[RelevantHeader.AMOUNT].replace(",", ".")
                )
                output["sum"][rule[Rules.WHERE]] = new_sum
                break
            else:
                if index == rules.shape[0] - 1:
                    prev_sum = output["sum"][default_sum]
                    new_sum = prev_sum + float(
                        transaction[RelevantHeader.AMOUNT].replace(",", ".")
                    )
                    output["sum"][default_sum] = new_sum
                else:
                    continue

    output.to_csv(path_or_buf=current_working_dir, sep=";", index=True)


def main():
    default_rules_path = create_files_structure()
    if CREATE_DATABASE:
        create_rules(default_rules_path)
    else:
        logger.info(f"Using file: {TRANSACTIONS_PATH} with rules from {RULES_PATH}")
        transactions = get_transactions_data()
        rules = get_rules(default_rules_path)
        process_transactions(transactions, rules)


if __name__ == "__main__":
    main()
