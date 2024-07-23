"""
### Restaurant Reservation System Blueprint

#### Classes:
1. **TableSize (Enum)**: Represents the size categories of tables.
   - Values: SMALL = 2, MEDIUM = 3, LARGE = 4

2. **TimeSlot (Enum)**: Represents different time intervals for reservations.
   - Values: FIRST = 1 (6:30 PM to 8:00 PM), SECOND = 2 (8:00 PM to 9:30 PM), THIRD = 3 (9:30 PM to 11:00 PM)

3. **Table**: Represents a single dining table in the restaurant.
   - Attributes: table_id, size (TableSize), reservations (defaultdict of sets)
   - Methods: is_available(date, slot), book_slot(date, slot), free_slot(date, slot)

4. **Reservation**: Represents a booking for a specific table at a specific time.
   - Attributes: reservation_id, table (Table), date, slot (TimeSlot), party_size
   - Auto-increments reservation_id for new reservations.

5. **ReservationManager**: Central system to manage all tables and reservations.
   - Attributes: tables (dict of lists, sorted by TableSize), reservations (dict), next_table_id
   - Methods: create_table(size, quantity), find_available_table(party_size, date, slot), book_table(party_size, date, slot), cancel_reservation(reservation_id)

#### Usage:
- **Initialization**: Start with creating an instance of `ReservationManager`.
- **Table Management**: Add tables of varying sizes to the system.
- **Reservation Handling**: 
  - Book tables by checking available sizes and time slots.
  - Automatically handle table assignments based on availability.
- **Modifications**:
  - Cancel reservations and update table availability accordingly.
- **Operations**:
  - Fetch details of all reservations and their statuses.
  - List all tables and their current reservation statuses.

  """

from enum import Enum
from collections import defaultdict

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
        self.reservations = defaultdict(set)

    def is_available(self, date, slot):
        return slot not in self.reservations[date]

    def book_slot(self, date, slot):
        if not self.is_available(date, slot):
            return False
        self.reservations[date].add(slot)
        return True

    def free_slot(self, date, slot):
        if slot in self.reservations[date]:
            self.reservations[date].remove(slot)
            if not self.reservations[date]:  # If no more reservations, delete the date key
                del self.reservations[date]
            return True
        return False

    def __str__(self):
        return f"Table ID: {self.table_id}, Size: {self.size}, Reservations: {self.reservations}"

class Reservation:
    _id_counter = 1

    def __init__(self, table, date, slot, party_size):
        self.reservation_id = Reservation._id_counter
        Reservation._id_counter += 1
        self.table = table
        self.date = date
        self.slot = slot
        self.party_size = party_size

    def __str__(self):
        return (f"Reservation ID: {self.reservation_id}, Table: {self.table.table_id}, "
                f"Date: {self.date}, Slot: {self.slot.name}, Party Size: {self.party_size}")

class ReservationManager:
    def __init__(self):
        self.tables = {size: [] for size in TableSize}
        self.reservations = {}
        self.next_table_id = 1

    def create_table(self, size, quantity):
        for _ in range(quantity):
            new_table = Table(table_id=self.next_table_id, size=size)
            self.tables[size].append(new_table)
            self.next_table_id += 1

    def find_available_table(self, party_size, date, slot):
        for size in TableSize:
            if size.value >= party_size:
                for table in self.tables[size]:
                    if table.is_available(date, slot):
                        return table
        return None

    def book_table(self, party_size, date, slot):
        table = self.find_available_table(party_size, date, slot)
        if table and table.book_slot(date, slot):
            new_reservation = Reservation(table=table, date=date, slot=slot, party_size=party_size)
            self.reservations.setdefault(date, []).append(new_reservation)
            return new_reservation
        return "No available table."

    def cancel_reservation(self, reservation_id):
        for date, reservations in self.reservations.items():
            for reservation in reservations:
                if reservation.reservation_id == reservation_id:
                    if reservation.table.free_slot(reservation.date, reservation.slot):
                        reservations.remove(reservation)
                        if not reservations:
                            del self.reservations[date]
                        return "Reservation cancelled."
        return "Reservation not found."

def main():
    manager = ReservationManager()
    manager.create_table(TableSize.SMALL, 2)  # Two small tables
    manager.create_table(TableSize.MEDIUM, 2)  # One medium table

    res1 = manager.book_table(2, '2023-07-22', TimeSlot.FIRST)
    res2 = manager.book_table(3, '2023-07-22', TimeSlot.FIRST)
    print(res1)
    print(res2)  # Should state no available table due to size constraints or slot availability

    print(manager.cancel_reservation(res1.reservation_id))
    res3 = manager.book_table(3, '2023-07-22', TimeSlot.FIRST)
    print(res3)  # Should now book successfully

if __name__ == "__main__":
    main()
