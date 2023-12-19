from py_oculus_touch.api import *
from time import sleep


class OculusTouch:
    def __init__(self, init: bool = True) -> None:
        """
        Initializes the Oculus Touch API. If `init` is set to False, you must call `InitOculus()` yourself.
        """
        if init:
            self.InitOculus()

    def InitOculus(self) -> int:
        """
        Initializes the Oculus Touch API. Need to investigate return codes.
        """
        return Func_initOculus()

    def Poll(self) -> int:
        """
        Polls the Oculus Touch API for state updates.
        """
        return Func_poll()

    def Sleep(self, length: float = 0.1) -> None:
        """
        Calls `time.sleep()` with a default value of 0.1 seconds.
        """
        return sleep(length)

    def PollAndSleep(self, length: float = 0.1) -> None:
        """
        Combines the `Poll()` and `Sleep()` functions.
        """
        self.Poll()
        return self.Sleep(length)

    def Wearing(self) -> bool:
        """
        Returns True if the user is wearing the headset, False otherwise. This is determined by the headset's proximity sensor.
        """
        return Func_isWearing() != 0

    def IsPressed(self, button: OculusTouchButtonEnum) -> bool:
        """
        Returns True if the specified button was first pressed in the current poll. The button must be a member of the `OculusTouchButtonEnum` class. As an example, you can pass the A button by doing `OculusTouchButtonEnum.A`.
        """
        return Func_isPressed(button.value) != 0

    def IsReleased(self, button: OculusTouchButtonEnum) -> bool:
        """
        Returns True if the specified button was released in the current poll. The button must be a member of the `OculusTouchButtonEnum` class. As an example, you can pass the A button by doing `OculusTouchButtonEnum.A`.
        """
        return Func_isReleased(button.value) != 0

    def isDown(self, button: OculusTouchButtonEnum) -> bool:
        """
        Returns True if the specified button is currently held down. The button must be a member of the `OculusTouchButtonEnum` class. As an example, you can pass the A button by doing `OculusTouchButtonEnum.A`.
        """
        return Func_isDown(button.value) != 0

    def IsTouchPressed(self, button: OculusTouchButtonEnum) -> bool:
        """
        Returns True if the specified button's capacitor was first touched in the current poll. The button must be a member of the `OculusTouchButtonEnum` class. As an example, you can pass the A button by doing `OculusTouchButtonEnum.A`.
        """
        return Func_isTouchPressed(button.value) != 0

    def IsTouchReleased(self, button: OculusTouchButtonEnum) -> bool:
        """
        Returns True if the specified button's capacitor was released in the current poll. The button must be a member of the `OculusTouchButtonEnum` class. As an example, you can pass the A button by doing `OculusTouchButtonEnum.A`.
        """
        return Func_isTouchReleased(button.value) != 0

    def IsTouchDown(self, button: OculusTouchButtonEnum) -> bool:
        """
        Returns True if the specified button's capacitor is currently being touched. The button must be a member of the `OculusTouchButtonEnum` class. As an example, you can pass the A button by doing `OculusTouchButtonEnum.A`.
        """
        return Func_isTouchDown(button.value) != 0

    def Reached(self, axis: OculusTouchAxisEnum, value: float) -> int:
        return Func_reached(axis.value, value)

    def GetAxis(self, axis: OculusTouchAxisEnum) -> float:
        return Func_getAxis(axis.value)

    def GetButtonsDown(self) -> int:
        """
        Returns a bitmask of all buttons currently held down. Query this with the `OculusTouchButtonEnum` class to determine which buttons are down. As an example, you can check if the A button is down by doing `OculusTouchButtonEnum.A & GetButtonsDown() != 0`.
        """
        return Func_getButtonsDown()

    def GetButtonsDownList(self) -> list[OculusTouchButtonEnum]:
        """
        Returns a list of all buttons currently held down. Query this with the `OculusTouchButtonEnum` class to determine which buttons are down. As an example, you can check if the A button is down by doing `OculusTouchButtonEnum.A in GetButtonsDownList()`.
        """
        down = self.GetButtonsDown()
        return [button for button in OculusTouchButtonEnum if down & button.value]

    def GetButtonsReleased(self) -> int:
        """
        Returns a bitmask of all buttons released in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were released. As an example, you can check if the A button was released by doing `OculusTouchButtonEnum.A & GetButtonsReleased() != 0`.
        """
        return Func_getButtonsReleased()

    def GetButtonsReleasedList(self) -> list[OculusTouchButtonEnum]:
        """
        Returns a list of all buttons released in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were released. As an example, you can check if the A button was released by doing `OculusTouchButtonEnum.A in GetButtonsReleasedList()`.
        """
        released = self.GetButtonsReleased()
        return [button for button in OculusTouchButtonEnum if released & button.value]

    def GetButtonsPressed(self) -> int:
        """
        Returns a bitmask of all buttons pressed in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were pressed. As an example, you can check if the A button was pressed by doing `OculusTouchButtonEnum.A & GetButtonsPressed() != 0`.
        """
        return Func_getButtonsPressed()

    def GetButtonsPressedList(self) -> list[OculusTouchButtonEnum]:
        """
        Returns a list of all buttons pressed in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were pressed. As an example, you can check if the A button was pressed by doing `OculusTouchButtonEnum.A in GetButtonsPressedList()`.
        """
        pressed = self.GetButtonsPressed()
        return [button for button in OculusTouchButtonEnum if pressed & button.value]

    def GetTouchDown(self) -> int:
        """
        Returns a bitmask of all buttons currently being touched. Query this with the `OculusTouchButtonEnum` class to determine which buttons are being touched. As an example, you can check if the A button is being touched by doing `OculusTouchButtonEnum.A & GetTouchDown() != 0`.
        """
        return Func_getTouchDown()

    def GetTouchDownList(self) -> list[OculusTouchButtonEnum]:
        """
        Returns a list of all buttons currently being touched. Query this with the `OculusTouchButtonEnum` class to determine which buttons are being touched. As an example, you can check if the A button is being touched by doing `OculusTouchButtonEnum.A in GetTouchDownList()`.
        """
        down = self.GetTouchDown()
        return [button for button in OculusTouchButtonEnum if down & button.value]

    def GetTouchPressed(self) -> int:
        """
        Returns a bitmask of all buttons whose capacitors were first touched in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were first touched. As an example, you can check if the A button was first touched by doing `OculusTouchButtonEnum.A & GetTouchPressed() != 0`.
        """
        return Func_getTouchPressed()

    def GetTouchPressedList(self) -> list[OculusTouchButtonEnum]:
        """
        Returns a list of all buttons whose capacitors were first touched in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were first touched. As an example, you can check if the A button was first touched by doing `OculusTouchButtonEnum.A in GetTouchPressedList()`.
        """
        pressed = self.GetTouchPressed()
        return [button for button in OculusTouchButtonEnum if pressed & button.value]

    def GetTouchReleased(self) -> int:
        """
        Returns a bitmask of all buttons whose capacitors were released in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were released. As an example, you can check if the A button was released by doing `OculusTouchButtonEnum.A & GetTouchReleased() != 0`.
        """
        return Func_getTouchReleased()

    def GetTouchReleasedList(self) -> list[OculusTouchButtonEnum]:
        """
        Returns a list of all buttons whose capacitors were released in the current poll. Query this with the `OculusTouchButtonEnum` class to determine which buttons were released. As an example, you can check if the A button was released by doing `OculusTouchButtonEnum.A in GetTouchReleasedList()`.
        """
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
