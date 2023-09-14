from decimal import Decimal, ROUND_HALF_UP
from typing import List


class Category:

    def __init__(self, name) -> None:
        self.ledger = []
        self.name = name
        self.balance = 0.00

    def __str__(self) -> str:
        output = ["*************" + self.get_name() + "*************"]

        for line in self.ledger:
            amount = str("{:.2f}".format(float(line.get("amount"))))
            description = line.get("description")[:23]
            space_number = 30 - len(description) - len(amount)

            line_string = description + " " * space_number + amount

            output.append(line_string)

        output.append(f'Total: {"{:.2f}".format(float(self.balance))}')

        for i in range(0, len(output) - 1):
            output[i] = output[i] + "\n"

        return "".join(output)

    def deposit(self, amount: float, description: str = "") -> None:
        line = {"amount": amount, "description": description}

        self.balance += amount
        self.ledger.append(line)

    def withdraw(self, amount: float, description: str = "") -> bool:
        if self.check_funds(amount):
            line = {"amount": -amount, "description": description}

            self.ledger.append(line)
            self.balance -= amount
            return True

        return False

    def get_balance(self) -> float:
        balance = round(self.balance, 2)
        return balance

    def get_name(self) -> str:
        return self.name

    def get_withdrawals(self) -> List[float]:
        withdrawals = []
        for line in self.ledger:
            if line.get("amount") < 0:
                withdrawals.append(abs(line.get("amount")))

        return withdrawals

    def transfer(self, amount: float, category: 'Category') -> bool:
        if self.check_funds(amount):
            category.deposit(amount, f'Transfer from {self.get_name()}')
            return self.withdraw(amount, f'Transfer to {category.get_name()}')

        return False

    def check_funds(self, amount: float):
        return amount <= self.balance


def create_spend_chart(categories) -> str:
    total = 0
    for category in categories:
        total += sum(category.get_withdrawals())

    category_percents = {}

    for category in categories:
        category_percent = (sum(category.get_withdrawals()) / total) * 100
        category_percents.update({category.get_name(): category_percent})

    graph = []

    for i in range(0, 110, 10):
        line = f'{" " * (3 - len(str(i)))}{i}| '
        for category in categories:
            percent = category_percents.get(category.get_name())
            plots = ("   " if percent < i else "o  ")
            line = line + plots
        graph.append(line)

    graph.reverse()

    for i in range(0, len(graph) - 1):
        graph[i] = f'{graph[i]}\n'

    category_names = list(
        map(lambda category: category.get_name().capitalize(), categories))

    plot_names = format_names(category_names)

    return f'Percentage spent by category\n{"".join(graph)}\n    -{"---" * (len(categories))}\n{plot_names}'


def format_names(names):
    longest_name = max(names, key=len)
    combined = ""

    for i in range(len(longest_name)):
        for name in names:
            formatted = ""
            if i < len(name):
                formatted = f'{name[i]}  '
            else:
                formatted = "   "

            if name == names[0]:
                formatted = "     " + formatted
            elif name == names[len(names) - 1] and i != (len(longest_name) - 1):
                formatted = formatted + "\n"

            combined += formatted

    return combined
