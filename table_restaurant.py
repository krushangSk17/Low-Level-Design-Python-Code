from enum import Enum

class TableSize(Enum):
    SMALL = 2
    MEDIUM = 3
    LARGE = 4

class TimeSlot(Enum):
    FIRST = 1  # 6:30 PM to 8:00 PM
    SECOND = 2 # 8:00 PM to 9:30 PM
    THIRD = 3  # 9:30 PM to 11:00 PM


class Table:
    def __init__(self, table_id, size):
        self.table_id = table_id
        self.size = size
        self.reservations = {}  # Dictionary to manage reservations by date and slot

    def is_available(self, date, slot):
        if date in self.reservations:
            return slot not in self.reservations[date]
        return True

    def book_slot(self, date, slot):
        if date not in self.reservations:
            self.reservations[date] = set()
        self.reservations[date].add(slot)

    def free_slot(self, date, slot):
        if date in self.reservations and slot in self.reservations[date]:
            self.reservations[date].remove(slot)
            if not self.reservations[date]:  # Remove the date if no slots are booked
                del self.reservations[date]

    def __str__(self):
        return f"Table ID: {self.table_id}, Size: {self.size}, Reservations: {self.reservations}"


class ReservationManager:
    def __init__(self):
        self.tables = []
        self.reservations = {}

    def create_table(self, size, quantity):
        for _ in range(quantity):
            new_table = Table(size=size)
            self.tables.append(new_table)

    def find_available_table(self, party_size, date, slot):
        tables_sorted = sorted([table for table in self.tables if table.size >= party_size],
                                key=lambda x: x.size)
        for table in tables_sorted:
            if table.is_available(date, slot):
                return table
        return None

    def book_table(self, party_size, date, slot):
        table = self.find_available_table(party_size, date, slot)
        if table:
            new_reservation = Reservation(table=table, date=date, slot=slot, party_size=party_size)
            table.book_slot(date, slot)
            if date not in self.reservations:
                self.reservations[date] = []
            self.reservations[date].append(new_reservation)
            return new_reservation
        else:
            return "No available table."

    def cancel_reservation(self, reservation_id):
        for date, reservations in self.reservations.items():
            for reservation in reservations:
                if reservation.reservation_id == reservation_id:
                    reservation.table.free_slot(reservation.date, reservation.slot)
                    reservations.remove(reservation)
                    return "Reservation cancelled."
        return "Reservation not found."
