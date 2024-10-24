# gACT : Initialization status, echo of the rACT bit (activation bit).
# 0x0 - Gripper reset.
# 0x1 - Gripper activation.

uint8 g_act

# gGTO : Action status. echo of the rGTO bit (go to bit).
# 0x0 - Stopped (or performing activation / grasping mode change / automatic release)
# 0x1 - Go to Position Request

uint8 g_gto

# gSTA : Motion status, returns the current motion of the Gripper fingers.
# 0x00 - Gripper is in reset
# 0x01 - Activation in progress
# 0x02 - NOT USED
# 0x03 - Activation complete

uint8 g_sta

# gOBJ : Object detection status, information on possible object pickup, ignore if == 0
# 0x00 - Gripper is in motion, no object detected
# 0x01 - Gripper has stopped, contact while opening before requested position
# 0x02 - Gripper has stopped, due to contact while closing, before request position
# 0x03 - Gripper is at request position, no contact with object

uint8 g_obj


# gPRA : Echo of the requested position of the Gripper (rPRA),
# 0x00 is minimum position (full opening) and
# 0xFF is maximum position (full closing).

uint8 g_pr


# gPO : Actual position of the gripper
# 0x00 - Fully opened
# 0xFF - Fully closed

uint8 g_po

# gCU : Current (Measured as 10 * value = mA)
# 0x00 - No current
# 0xFF - Max Current

uint8 g_cu
