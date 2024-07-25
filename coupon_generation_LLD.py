"""
+-------------------+   +-------------------+
|      Category     |   |      Product      |
+-------------------+   +-------------------+
| - category_id     |   | - product_id      |
| - name            |   | - name            |
+-------------------+   | - price           |
                        | - category        |
                        +-------------------+
                                |
                                |
                        +-------------------+
                        |        Cart       |
                        +-------------------+
                        | - products        |
                        | - total_amount    |
                        +-------------------+
                        | + add_product()   |
                        | + get_total_amount() |
                        +-------------------+
                                |
                                | Uses
                                |
             +-------------------+-------------------+
             |              Condition (ABC)          |
             +---------------------------------------+
             | + is_satisfied(cart): bool            |
             +---------------------------------------+
                         ^       ^        ^
                        /        |         \
                       /         |          \
+-------------------+  +-------------------+  +-------------------+
|  ProductCondition |  |  CategoryCondition|  | MinimumAmountCondition |
+-------------------+  +-------------------+  +-------------------+
| - product_id      |  | - category_id     |  | - minimum_amount   |
+-------------------+  +-------------------+  +-------------------+
| + is_satisfied()  |  | + is_satisfied()  |  | + is_satisfied()  |
+-------------------+  +-------------------+  +-------------------+

+-------------------+ 
|      Coupon       | 
+-------------------+
| - code            |
| - discount        |
| - conditions      |
| - expiry_date     |
+-------------------+
| + is_valid()      |
| + apply_discount()|
+-------------------+

+-------------------+ 
|   CouponManager   | 
+-------------------+
| - coupons         |
+-------------------+
| + generate_coupon() |
| + apply_coupon()  |
+-------------------+

"""
from datetime import datetime


from datetime import datetime, timedelta
import random
import string

from abc import ABC, abstractmethod


class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

class Product:
    def __init__(self, product_id, name, price, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category

class Cart:
    def __init__(self):
        self.products = []
        self.total_amount = 0.0

    def add_product(self, product):
        self.products.append(product)
        self.total_amount += product.price

    def get_total_amount(self):
        return self.total_amount

class Condition(ABC):
    @abstractmethod
    def is_satisfied(self, cart):
        pass

class ProductCondition(Condition):
    def __init__(self, product_id):
        self.product_id = product_id

    def is_satisfied(self, cart):
        for product in cart.products:
            if product.product_id == self.product_id:
                return True
        return False

class CategoryCondition(Condition):
    def __init__(self, category_id):
        self.category_id = category_id

    def is_satisfied(self, cart):
        for product in cart.products:
            if product.category.category_id == self.category_id:
                return True
        return False

class MinimumAmountCondition(Condition):
    def __init__(self, minimum_amount):
        self.minimum_amount = minimum_amount

    def is_satisfied(self, cart):
        return cart.total_amount >= self.minimum_amount

class Coupon:
    def __init__(self, code, discount, conditions, expiry_date):
        self.code = code
        self.discount = discount
        self.conditions = conditions
        self.expiry_date = expiry_date

    def is_valid(self, cart):
        if datetime.now() > self.expiry_date:
            return False
        # Check conditions
        for condition in self.conditions:
            if not condition.is_satisfied(cart):
                return False
        return True

    def apply_discount(self, total_amount):
        return total_amount - self.discount

class CouponManager:
    def __init__(self):
        self.coupons = []

    def generate_coupon(self, discount, conditions, expiry_days):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expiry_date = datetime.now() + timedelta(days=expiry_days)
        coupon = Coupon(code, discount, conditions, expiry_date)
        self.coupons.append(coupon)
        return coupon

    def apply_coupon(self, cart, coupon_code):
        for coupon in self.coupons:
            if coupon.code == coupon_code:
                if coupon.is_valid(cart):
                    cart.total_amount = coupon.apply_discount(cart.total_amount)
                    return True
        return False

electronics = Category(1, "Electronics")
clothing = Category(2, "Clothing")

# Create products
laptop = Product(101, "Laptop", 1000, electronics)
shirt = Product(201, "Shirt", 50, clothing)

# Create a cart and add products
cart = Cart()
cart.add_product(laptop)
cart.add_product(shirt)

# Create conditions
product_condition = ProductCondition(101)
category_condition = CategoryCondition(2)
min_amount_condition = MinimumAmountCondition(500)

# Generate a coupon
coupon_manager = CouponManager()
coupon = coupon_manager.generate_coupon(100, [product_condition, category_condition, min_amount_condition], 30)

# Apply the coupon to the cart
success = coupon_manager.apply_coupon(cart, coupon.code)
if success:
    print(f"Coupon applied successfully! New total amount: {cart.get_total_amount()}")
else:
    print("Failed to apply coupon.")
