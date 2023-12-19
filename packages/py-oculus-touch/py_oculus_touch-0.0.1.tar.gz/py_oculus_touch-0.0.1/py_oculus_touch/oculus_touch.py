from py_oculus_touch.api import *
from time import sleep


class OculusTouch:
    def __init__(self, init: bool = True) -> None:
        if init:
            self.InitOculus()

    def InitOculus(self) -> int:
        return Func_initOculus()

    def Poll(self) -> int:
        return Func_poll()

    def Sleep(self, length: float = 0.1) -> None:
        return sleep(length)

    def PollAndSleep(self, length: float = 0.1) -> None:
        self.Poll()
        return self.Sleep(length)

    def Wearing(self) -> bool:
        return Func_isWearing() != 0

    def IsPressed(self, button: OculusTouchButtonEnum) -> bool:
        return Func_isPressed(button.value) != 0

    def IsReleased(self, button: OculusTouchButtonEnum) -> bool:
        return Func_isReleased(button.value) != 0

    def isDown(self, button: OculusTouchButtonEnum) -> bool:
        return Func_isDown(button.value) != 0

    def IsTouchPressed(self, button: OculusTouchButtonEnum) -> bool:
        return Func_isTouchPressed(button.value) != 0

    def IsTouchReleased(self, button: OculusTouchButtonEnum) -> bool:
        return Func_isTouchReleased(button.value) != 0

    def IsTouchDown(self, button: OculusTouchButtonEnum) -> bool:
        return Func_isTouchDown(button.value) != 0

    def Reached(self, axis: OculusTouchAxisEnum, value: float) -> int:
        return Func_reached(axis.value, value)

    def GetAxis(self, axis: OculusTouchAxisEnum) -> float:
        return Func_getAxis(axis.value)

    def GetButtonsDown(self) -> int:
        return Func_getButtonsDown()

    def GetButtonsDownList(self) -> list[OculusTouchButtonEnum]:
        down = self.GetButtonsDown()
        return [button for button in OculusTouchButtonEnum if down & button.value]

    def GetButtonsReleased(self) -> int:
        return Func_getButtonsReleased()

    def GetButtonsReleasedList(self) -> list[OculusTouchButtonEnum]:
        released = self.GetButtonsReleased()
        return [button for button in OculusTouchButtonEnum if released & button.value]

    def GetButtonsPressed(self) -> int:
        return Func_getButtonsPressed()

    def GetButtonsPressedList(self) -> list[OculusTouchButtonEnum]:
        pressed = self.GetButtonsPressed()
        return [button for button in OculusTouchButtonEnum if pressed & button.value]

    def GetTouchDown(self) -> int:
        return Func_getTouchDown()

    def GetTouchDownList(self) -> list[OculusTouchButtonEnum]:
        down = self.GetTouchDown()
        return [button for button in OculusTouchButtonEnum if down & button.value]

    def GetTouchPressed(self) -> int:
        return Func_getTouchPressed()

    def GetTouchPressedList(self) -> list[OculusTouchButtonEnum]:
        pressed = self.GetTouchPressed()
        return [button for button in OculusTouchButtonEnum if pressed & button.value]

    def GetTouchReleased(self) -> int:
        return Func_getTouchReleased()

    def GetTouchReleasedList(self) -> list[OculusTouchButtonEnum]:
        released = self.GetTouchReleased()
        return [button for button in OculusTouchButtonEnum if released & button.value]

    def GetTrigger(self, hand: int, trigger: int) -> float:
        return Func_getTrigger(hand, trigger)

    def GetThumbStick(self, hand: int, axis: OculusTouchAxisEnum) -> float:
        return Func_getThumbStick(hand, axis.value)

    def Vibrate(
        self, controller: int, frequency: int, amplitude: int, length: float
    ) -> None:
        return Func_setVibration(controller, frequency, amplitude, length)

    def GetYaw(self, controller: int) -> float:
        return Func_getYaw(controller)

    def GetPitch(self, controller: int) -> float:
        return Func_getPitch(controller)

    def GetRoll(self, controller: int) -> float:
        return Func_getRoll(controller)

    def GetPositionX(self, controller: int) -> float:
        return Func_getPositionX(controller)

    def GetPositionY(self, controller: int) -> float:
        return Func_getPositionY(controller)

    def GetPositionZ(self, controller: int) -> float:
        return Func_getPositionZ(controller)

    def SetTrackingOrigin(self, origin: OculusTouchTrackingOriginEnum) -> None:
        return Func_setTrackingOrigin(origin.value)

    def ResetFacing(self, controller: int) -> None:
        return Func_resetFacing(controller)

    def InitvJoy(self, device: int) -> None:
        result: str = Func_initvJoy(device)
        if len(result) > 0:
            raise Exception(result)

    def SetvJoyAxis(self, axis: OculusTouchAxisEnum, value: float) -> None:
        return Func_setvJoyAxis(value, axis.value)

    def SetvJoyAxisU(self, axis: OculusTouchAxisEnum, value: float) -> None:
        return Func_setvJoyAxis(value * 2 - 1, axis.value)

    def SetvJoyButton(self, button: OculusTouchButtonEnum, value: int) -> None:
        return Func_setvJoyButton(value, button.value)

    def SendRawMouseMove(self, x: int, y: int, z: int) -> None:
        return Func_sendRawMouseMove(x, y, z)

    def SendRawMouseButtonDown(self, button: OculusTouchButtonEnum) -> None:
        return Func_sendRawMouseButtonDown(button.value)

    def SendRawMouseButtonUp(self, button: OculusTouchButtonEnum) -> None:
        return Func_sendRawMouseButtonUp(button.value)
