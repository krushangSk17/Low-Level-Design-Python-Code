class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

class Property:
    def __init__(self, property_id, host, title, description, location, price_per_night):
        self.property_id = property_id
        self.host = host
        self.title = title
        self.description = description
        self.location = location
        self.price_per_night = price_per_night

class Booking:
    def __init__(self, booking_id, property, guest, check_in_date, check_out_date):
        self.booking_id = booking_id
        self.property = property
        self.guest = guest
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_price = (self.check_out_date - self.check_in_date).days * self.property.price_per_night

class Review:
    def __init__(self, review_id, property, guest, rating, comment):
        self.review_id = review_id
        self.property = property
        self.guest = guest
        self.rating = rating
        self.comment = comment

class Payment:
    def __init__(self, payment_id, booking, amount):
        self.payment_id = payment_id
        self.booking = booking
        self.amount = amount
        self.status = 'pending'

    def process_payment(self):
        self.status = 'completed'

# Example Usage:
import datetime

# Define users
host = User(1, "Host Name", "host@example.com")
guest = User(2, "Guest Name", "guest@example.com")

# Define a property
property = Property(1, host, "Beach House", "A beautiful beach house.", "Seaside", 150)

# Create a booking
check_in_date = datetime.date(2024, 7, 1)
check_out_date = datetime.date(2024, 7, 5)
booking = Booking(1, property, guest, check_in_date, check_out_date)

# Post a review
review = Review(1, property, guest, 5, "Incredible location and great service!")

# Process a payment
payment = Payment(1, booking, booking.total_price)
payment.process_payment()

# Output
print(f"Booking total for {booking.total_price} made with status {payment.status}.")
