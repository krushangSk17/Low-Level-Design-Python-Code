"""
# 1 Amazon Cart discount and scalable (Self)

# Write code that will be used by a Shopping cart service to enforce rules on the order

# eg.
# Offer free 2 day shipping on orders > $35 if customer is not a prime member
# Offer free 2 day shipping on all orders if customer is a prime member
# Offer free 1 day shipping for orders > $125
# Offer free 2 hour shipping for prime customers with orders > $25 and the items are grocery items
# Make this extensible to add other rules in the future
# Apply a 10% discount if an item has been marked for subscribe and save

BLUEPRINT TO UNDERSTAND IT BETTER
LLD SHOPPING CART SERVICE WITH RULES

Classes:
1. Order: Represents an order placed by a customer.
   - Attributes: total, items, is_prime, is_groc, is_fav, discount, deltype
   - Methods: __init__(total, items, is_groc, is_fav, is_prime)

2. Rule (Abstract Class): Base class for different rules.
   - Methods: apply(order)

3. FreeTwoDayShippingRule: Applies free two-day shipping.
   - Inherits: Rule
   - Methods: apply(order)

4. FreeOneDayShippingRule: Applies free one-day shipping.
   - Inherits: Rule
   - Methods: apply(order)

5. FreeTwoHourShippingRule: Applies free two-hour shipping.
   - Inherits: Rule
   - Methods: apply(order)

6. SubscribeAndSaveDiscountRule: Applies subscribe and save discount.
   - Inherits: Rule
   - Methods: apply(order)

Usage:
- Create an Order object with necessary details.
- Create and apply rules to the Order object.
"""
from typing import List

class Order:
    def __init__(self, total: float, items: List[str], is_groc: bool, is_fav: bool, is_prime: bool = True) -> None:
        self.total = total
        self.items = items
        self.is_prime = is_prime
        self.is_groc = is_groc
        self.is_fav = is_fav
        self.discount = 0
        self.deltype = 'Regular'

class Rule:
    def apply(self, order: Order):
        raise NotImplementedError

class FreeTwoDayShippingRule(Rule):
    def apply(self, order: Order):
        if order.total > 35 or order.is_prime:
            order.deltype = 'two day'

class FreeOneDayShippingRule(Rule):
    def apply(self, order: Order):
        if order.total > 125:
            order.deltype = 'one day'

class FreeTwoHourShippingRule(Rule):
    def apply(self, order: Order):
        if order.total > 25 and order.is_groc:
            order.deltype = 'two hour'

class SubscribeAndSaveDiscountRule(Rule):
    def apply(self, order: Order):
        if order.is_fav:
            order.discount = 0.1 * order.total

# Example usage:
order = Order(total=150, items=['item1', 'item2'], is_groc=True, is_fav=True)

FreeTwoDayShippingRule().apply(order)
FreeOneDayShippingRule().apply(order)
FreeTwoHourShippingRule().apply(order)
SubscribeAndSaveDiscountRule().apply(order)

print(f"Order Total: {order.total}")
print(f"Items: {order.items}")
print(f"Is Prime Member: {order.is_prime}")
print(f"Is Grocery: {order.is_groc}")
print(f"Subscribe and Save: {order.is_fav}")
print(f"Shipping Type: {order.deltype}")
print(f"Discount: {order.discount}")
print(f"Total after Discount: {order.total - order.discount}")
