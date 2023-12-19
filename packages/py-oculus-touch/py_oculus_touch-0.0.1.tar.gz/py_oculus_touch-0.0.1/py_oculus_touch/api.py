import ctypes
from enum import Enum


# Button enums
class OculusTouchButtonEnum(Enum):
    A = 0x00000001  # Touch-A            Remote-None         Xbox-A
    B = 0x00000002  # Touch-B            Remote-None         Xbox-B
    RThumb = 0x00000004  # Touch-Right Stick  Remote-None         Xbox-Right Thumbstick
    RShoulder = 0x00000008  # Touch-None         Remote-None         Xbox-Right Shoulder
    X = 0x00000100  # Touch-X            Remote-None         Xbox-X
    Y = 0x00000200  # Touch-Y            Remote-None         Xbox-Y
    LThumb = 0x00000400  # Touch-Left Stick   Remote-None         Xbox-Left Thumbstick
    LShoulder = 0x00000800  # Touch-None         Remote-None         Xbox-Left Shoulder
    Up = 0x00010000  # Touch-None         Remote-Up           Xbox-Up
    Down = 0x00020000  # Touch-None         Remote-Down         Xbox-Down
    Left = 0x00040000  # Touch-None         Remote-Left         Xbox-Left
    Right = 0x00080000  # Touch-None         Remote-Right        Xbox-Right
    Enter = 0x00100000  # Touch-Left Menu    Remote-Select       Xbox-Start
    Back = 0x00200000  # Touch-None         Remote-Back         Xbox-Back


# Capacitive touch sensor enums
class OculusTouchSensorEnum(Enum):
    A = 0x00000001
    B = 0x00000002
    RThumb = 0x00000004
    RThumbRest = 0x00000008
    RIndexTrigger = 0x00000010
    X = 0x00000100
    Y = 0x00000200
    LThumb = 0x00000400
    LThumbRest = 0x00000800
    LIndexTrigger = 0x00001000


# Capacitive touch gesture enums
class OculusTouchGestureEnum(Enum):
    RIndexPointing = 0x00000020
    RThumbUp = 0x00000040
    LIndexPointing = 0x00002000
    LThumbUp = 0x00004000


# Controller types enums
class OculusTouchControllerTypeEnum(Enum):
    LTouch = 0x0001
    RTouch = 0x0002
    XBox = 0x0010


class OculusTouchMiscEnum(Enum):
    LeftHand = 0
    RightHand = 1
    Head = 2
    IndexTrigger = 0
    HandTrigger = 1
    XAxis = 0
    YAxis = 1
    LeftMouse = 0
    RightMouse = 1
    MiddleMouse = 2
    # The following button enums exist in the SDK, but the buttons can't be detected by user programs.
    # They are included here for completeness only, you will never see them.
    VolUp = 0x00400000  # Touch-None         Remote-Volume Up    Xbox-None
    VolDown = 0x00800000  # Touch-None         Remote-Volume Down  Xbox-None
    Home = 0x01000000  # Touch-Oculus       Remote-Oculus       Xbox-Home


# Tracking origin enums
class OculusTouchTrackingOriginEnum(Enum):
    EyeLevel = 0
    FloorLevel = 1


# Axis definition enums
class OculusTouchAxisEnum(Enum):
    IndexTriggerLeft = 0
    IndexTriggerRight = 1
    HandTriggerLeft = 2
    HandTriggerRight = 3
    XLeft = 4
    XRight = 5
    YLeft = 6
    YRight = 7


# vJoy definition enums
class OculusTouchvJoyDeviceEnum(Enum):
    HID_USAGE_X = 0x30  # Left gamepad thumbstick x
    HID_USAGE_Y = 0x31  # Left gamepad thumbstick y
    HID_USAGE_Z = 0x32  # Left gamepad trigger
    HID_USAGE_RX = 0x33  # Right gamepad thumbstick x
    HID_USAGE_RY = 0x34  # Right gamepad thumbstick y
    HID_USAGE_RZ = 0x35  # Right gamepad trigger
    HID_USAGE_SL0 = 0x36
    HID_USAGE_SL1 = 0x37
    HID_USAGE_WHL = 0x38
    HID_USAGE_POV = 0x39


# Grab the library.
oculus_touch_dll = ctypes.WinDLL("py_oculus_touch/lib/auto_oculus_touch.dll")

Func_initOculus = oculus_touch_dll.initOculus
Func_poll = oculus_touch_dll.poll
Func_isWearing = oculus_touch_dll.isWearing
Func_isPressed = oculus_touch_dll.isPressed
Func_isReleased = oculus_touch_dll.isReleased
Func_isDown = oculus_touch_dll.isDown
Func_isTouchPressed = oculus_touch_dll.isTouchPressed
Func_isTouchReleased = oculus_touch_dll.isTouchReleased
Func_isTouchDown = oculus_touch_dll.isTouchDown
Func_reached = oculus_touch_dll.reached
Func_getAxis = oculus_touch_dll.getAxis
Func_getButtonsDown = oculus_touch_dll.getButtonsDown
Func_getButtonsReleased = oculus_touch_dll.getButtonsReleased
Func_getButtonsPressed = oculus_touch_dll.getButtonsPressed
Func_getTouchDown = oculus_touch_dll.getTouchDown
Func_getTouchPressed = oculus_touch_dll.getTouchPressed
Func_getTouchReleased = oculus_touch_dll.getTouchReleased
Func_getTrigger = oculus_touch_dll.getTrigger
Func_getThumbStick = oculus_touch_dll.getThumbStick
Func_setVibration = oculus_touch_dll.setVibration
Func_getYaw = oculus_touch_dll.getYaw
Func_getPitch = oculus_touch_dll.getPitch
Func_getRoll = oculus_touch_dll.getRoll
Func_getPositionX = oculus_touch_dll.getPositionX
Func_getPositionY = oculus_touch_dll.getPositionY
Func_getPositionZ = oculus_touch_dll.getPositionZ
Func_setTrackingOrigin = oculus_touch_dll.setTrackingOrigin
Func_resetFacing = oculus_touch_dll.resetFacing
Func_initvJoy = oculus_touch_dll.initvJoy
Func_setvJoyAxis = oculus_touch_dll.setvJoyAxis
Func_setvJoyButton = oculus_touch_dll.setvJoyButton
Func_sendRawMouseMove = oculus_touch_dll.sendRawMouseMove
Func_sendRawMouseButtonDown = oculus_touch_dll.sendRawMouseButtonDown
Func_sendRawMouseButtonUp = oculus_touch_dll.sendRawMouseButtonUp
