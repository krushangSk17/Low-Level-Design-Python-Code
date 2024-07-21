"""
BLUEPRINT TO UNDERSTAND IT BETTER
LLD COFFEE VENDING MACHINE

Classes:
1. Coffee: Represents a coffee drink.
   - Attributes: name, price, recipe
   - Methods: __init__(name, price, recipe)

2. Ingredient: Represents an ingredient.
   - Attributes: name, quantity
   - Methods: __init__(name, quantity), update_quantity(amount)

3. Payment: Represents a payment.
   - Attributes: amount
   - Methods: __init__(amount)

4. CoffeeMachine: Singleton coffee vending machine.
   - Attributes: _instance, coffee_menu, ingredients
   - Methods: __init__(), get_instance(), _initialize_coffee_menu(), _initialize_ingredients(), display_menu(), select_coffee(coffee_name), dispense_coffee(coffee, payment), _has_enough_ingredients(coffee), _update_ingredients(coffee)

5. CoffeeVendingMachineDemo: Demonstrates the coffee vending machine.
   - Methods: run()

Usage:
- Initialize coffee machine with CoffeeMachine.get_instance().
- Display coffee menu using display_menu().
- Select and dispense coffee using select_coffee(coffee_name) and dispense_coffee(coffee, payment).
"""


class Coffee:
    def __init__(self, name, price, recipe):
        self.name = name
        self.price = price
        self.recipe = recipe

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_recipe(self):
        return self.recipe


class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def update_quantity(self, amount):
        self.quantity += amount


class Payment:
    def __init__(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount
    

class CoffeeMachine:
    _instance = None

    def __init__(self):
        if CoffeeMachine._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CoffeeMachine._instance = self
            self.coffee_menu = []
            self.ingredients = {}
            self._initialize_ingredients()
            self._initialize_coffee_menu()

    @staticmethod
    def get_instance():
        if CoffeeMachine._instance is None:
            CoffeeMachine()
        return CoffeeMachine._instance

    def _initialize_coffee_menu(self):
        espresso_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1
        }
        self.coffee_menu.append(Coffee("Espresso", 2.5, espresso_recipe))

        cappuccino_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1,
            self.ingredients["Milk"]: 1
        }
        self.coffee_menu.append(Coffee("Cappuccino", 3.5, cappuccino_recipe))

        latte_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1,
            self.ingredients["Milk"]: 2
        }
        self.coffee_menu.append(Coffee("Latte", 4.0, latte_recipe))

    def _initialize_ingredients(self):
        self.ingredients["Coffee"] = Ingredient("Coffee", 10)
        self.ingredients["Water"] = Ingredient("Water", 10)
        self.ingredients["Milk"] = Ingredient("Milk", 10)

    def display_menu(self):
        print("Coffee Menu:")
        for coffee in self.coffee_menu:
            print(f"{coffee.get_name()} - ${coffee.get_price()}")

    def select_coffee(self, coffee_name):
        for coffee in self.coffee_menu:
            if coffee.get_name().lower() == coffee_name.lower():
                return coffee
        return None

    def dispense_coffee(self, coffee, payment):
        if payment.get_amount() >= coffee.get_price():
            if self._has_enough_ingredients(coffee):
                self._update_ingredients(coffee)
                print(f"Dispensing {coffee.get_name()}...")
                change = payment.get_amount() - coffee.get_price()
                if change > 0:
                    print(f"Please collect your change: ${change}")
            else:
                print(f"Insufficient ingredients to make {coffee.get_name()}")
        else:
            print(f"Insufficient payment for {coffee.get_name()}")

    def _has_enough_ingredients(self, coffee):
        for ingredient, required_quantity in coffee.get_recipe().items():
            if ingredient.get_quantity() < required_quantity:
                return False
        return True

    def _update_ingredients(self, coffee):
        for ingredient, required_quantity in coffee.get_recipe().items():
            ingredient.update_quantity(-required_quantity)
            if ingredient.get_quantity() < 3:
                print(f"Low inventory alert: {ingredient.get_name()}")


class CoffeeVendingMachineDemo:
    @staticmethod
    def run():
        coffee_machine = CoffeeMachine.get_instance()

        # Display coffee menu
        coffee_machine.display_menu()

        # Simulate user requests
        espresso = coffee_machine.select_coffee("Espresso")
        coffee_machine.dispense_coffee(espresso, Payment(3.0))

        cappuccino = coffee_machine.select_coffee("Cappuccino")
        coffee_machine.dispense_coffee(cappuccino, Payment(3.5))

        latte = coffee_machine.select_coffee("Latte")
        coffee_machine.dispense_coffee(latte, Payment(4.0))


if __name__ == "__main__":
    CoffeeVendingMachineDemo.run()