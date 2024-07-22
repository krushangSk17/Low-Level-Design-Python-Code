"""
[Enum] ControllerType
---------------------
- XBOX: 'Xbox' - PLAYSTATION: 'PlayStation' - GENERIC: 'Generic'

[Class] Button
--------------
- name: str- pressed: bool
--------------
+ __init__(name: str) + press() + release()

[Class] Joystick
----------------
- name: str- x: int- y: int
----------------
+ __init__(name: str) + move(x: int, y: int)

[Class] UniversalController
---------------------------
- controller_type: ControllerType - buttons: Dict[str, Button] - joysticks: Dict[str, Joystick]
---------------------------
+ __init__(controller_type: ControllerType) + create_standard_controls() + press_button(button_name: str) + release_button(button_name: str)
+ move_joystick(joystick_name: str, x: int, y: int)

[Class] ConsoleConnector
------------------------
- console_type: ControllerType
------------------------
+ __init__(console_type: ControllerType) + connect()
+ send_input(input_data: Dict[str, any])

[Class] InputMapper
-------------------
(Static Methods)
-------------------
+ map_to_console_format(controller: UniversalController) -> Dict[str, any]

"""


from enum import Enum
from typing import List, Dict

class ControllerType(Enum):
    XBOX = 'Xbox'
    PLAYSTATION = 'PlayStation'
    GENERIC = 'Generic'

class Button:
    def __init__(self, name: str):
        self.name = name
        self.pressed = False

    def press(self):
        self.pressed = True

    def release(self):
        self.pressed = False

class Joystick:
    def __init__(self, name: str):
        self.name = name
        self.x = 0
        self.y = 0

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

class UniversalController:
    def __init__(self, controller_type: ControllerType):
        self.controller_type = controller_type
        self.buttons: Dict[str, Button] = {}
        self.joysticks: Dict[str, Joystick] = {}
        self.create_standard_controls()

    def create_standard_controls(self):
        standard_buttons = ['A', 'B', 'X', 'Y', 'Start', 'Select']
        standard_joysticks = ['Left', 'Right']
        for name in standard_buttons:
            self.buttons[name] = Button(name)
        for name in standard_joysticks:
            self.joysticks[name] = Joystick(name)

    def press_button(self, button_name: str):
        if button_name in self.buttons:
            self.buttons[button_name].press()

    def release_button(self, button_name: str):
        if button_name in self.buttons:
            self.buttons[button_name].release()

    def move_joystick(self, joystick_name: str, x: int, y: int):
        if joystick_name in self.joysticks:
            self.joysticks[joystick_name].move(x, y)

class ConsoleConnector:
    def __init__(self, console_type: ControllerType):
        self.console_type = console_type

    def connect(self):
        # Simulate connection logic
        print(f"Connected to {self.console_type.value} console")

    def send_input(self, input_data: Dict[str, any]):
        # Simulate sending input data to the console
        print(f"Sending input to {self.console_type.value} console: {input_data}")

class InputMapper:
    @staticmethod
    def map_to_console_format(controller: UniversalController) -> Dict[str, any]:
        # Map the universal controller inputs to a format that the console understands
        mapped_input = {}
        for button_name, button in controller.buttons.items():
            mapped_input[button_name] = button.pressed
        for joystick_name, joystick in controller.joysticks.items():
            mapped_input[joystick_name] = {'x': joystick.x, 'y': joystick.y}
        return mapped_input

# Example usage
def main():
    # Create a universal controller and a console connector
    universal_controller = UniversalController(ControllerType.GENERIC)
    console_connector = ConsoleConnector(ControllerType.XBOX)
    
    # Connect to the console
    console_connector.connect()
    
    # Simulate some controller actions
    universal_controller.press_button('A')
    universal_controller.move_joystick('Left', 10, -5)
    
    # Map the inputs and send to the console
    mapped_input = InputMapper.map_to_console_format(universal_controller)
    console_connector.send_input(mapped_input)
    
    # Release the button
    universal_controller.release_button('A')
    
    # Map the inputs and send to the console again
    mapped_input = InputMapper.map_to_console_format(universal_controller)
    console_connector.send_input(mapped_input)

if __name__ == "__main__":
    main()
