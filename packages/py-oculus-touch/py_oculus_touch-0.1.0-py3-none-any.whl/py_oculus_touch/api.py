import ctypes
from enum import Enum

DLL = ctypes.WinDLL("py_oculus_touch/lib/auto_oculus_touch.dll")


class OculusTouchButtonEnum(Enum):
    """Controller button enums. These buttons can be pushed down."""

    A = 0x00000001
    B = 0x00000002
    RThumb = 0x00000004
    RShoulder = 0x00000008
    X = 0x00000100
    Y = 0x00000200
    LThumb = 0x00000400
    LShoulder = 0x00000800
    Up = 0x00010000
    Down = 0x00020000
    Left = 0x00040000
    Right = 0x00080000
    Enter = 0x00100000
    Back = 0x00200000


class OculusTouchSensorEnum(Enum):
    """Controller capacitive sensor enums. These sensors can be touched."""

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


class OculusTouchGestureEnum(Enum):
    """Controller gesture enums. These hand gestures can be made with the controller."""

    RIndexPointing = 0x00000020
    RThumbUp = 0x00000040
    LIndexPointing = 0x00002000
    LThumbUp = 0x00004000


class OculusTouchControllerTypeEnum(Enum):
    """Controller type enums. These enums represent the type of controller."""

    LTouch = 0x0001
    RTouch = 0x0002
    XBox = 0x0010


class OculusTouchHandEnum(Enum):
    """Controller hand enums. These enums represent the hand the controller is in."""

    Left = 0
    Right = 1


class OculusTouchControllerEnum(Enum):
    """Controller enums. These enums represent the controller (which includes the headset too)."""

    Left = 0
    Right = 1
    Head = 2


class OculusTouchTriggerEnum(Enum):
    """Controller trigger enums. These enums represent the trigger type."""

    Index = 0
    Hand = 1


class OculusTouchVibrationFrequencyEnum(Enum):
    """Controller vibration frequency enums. These enums represent the preset vibration frequencies."""

    High = 1
    Medium = 2
    Low = 3
    VeryLow = 4


class OculusTouchTrackingOriginEnum(Enum):
    """Tracking origin enums. These enums represent the different tracking origins."""

    EyeLevel = 0
    FloorLevel = 1


class OculusTouchAxisEnum(Enum):
    """Controller axis enums. These enums represent the different axes on the controller."""

    IndexTriggerLeft = 0
    IndexTriggerRight = 1
    HandTriggerLeft = 2
    HandTriggerRight = 3
    XLeft = 4
    XRight = 5
    YLeft = 6
    YRight = 7


class OculusTouchvJoyDeviceEnum(Enum):
    """vJoy device enums. These enums represent the different vJoy buttons."""

    HIDUsageX = 0x30
    HIDUsageY = 0x31
    HIDUsageZ = 0x32
    HIDUsageRX = 0x33
    HIDUsageRY = 0x34
    HIDUsageRZ = 0x35
    HIDUsageSL0 = 0x36
    HIDUsageSL1 = 0x37
    HIDUsageWHL = 0x38
    HIDUsagePOV = 0x39


class OculusTouchRawMouseButtonEnum(Enum):
    """Raw mouse button enums. These enums represent the different mouse buttons."""

    Left = 0
    Right = 1
    Middle = 2


class OculusTouchMiscEnum(Enum):
    """Misc enums. These enums represent buttons that exist in the SDK, but can't be detected by user programs. You will never see or use them, but they are included here for completeness."""

    VolUp = 0x00400000
    VolDown = 0x00800000
    Home = 0x01000000


# Function prototypes
Func_initOculus = DLL.initOculus
Func_poll = DLL.poll
Func_isWearing = DLL.isWearing
Func_isPressed = DLL.isPressed
Func_isReleased = DLL.isReleased
Func_isDown = DLL.isDown
Func_isTouchPressed = DLL.isTouchPressed
Func_isTouchReleased = DLL.isTouchReleased
Func_isTouchDown = DLL.isTouchDown
Func_reached = DLL.reached
Func_getAxis = DLL.getAxis
Func_getButtonsDown = DLL.getButtonsDown
Func_getButtonsReleased = DLL.getButtonsReleased
Func_getButtonsPressed = DLL.getButtonsPressed
Func_getTouchDown = DLL.getTouchDown
Func_getTouchPressed = DLL.getTouchPressed
Func_getTouchReleased = DLL.getTouchReleased
Func_getTrigger = DLL.getTrigger
Func_getThumbStick = DLL.getThumbStick
Func_setVibration = DLL.setVibration
Func_getYaw = DLL.getYaw
Func_getPitch = DLL.getPitch
Func_getRoll = DLL.getRoll
Func_getPositionX = DLL.getPositionX
Func_getPositionY = DLL.getPositionY
Func_getPositionZ = DLL.getPositionZ
Func_setTrackingOrigin = DLL.setTrackingOrigin
Func_resetFacing = DLL.resetFacing
Func_initvJoy = DLL.initvJoy
Func_setvJoyAxis = DLL.setvJoyAxis
Func_setvJoyButton = DLL.setvJoyButton
Func_sendRawMouseMove = DLL.sendRawMouseMove
Func_sendRawMouseButtonDown = DLL.sendRawMouseButtonDown
Func_sendRawMouseButtonUp = DLL.sendRawMouseButtonUp

