import os
from collections import OrderedDict
from datetime import datetime
from typing import Optional

import pandas

from money._logger import logger
from money.constants import DEFAULT_SUM_FIELD, RelevantHeader, Rules
from money.rules import Rule


class Transaction:
    def __init__(self, transaction: pandas.Series):
        self.receiver = transaction[RelevantHeader.RECEIVER_DATA].lower()
        self.title = transaction[RelevantHeader.TITLE].lower()
        self.amount = float(transaction[RelevantHeader.AMOUNT].replace(",", "."))
        self.currency = transaction[RelevantHeader.CURRENCY_AMOUNT].lower()


class TransactionConsumer:
    def __init__(self, transactions: pandas.DataFrame, rules: pandas.DataFrame):
        self.transactions = transactions
        self.rules = rules
        self.output: Optional[pandas.DataFrame] = self._create_output_df()

    def run(self):
        results_dir = os.path.join(os.getcwd(), "output")
        output_path = os.path.join(
            results_dir, datetime.now().strftime("%Y_%m_%d_%H_%M_%S/")
        )
        for _, _transaction in self.transactions.iterrows():
            transaction = Transaction(_transaction)
            logger.info(f"Working on {transaction.title}")
            for index, _rule in self.rules.iterrows():
                rule = Rule(_rule)
                if self.is_condition_met(rule, transaction):
                    self._update_output_sum(rule.destination, transaction.amount)
                    break
                elif index == self.rules.shape[0] - 1:
                    logger.info(f"No rule found for {transaction.title}")
                    self._update_output_sum(DEFAULT_SUM_FIELD, transaction.amount)
                    break
        logger.info(f"Saving output to file {output_path}")
        self.output.to_csv(path_or_buf=output_path, sep=";", index=True)
        print(self.output)

    @staticmethod
    def is_condition_met(rule: Rule, transaction: Transaction):
        is_title = rule.title in transaction.title
        is_receiver = rule.receiver in transaction.receiver
        return is_title and is_receiver

    def _create_output_df(self):
        types = [DEFAULT_SUM_FIELD] + list(
            OrderedDict.fromkeys(self.rules[Rules.WHERE])
        )
        return pandas.DataFrame(columns=["sum"], index=types).fillna(0)

    def _update_output_sum(self, destination: str, amount: float):
        prev_sum = self.output["sum"][destination]
        new_sum = prev_sum + amount
        self.output["sum"][destination] = new_sum
