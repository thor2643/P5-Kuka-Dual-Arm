from Robotiq2F85Driver import Robotiq2F85Driver
from time import sleep
# from pathlib import Path

# t = Robotiq2F85Driver.LinuxFindTTYWithSerialNumber()
# print(t.get_serial_number(Path("/ttyUSB0")))


# Initialize the driver with the gripper's serial number
gripper = Robotiq2F85Driver(serial_number='DA8BRYE3')

# Reset the gripper
#gripper.reset()

# Move the gripper to fully open position (opening = 85 mm)
# The motion is done at 150 mm/s with a force of up to 235 Newtons.
sleep(2)
print("opening gripper")
gripper.go_to(opening=85, speed=150, force=235)
sleep(3)
print("closing gripper")
gripper.go_to(opening=32.37, speed=150, force=235)  # 32.37 to hold a lego

# Get the current gripper opening
print(gripper.opening)
