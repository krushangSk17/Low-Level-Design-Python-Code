"""
BLUE PRINT TO UNDERSTAND IT BETTER
LLD LOCKER SYSTEM

Classes:
1. Size (Enum): Represents the size of products and lockers.
   - Values: SMALL = 0, MEDIUM = 1, LARGE = 2

2. Product: Represents the products stored in lockers.
   - Attributes: id , name, size, locker (refers to Locker)

3. Locker: Represents the lockers that store products.
   - Attributes: id , size, product (refers to Product)

4. System: Manages lockers and products.
   - Attributes: lockers, products, available lockers [list of all assets]
   - Methods: create_locker(size), create_product(name, size), fetch_locker(product), add_product(product), remove_product(product)

Usage:
- System initialization
- Create lockers of various sizes
- Create products and assign to lockers
- Attempt to handle overflows when lockers are full
- Remove products and reuse lockers
"""


from enum import Enum

class Size(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

class Product:
    ID = 0  # Class variable for auto-incrementing product ID

    def __init__(self, size, name):
        self.id = Product.ID
        Product.ID += 1
        self.name = name
        self.size = self.get_size_enum(size)
        self.locker = None

    def get_size_enum(self, size_str):
        size_str = size_str.lower()
        if size_str in ['small', 'medium', 'large']:
            return Size[size_str.upper()]
        else:
            raise ValueError("Invalid size provided. Available sizes are: small, medium, large.")

    def __str__(self):
        return f"Product(ID: {self.id}, Name: {self.name}, Size: {self.size.name})"

class Locker:
    ID = 0  # Class variable for auto-incrementing locker ID

    def __init__(self, size):
        self.id = Locker.ID
        Locker.ID += 1
        self.size = self.get_size_enum(size)
        self.product = None

    def get_size_enum(self, size_str):
        size_str = size_str.lower()
        if size_str in ['small', 'medium', 'large']:
            return Size[size_str.upper()]
        else:
            raise ValueError("Invalid size provided. Available sizes are: small, medium, large.")

    def __str__(self):
        return f"Locker(ID: {self.id}, Size: {self.size.name}, Occupied: {self.product is not None})"

class System:
    def __init__(self):
        self.lockers = []
        self.products = {}
        self.available_lockers = {Size.SMALL: [], Size.MEDIUM: [], Size.LARGE: []}

    def create_locker(self, size):
        locker = Locker(size)
        self.lockers.append(locker)
        self.available_lockers[locker.size].append(locker)
        print(f"New locker added: {locker}")

    def create_product(self, name, size):
        product = Product(size, name)
        self.products[product.id] = product
        print(f"New product added: {product}")
        return product

    def fetch_locker(self, product):
        try:
            for size_val in range(product.size.value, 3):
                if self.available_lockers[Size(size_val)]:
                    locker = self.available_lockers[Size(size_val)].pop(0)
                    return locker
            raise Exception('A suitable size locker is not available')
        except Exception as e:
            print(e)
            return None

    def add_product(self, product):
        locker = self.fetch_locker(product)
        if locker:
            locker.product = product
            product.locker = locker
            print(f"{product} put in: {locker}")

    def remove_product(self, product):
        locker = product.locker
        if locker:
            self.available_lockers[locker.size].append(locker)
            locker.product = None
            product.locker = None
            print(f"{product} has been removed from: {locker}")
        else:
            print("Product is not in a locker.")

if __name__ == '__main__':
    system = System()
    system.create_locker('small')
    system.create_locker('medium')
    system.create_locker('large')
    product1 = system.create_product("Laptop", "medium")
    system.add_product(product1)

    product2 = system.create_product("Phone", "small")
    product3 = system.create_product("Monitor", "large")
    system.add_product(product2)
    system.add_product(product3)

    # Attempt to add another product with no available locker
    product4 = system.create_product("Tablet", "medium")
    system.add_product(product4)


