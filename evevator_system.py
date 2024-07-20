"""

BLUE PRINT TO UNDERSTAND IT BETTER
LLD ELEVATOR SYSTEM

Classes:
1. Direction (Enum): Represents the direction of the elevator.
   - Values: UP = 1, DOWN = 2

2. Request: Represents a request made by a user to use the elevator.
   - Attributes: source_floor, destination_floor

3. Elevator: Represents an elevator that processes user requests.
   - Attributes: id, capacity, current_floor, current_direction, requests (list of Request)
   - Methods: add_request(request), process_requests(), process_request(request), move_to_floor(target_floor)

4. ElevatorController: Manages multiple elevators and assigns requests to the optimal elevator.
   - Attributes: elevators (list of Elevator)
   - Methods: request_elevator(source_floor, destination_floor), find_optimal_elevator(source_floor)

Usage:
- System initialization with a specified number of elevators and their capacity.
- Adding requests to the system to move from a source floor to a destination floor.
- Elevators process the requests in a sequential manner.
- The controller assigns requests to the optimal elevator based on the current floor of each elevator.

"""

from enum import Enum
import time

class Direction(Enum):
    UP = 1
    DOWN = 2

class Request:
    def __init__(self, source_floor, destination_floor):
        self.source_floor = source_floor
        self.destination_floor = destination_floor

class Elevator:
    def __init__(self, id: int, capacity: int):
        self.id = id
        self.capacity = capacity
        self.current_floor = 1
        self.current_direction = Direction.UP
        self.requests = []

    def add_request(self, request: Request):
        if len(self.requests) < self.capacity:
            self.requests.append(request)
            print(f"Elevator {self.id} added request: {request.source_floor} to {request.destination_floor}")

    def process_requests(self):
        while self.requests:
            request = self.requests.pop(0)

            # self.process_request(request)
            print(f"Elevator {self.id} processing request from {request.source_floor} to {request.destination_floor}")

            # Move to source floor
            self.move_to_floor(request.source_floor)
            
            # Move to destination floor
            self.move_to_floor(request.destination_floor)

    def process_request(self, request: Request):
        print(f"Elevator {self.id} processing request from {request.source_floor} to {request.destination_floor}")

        # Move to source floor
        self.move_to_floor(request.source_floor)
        
        # Move to destination floor
        self.move_to_floor(request.destination_floor)

    def move_to_floor(self, target_floor: int):
        while self.current_floor != target_floor:
            if self.current_floor < target_floor:
                self.current_floor += 1
                self.current_direction = Direction.UP
            else:
                self.current_floor -= 1
                self.current_direction = Direction.DOWN
            print(f"Elevator {self.id} reached floor {self.current_floor}")
            time.sleep(1)  # Simulate time to move between floors

class ElevatorController:
    def __init__(self, num_elevators: int, capacity: int):
        self.elevators = [Elevator(i + 1, capacity) for i in range(num_elevators)]

    def request_elevator(self, source_floor: int, destination_floor: int):
        optimal_elevator = self.find_optimal_elevator(source_floor)
        optimal_elevator.add_request(Request(source_floor, destination_floor))
        optimal_elevator.process_requests()

    def find_optimal_elevator(self, source_floor: int) -> Elevator:
        return min(self.elevators, key=lambda e: abs(e.current_floor - source_floor))

class ElevatorSystemDemo:
    @staticmethod
    def run():
        controller = ElevatorController(3, 5)
        controller.request_elevator(5, 10)
        controller.request_elevator(3, 7)
        controller.request_elevator(8, 2)
        controller.request_elevator(1, 9)

        print("All requests have been processed.")

if __name__ == "__main__":
    ElevatorSystemDemo.run()
