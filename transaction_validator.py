"""

    +-------------------+
    |    Transaction    |
    +-------------------+
    | - amount: float   |
    | - sender: str     |
    | - receiver: str   |
    | - timestamp: str  |
    +-------------------+

            |
            | Uses
            V

    +-------------------+
    |       Rule        |
    +-------------------+
    | + is_valid(...)   |
    +-------------------+
            ^
            | Inherits
            |
+-----------------------+   +------------------------+   +--------------------------+
|      AmountRule       |   |      SenderRule        |   |      ReceiverRule        |
+-----------------------+   +------------------------+   +--------------------------+
| - min_amount: float   |   | - allowed_senders: set |   | - allowed_receivers: set |
| - max_amount: float   |   +------------------------+   +--------------------------+
+-----------------------+   | + is_valid(...)        |   | + is_valid(...)          |
                            +------------------------+   +--------------------------+

            |
            | Uses
            V

    +-----------------------+
    | TransactionValidator  |
    +-----------------------+
    | - rules: list[Rule]   |
    +-----------------------+
    | + is_valid(...)       |
    +-----------------------+



"""

class Transaction:
    def __init__(self, amount: float, sender: str, receiver: str, timestamp: str):
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp

from abc import ABC, abstractmethod

class Rule(ABC):
    @abstractmethod
    def is_valid(self, transaction: Transaction) -> bool:
        pass

class AmountRule(Rule):
    def __init__(self, min_amount: float, max_amount: float):
        self.min_amount = min_amount
        self.max_amount = max_amount
    def is_valid(self, transaction: Transaction) -> bool:
        return self.min_amount <= transaction.amount <= self.max_amount

class SenderRule(Rule):
    def __init__(self, allowed_senders: set):
        self.allowed_senders = allowed_senders
    def is_valid(self, transaction: Transaction) -> bool:
        return transaction.sender in self.allowed_senders

class ReceiverRule(Rule):
    def __init__(self, allowed_receivers: set):
        self.allowed_receivers = allowed_receivers
    def is_valid(self, transaction: Transaction) -> bool:
        return transaction.receiver in self.allowed_receivers

class TransactionValidator:
    def __init__(self, rules: list):
        self.rules = rules
    def is_valid(self, transaction: Transaction) -> bool:
        return all(rule.is_valid(transaction) for rule in self.rules)

# Example usage:
allowed_categories = ["electronics", "furniture"]
max_capacity = 1000.0  # Example capacity in weight units

validator = TransactionValidator(rules=[
    AmountRule(min_amount=10, max_amount=1000),
    SenderRule(allowed_senders={'Alice', 'Bob'}),
    ReceiverRule(allowed_receivers={'Charlie', 'David'})
])

transaction1 = Transaction(amount=50, sender='Alice', receiver='Charlie', timestamp='2024-07-21T10:00:00Z')
transaction2 = Transaction(amount=5000, sender='Alice', receiver='Charlie', timestamp='2024-07-21T10:00:00Z')
transaction3 = Transaction(amount=50, sender='Eve', receiver='Charlie', timestamp='2024-07-21T10:00:00Z')

print(validator.is_valid(transaction1))  # Output: True
print(validator.is_valid(transaction2))  # Output: False
print(validator.is_valid(transaction3))  # Output: False
