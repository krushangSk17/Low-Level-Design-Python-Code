"""
BLUEPRINT TO UNDERSTAND IT BETTER
LLD PARKING LOT SYSTEM

Classes:
1. Size (Enum): Enumerates the sizes of parking spots and vehicles.
   - Methods:
     - get(size): Converts a size string to a corresponding Enum value.

2. Vehicle: Represents vehicles that use the parking lot.
   - Attributes: id, numberplate, size, parked_spot

3. ParkingSpot: Represents individual parking spots within the lot.
   - Attributes: id, size, vehicle

4. ParkingLot: Manages the operations of parking vehicles.
   - Attributes: vehicleid, parkingspotid, parkingspots, vehicles, available_parking_spots
   - Methods:
     - create_spot(size): Creates a parking spot of a given size.
     - create_vehicle(numberplate, size): Creates a vehicle of a given size.
     - find_spot(vehicle): Finds an available parking spot for a vehicle based on its size.
     - park_vehicle(vehicle): Parks a vehicle in an appropriate spot.
     - remove_vehicle(vehicle): Removes a vehicle from its spot and makes the spot available again.

Usage:
- System initialization with counts of small, medium, and large spots.
- Vehicle creation with number plates and sizes.
- Vehicle parking and removal from the lot.
- Error handling for full parking lot scenarios.
- Display parking lot status with spots and vehicle placements.
"""


from enum import Enum

class Size(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

    @staticmethod
    def get(size):
        if size.lower() == 'small':
            return Size.SMALL
        elif size.lower() == 'medium':
            return Size.MEDIUM
        elif size.lower() == 'large':
            return Size.LARGE
        raise ValueError(f'No size matching with "{size}"')

class Vehicle:
    def __init__(self, id, numberplate, size):
        self.id = id
        self.numberplate = numberplate
        self.size = Size.get(size)
        self.parked_spot = None

class ParkingSpot:
    def __init__(self, id, size):
        self.id = id
        self.size = Size.get(size)
        self.vehicle = None

    def is_available(self):
        return self.vehicle is None

class ParkingLot:
    def __init__(self, small_count, medium_count, large_count):
        self.vehicleid = 0
        self.parkingspotid = 0
        self.parkingspots = []
        self.vehicles = {}
        self.available_parking_spots = [[], [], []]

        for _ in range(small_count):
            self.create_spot('small')
        for _ in range(medium_count):
            self.create_spot('medium')
        for _ in range(large_count):
            self.create_spot('large')

    def create_spot(self, size):
        p = ParkingSpot(self.parkingspotid, size)
        self.parkingspots.append(p)
        self.available_parking_spots[Size.get(size).value].append(p)
        self.parkingspotid += 1

    def create_vehicle(self, numberplate, size):
        v = Vehicle(self.vehicleid, numberplate, size)
        self.vehicles[v.id] = v
        self.vehicleid += 1
        return v

    def find_spot(self, vehicle):
        try:
            for i in range(vehicle.size.value, 3):
                if self.available_parking_spots[i]:
                    parking_spot = self.available_parking_spots[i].pop()
                    return parking_spot
            raise Exception('Compatible parking spot is not available')
        except Exception as e:
            print(f"Error: {e}")

    def park_vehicle(self, vehicle):
        spot = self.find_spot(vehicle)
        if spot:
            vehicle.parked_spot = spot
            spot.vehicle = vehicle

    def remove_vehicle(self, vehicle):
        if vehicle.parked_spot and vehicle.parked_spot.vehicle == vehicle:
            spot = vehicle.parked_spot
            spot.vehicle = None
            vehicle.parked_spot = None
            self.available_parking_spots[spot.size.value].append(spot)
            del self.vehicles[vehicle.id]
        else:
            raise Exception('Vehicle is not in a parking spot')

def main():
    # Initialize the parking lot with 2 of each spot size
    parking_lot = ParkingLot(small_count=2, medium_count=2, large_count=2)

    # Create vehicles of different sizes
    vehicle1 = parking_lot.create_vehicle('ABC123', 'small')
    vehicle2 = parking_lot.create_vehicle('XYZ456', 'medium')
    vehicle3 = parking_lot.create_vehicle('DEF789', 'large')
    vehicle4 = parking_lot.create_vehicle('GHI012', 'large')

    # Park the vehicles
    parking_lot.park_vehicle(vehicle1)
    parking_lot.park_vehicle(vehicle2)
    parking_lot.park_vehicle(vehicle3)
    parking_lot.park_vehicle(vehicle4)

    # Display parking info
    print(f'Vehicle {vehicle1.numberplate} parked at spot ID {vehicle1.parked_spot.id}')
    print(f'Vehicle {vehicle2.numberplate} parked at spot ID {vehicle2.parked_spot.id}')
    print(f'Vehicle {vehicle3.numberplate} parked at spot ID {vehicle3.parked_spot.id}')
    print(f'Vehicle {vehicle4.numberplate} parked at spot ID {vehicle4.parked_spot.id}')

    # Attempt to park another vehicle when the lot is full
    vehicle5 = parking_lot.create_vehicle('JKL345', 'large')
    parking_lot.park_vehicle(vehicle5)
    

    # Remove a vehicle and try to park another one
    parking_lot.remove_vehicle(vehicle3)
    parking_lot.park_vehicle(vehicle5)
    print(f'After removing, vehicle {vehicle5.numberplate} parked at spot ID {vehicle5.parked_spot.id}')

    # Display the status of parking spots
    print("Status of parking spots after operations:")
    for spot in parking_lot.parkingspots:
        status = 'available' if spot.is_available() else f'occupied by {spot.vehicle.numberplate}'
        print(f'Spot ID {spot.id}, Size {spot.size.name}, Status: {status}')


if __name__ == '__main__':
    main()