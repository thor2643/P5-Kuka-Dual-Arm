# rACT: Action request (activation bit).
# 0x0 - Decativate gripper.
# 0x1 - Activate gripper.

uint8 r_act


# rARD: Changes the gripper auto release direction.
# 0x0 - Closing.
# 0x1 - Opening.

uint8 r_ard


# rGTO: "Go To" action moves the gripper fingers to the requested position.
# 0x0 - Stop.
# 0x1 - Go to the requested position.

uint8 r_gto


# rATR: Automatic release routine.
# 0x0 - Stop.
# 0x1 Emergency auto-release.

uint8 r_atr


# rPR: Target position of the fingers.
# 0x00 Minimum position (open).
# 0xFF Maximum position (close).

uint8 r_pra


# rSP: Gripper closing or opening speed.
# Setting a speed will not initiate a motion.
# 0x00 Minimum speed.
# 0xFF Maximum speed.

uint8 r_spa


# rFR: Final grasping force of the gripper.
# Setting a force will not initiate a motion.
# 0x00 Minimum force.
# 0xFF Maximum force.

uint8 r_fra