# Function argument types
Func_initOculus.argtypes = []
Func_poll.argtypes = []
Func_isWearing.argtypes = []
Func_isPressed.argtypes = [ctypes.c_uint]
Func_isReleased.argtypes = [ctypes.c_uint]
Func_isDown.argtypes = [ctypes.c_uint]
Func_isTouchPressed.argtypes = [ctypes.c_uint]
Func_isTouchReleased.argtypes = [ctypes.c_uint]
Func_isTouchDown.argtypes = [ctypes.c_uint]
Func_reached.argtypes = [ctypes.c_uint, ctypes.c_float]
Func_getAxis.argtypes = [ctypes.c_uint]
Func_getButtonsDown.argtypes = []
Func_getButtonsReleased.argtypes = []
Func_getButtonsPressed.argtypes = []
Func_getTouchDown.argtypes = []
Func_getTouchPressed.argtypes = []
Func_getTouchReleased.argtypes = []
Func_getTrigger.argtypes = [ctypes.c_int, ctypes.c_int]
Func_getThumbStick.argtypes = [ctypes.c_int, ctypes.c_int]
Func_setVibration.argtypes = [
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_ubyte,
    ctypes.c_float,
]
Func_getYaw.argtypes = [ctypes.c_uint]
Func_getPitch.argtypes = [ctypes.c_uint]
Func_getRoll.argtypes = [ctypes.c_uint]
Func_getPositionX.argtypes = [ctypes.c_uint]
Func_getPositionY.argtypes = [ctypes.c_uint]
Func_getPositionZ.argtypes = [ctypes.c_uint]
Func_setTrackingOrigin.argtypes = [ctypes.c_uint]
Func_resetFacing.argtypes = [ctypes.c_uint]
Func_initvJoy.argtypes = [ctypes.c_uint]
Func_setvJoyAxis.argtypes = [ctypes.c_float, ctypes.c_uint]
Func_setvJoyButton.argtypes = [ctypes.c_uint, ctypes.c_uint]
Func_sendRawMouseMove.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
Func_sendRawMouseButtonDown.argtypes = [ctypes.c_uint]
Func_sendRawMouseButtonUp.argtypes = [ctypes.c_uint]

# Function return types
Func_initOculus.restype = ctypes.c_int
Func_poll.restype = None
Func_isWearing.restype = ctypes.c_uint
Func_isPressed.restype = ctypes.c_uint
Func_isReleased.restype = ctypes.c_uint
Func_isDown.restype = ctypes.c_uint
Func_isTouchPressed.restype = ctypes.c_uint
Func_isTouchReleased.restype = ctypes.c_uint
Func_isTouchDown.restype = ctypes.c_uint
Func_reached.restype = ctypes.c_float
Func_getAxis.restype = ctypes.c_float
Func_getButtonsDown.restype = ctypes.c_uint
Func_getButtonsReleased.restype = ctypes.c_uint
Func_getButtonsPressed.restype = ctypes.c_uint
Func_getTouchDown.restype = ctypes.c_uint
Func_getTouchPressed.restype = ctypes.c_uint
Func_getTouchReleased.restype = ctypes.c_uint
Func_getTrigger.restype = ctypes.c_float
Func_getThumbStick.restype = ctypes.c_float
Func_setVibration.restype = None
Func_getYaw.restype = ctypes.c_float
Func_getPitch.restype = ctypes.c_float
Func_getRoll.restype = ctypes.c_float
Func_getPositionX.restype = ctypes.c_float
Func_getPositionY.restype = ctypes.c_float
Func_getPositionZ.restype = ctypes.c_float
Func_setTrackingOrigin.restype = None
Func_resetFacing.restype = None
Func_initvJoy.restype = ctypes.c_char_p
Func_setvJoyAxis.restype = None
Func_setvJoyButton.restype = None
Func_sendRawMouseMove.restype = None
Func_sendRawMouseButtonDown.restype = None
Func_sendRawMouseButtonUp.restype = None
