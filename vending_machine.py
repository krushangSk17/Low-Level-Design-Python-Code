"""

BLUE PRINT TO UNDERSTAND IT BETTER
LLD VENDING MACHINE SYSTEM

Classes:
1. Coin (Enum): Represents different coin denominations.
   - Values: PENNY = 0.01, NICKEL = 0.05, DIME = 0.1, QUARTER = 0.25

2. Note (Enum): Represents different note denominations.
   - Values: ONE = 1, FIVE = 5, TEN = 10, TWENTY = 20

3. Product: Represents products available in the vending machine.
   - Attributes: name, price

4. Inventory: Manages the inventory of products.
   - Attributes: products
   - Methods: add_product(product, quantity), update_quantity(product, quantity), is_available(product)

5. VendingMachineState (Abstract Class): Base class for different states of the vending machine.
   - Attributes: vending_machine
   - Methods: select_product(product), insert_coin(coin), insert_note(note), dispense_product(), return_change()

6. IdleState: Represents the state when the machine is idle.
   - Inherits: VendingMachineState
   - Methods: select_product(product), insert_coin(coin), insert_note(note), dispense_product(), return_change()

7. ReadyState: Represents the state when a product is selected and waiting for payment.
   - Inherits: VendingMachineState
   - Methods: select_product(product), insert_coin(coin), insert_note(note), dispense_product(), return_change()

8. DispenseState: Represents the state when the product is being dispensed.
   - Inherits: VendingMachineState
   - Methods: select_product(product), insert_coin(coin), insert_note(note), dispense_product(), return_change()

9. ReturnChangeState: Represents the state when returning change.
   - Inherits: VendingMachineState
   - Methods: select_product(product), insert_coin(coin), insert_note(note), dispense_product(), return_change()

10. VendingMachine: Manages the state transitions and operations of the vending machine.
    - Attributes: inventory, idle_state, ready_state, dispense_state, return_change_state, current_state, selected_product, total_payment
    - Methods: select_product(product), insert_coin(coin), insert_note(note), dispense_product(), return_change(), set_state(state)

Usage:
- System initialization with a list of products and their quantities.
- Select a product to purchase.
- Insert coins or notes to make payment.
- Dispense the selected product after payment is complete.
- Return any change if overpayment is made.
- Transition between different states (Idle, Ready, Dispense, ReturnChange) to handle operations.


"""


from enum import Enum
from abc import ABC, abstractmethod

class Coin(Enum):
    PENNY = 0.01
    NICKEL = 0.05
    DIME = 0.1
    QUARTER = 0.25

class Note(Enum):
    ONE = 1
    FIVE = 5
    TEN = 10
    TWENTY = 20

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity):
        self.products[product] = quantity

    def update_quantity(self, product, quantity):
        self.products[product] = quantity

    def is_available(self, product):
        return self.products.get(product, 0) > 0

class VendingMachineState(ABC):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    @abstractmethod
    def select_product(self, product):
        pass

    @abstractmethod
    def insert_coin(self, coin):
        pass

    @abstractmethod
    def insert_note(self, note):
        pass

    @abstractmethod
    def dispense_product(self):
        pass

    @abstractmethod
    def return_change(self):
        pass

class IdleState(VendingMachineState):
    def select_product(self, product: Product):
        if self.vending_machine.inventory.is_available(product):
            self.vending_machine.selected_product = product
            self.vending_machine.set_state(self.vending_machine.ready_state)
            print(f"Product selected: {product.name}")
        else:
            print(f"Product not available: {product.name}")

    def insert_coin(self, coin: Coin):
        print("Please select a product first.")

    def insert_note(self, note: Note):
        print("Please select a product first.")

    def dispense_product(self):
        print("Please select a product and make payment.")

    def return_change(self):
        print("No change to return.")

