import pandas

from money.constants import RelevantHeader, Rules


class Rule:
    def __init__(self, rule: pandas.Series):
        self.id = int(rule[Rules.ID])
        self.receiver = rule[Rules.RECEIVER_DATA].lower()
        self.title = rule[Rules.TITLE].lower()
        self.destination = rule[Rules.WHERE].lower()


def print_existing_rules(rules_path) -> None:
    try:
        rules = pandas.read_csv(rules_path, delimiter=";")
    except pandas.errors.EmptyDataError:
        print("No existing rules")
        d = {Rules.ID: [], Rules.RECEIVER_DATA: [], Rules.TITLE: [], Rules.WHERE: []}
        df = pandas.DataFrame(data=d)
        df.to_csv(path_or_buf=rules_path, sep=";", index=False)
        print(f"Initial rules structure: {df}")
        return
    print(rules)


def get_last_rule_index(rules_path) -> int:
    rules = pandas.read_csv(rules_path, delimiter=";")
    if rules.tail(1)[Rules.ID].empty:
        return 0
    else:
        return rules.iloc[-1][Rules.ID]


def create_rules(rules_path: str):
    print(f"Creating rules in {rules_path}.\nAlready existing rules:")
    print_existing_rules(rules_path)
    print("Rules can be created for:")
    print(f"1. Contains selected text in {RelevantHeader.RECEIVER_DATA}")
    print(f"2. Contains selected text in {RelevantHeader.TITLE}")
    print("User can select one or both rules. Leaving a rule empty acts as *")
    print("Leaving both fields empty exits the program.")
    print("Third field tells the program where to store the data")
    print("Entries that don't match any rules will be stored as General")

    while True:
        last_rule_id = get_last_rule_index(rules_path)
        print(f"Creating rule {last_rule_id + 1}")
        receiver_data = input(f"Enter {RelevantHeader.RECEIVER_DATA}: ").lower()
        title = input(f"Enter {RelevantHeader.TITLE}: ").lower()
        destination = input("Enter Destination: ").lower()
        if any([receiver_data, title]) and destination:
            rules = pandas.read_csv(rules_path, delimiter=";")
            entry = {
                Rules.ID: [last_rule_id + 1],
                Rules.RECEIVER_DATA: [receiver_data],
                Rules.TITLE: [title],
                Rules.WHERE: [destination],
            }
            rules = pandas.concat([rules, pandas.DataFrame(entry)], ignore_index=True)
            rules.to_csv(sep=";", path_or_buf=rules_path, index=False)
        else:
            print("Closing...")
            break