class ReadyState(VendingMachineState):
    def select_product(self, product: Product):
        print("Product already selected. Please make payment.")

    def insert_coin(self, coin: Coin):
        self.vending_machine.total_payment += coin.value
        print(f"Coin inserted: {coin.name} worth ${coin.value:.2f}")
        if self.vending_machine.total_payment >= self.vending_machine.selected_product.price:
            self.vending_machine.set_state(self.vending_machine.dispense_state)

    def insert_note(self, note: Note):
        self.vending_machine.total_payment += note.value
        print(f"Note inserted: {note.name} worth ${note.value:.2f}")
        if self.vending_machine.total_payment >= self.vending_machine.selected_product.price:
            self.vending_machine.set_state(self.vending_machine.dispense_state)

    def dispense_product(self):
        print("Please make payment first.")

    def return_change(self):
        print("Make payment and collect the dispensed product first.")

class DispenseState(VendingMachineState):
    def select_product(self, product: Product):
        print("Product already selected. Please collect the dispensed product.")

    def insert_coin(self, coin: Coin):
        print("Payment already made. Please collect the dispensed product.")

    def insert_note(self, note: Note):
        print("Payment already made. Please collect the dispensed product.")

    def dispense_product(self):
        product = self.vending_machine.selected_product
        self.vending_machine.inventory.update_quantity(product, self.vending_machine.inventory.products[product] - 1)
        print(f"Product dispensed: {product.name}")
        self.vending_machine.set_state(self.vending_machine.return_change_state)

    def return_change(self):
        print("Please collect the dispensed product first.")

class ReturnChangeState(VendingMachineState):
    def select_product(self, product: Product):
        print("Please collect the change first.")

    def insert_coin(self, coin: Coin):
        print("Please collect the change first.")

    def insert_note(self, note: Note):
        print("Please collect the change first.")

    def dispense_product(self):
        print("Product already dispensed. Please collect the change.")

    def return_change(self):
        change = self.vending_machine.total_payment - self.vending_machine.selected_product.price
        if change > 0:
            print(f"Change returned: ${change:.2f}")
        else:
            print("No change left")
        self.vending_machine.total_payment = 0
        self.vending_machine.selected_product = None
        self.vending_machine.set_state(self.vending_machine.idle_state)

class VendingMachine:
    def __init__(self):
        self.inventory = Inventory()
        self.idle_state = IdleState(self)
        self.ready_state = ReadyState(self)
        self.dispense_state = DispenseState(self)
        self.return_change_state = ReturnChangeState(self)
        self.current_state = self.idle_state
        self.selected_product = None
        self.total_payment = 0.0

    def select_product(self, product: Product):
        self.current_state.select_product(product)

    def insert_coin(self, coin: Coin):
        self.current_state.insert_coin(coin)

    def insert_note(self, note: Note):
        self.current_state.insert_note(note)

    def dispense_product(self):
        self.current_state.dispense_product()

    def return_change(self):
        self.current_state.return_change()

    def set_state(self, state: VendingMachineState):
        self.current_state = state

class VendingMachineDemo:
    @staticmethod
    def run():
        vending_machine = VendingMachine()

        # Add products to the inventory
        coke = Product("Coke", 1.5)
        pepsi = Product("Pepsi", 1.25)
        water = Product("Water", 1.0)

        vending_machine.inventory.add_product(coke, 5)
        vending_machine.inventory.add_product(pepsi, 3)
        vending_machine.inventory.add_product(water, 2)

        # Select a product
        vending_machine.select_product(coke)

        # Insert coins
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)

        # Insert a note
        vending_machine.insert_note(Note.ONE)

        # Dispense the product
        vending_machine.dispense_product()

        # Return change
        vending_machine.return_change()

        # Select another product
        vending_machine.select_product(pepsi)

        # Insert insufficient payment
        vending_machine.insert_coin(Coin.QUARTER)

        # Try to dispense the product
        vending_machine.dispense_product()

        # Insert more coins
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)
        vending_machine.insert_coin(Coin.QUARTER)

        # Dispense the product
        vending_machine.dispense_product()

        # Return change
        vending_machine.return_change()

if __name__ == "__main__":
    VendingMachineDemo.run()
