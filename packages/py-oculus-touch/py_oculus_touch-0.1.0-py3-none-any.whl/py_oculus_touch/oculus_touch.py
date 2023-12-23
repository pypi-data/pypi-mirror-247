from py_oculus_touch.api import *
from time import sleep


class OculusTouch:
    def __init__(self, init: bool = True, poll: bool = True) -> None:
        """Initializes the Oculus Touch object.

        Args:
            init (bool, optional): If True, initializes the Oculus API. Defaults to True.
            poll (bool, optional): If True, polls the Oculus API after initializing. Defaults to True.
        """
        if init:
            self.InitOculus(poll=poll)

    def InitOculus(self, poll: bool = True) -> int:
        """Initializes the Oculus API.

        Args:
            poll (bool, optional): If True, polls the Oculus API after initializing. Defaults to True.

        Returns:
            int: Return code from the initialization process.
        """
        ret = Func_initOculus()
        if poll:
            self.Poll()
        return ret

    def Poll(self) -> int:
        """Polls the Oculus Touch API for state updates.

        Returns:
            int: Return code from the polling process.
        """
        return Func_poll()

    def Sleep(self, length: float = 0.1) -> None:
        """Blocks the runtime and waits for the specified length. Useful for sleeping between polls.

        Args:
            length (float, optional): Length of time to sleep in seconds. Defaults to 0.1.
        """
        return sleep(length)

    def PollAndSleep(self, length: float = 0.1) -> None:
        """Combines the `Poll()` and `Sleep()` functions.

        Args:
            length (float, optional): Length of time to sleep in seconds. Defaults to 0.1.
        """
        self.Poll()
        return self.Sleep(length)

    def Wearing(self) -> bool:
        """Checks if the user is wearing the headset.

        Returns:
            bool: True if the user is wearing the headset, False otherwise.
        """
        return Func_isWearing() != 0

    def IsPressed(self, button: OculusTouchButtonEnum) -> bool:
        """Checks if the specified button was pressed in the current poll. "Pressed" and "Down" are not the same thing.

        Args:
            button (OculusTouchButtonEnum): The button to check.

        Returns:
            bool: True if the button was pressed, False otherwise.
        """
        return Func_isPressed(button.value) != 0

    def IsReleased(self, button: OculusTouchButtonEnum) -> bool:
        """Checks if the specified button was released in the current poll.

        Args:
            button (OculusTouchButtonEnum): The button to check.

        Returns:
            bool: True if the button was released, False otherwise.
        """
        return Func_isReleased(button.value) != 0

    def IsDown(self, button: OculusTouchButtonEnum) -> bool:
        """Checks if the specified button is currently held down. "Pressed" and "Down" are not the same thing.

        Args:
            button (OculusTouchButtonEnum): The button to check.

        Returns:
            bool: True if the button is held down, False otherwise.
        """
        return Func_isDown(button.value) != 0

    def IsTouchPressed(self, sensor: OculusTouchSensorEnum) -> bool:
        """Checks if the specified button's capacitor was touched in the current poll. "Pressed" and "Down" are not the same thing.

        Args:
            button (OculusTouchButtonEnum): The button to check.

        Returns:
            bool: True if the button's capacitor was touched, False otherwise.
        """
        return Func_isTouchPressed(sensor.value) != 0

    def IsTouchReleased(self, sensor: OculusTouchSensorEnum) -> bool:
        """Checks if the specified button's capacitor was released in the current poll.

        Args:
            button (OculusTouchButtonEnum): The button to check.

        Returns:
            bool: True if the button's capacitor was released, False otherwise.
        """
        return Func_isTouchReleased(sensor.value) != 0

    def IsTouchDown(self, sensor: OculusTouchSensorEnum) -> bool:
        """Checks if the specified button's capacitor is currently being touched. "Pressed" and "Down" are not the same thing.

        Args:
            button (OculusTouchButtonEnum): The button to check.

        Returns:
            bool: True if the button's capacitor is being touched, False otherwise.
        """
        return Func_isTouchDown(sensor.value) != 0

    def Reached(self, axis: OculusTouchAxisEnum, value: float) -> int:
        """Checks whether a specified axis has reached a specified threshold value in between the last poll.

        Args:
            axis (OculusTouchAxisEnum): The axis to check.
            value (float): The threshold value to check against.

        Returns:
            int: Return code indicating if the axis has reached the threshold. 0 if the threshold wasn't crossed. 1 if the threshold was crossed in the positive direction. -1 if the threshold was crossed in the negative direction.
        """
        return Func_reached(axis.value, value)

    def GetAxis(self, axis: OculusTouchAxisEnum) -> float:
        """Returns the value of the specified axis.

        Args:
            axis (OculusTouchAxisEnum): The axis to query.

        Returns:
            float: The current value of the specified axis.
        """
        return Func_getAxis(axis.value)

    def GetButtonsDown(self) -> int:
        """Returns a bitmask of all buttons currently held down. "Pressed" and "Down" are not the same thing.

        Returns:
            int: Bitmask representing buttons currently held down.
        """
        return Func_getButtonsDown()

    def GetButtonsDownList(self) -> list[OculusTouchButtonEnum]:
        """Returns a list of all buttons currently held down. "Pressed" and "Down" are not the same thing.

        Returns:
            list[OculusTouchButtonEnum]: List of buttons currently held down.
        """
        down = self.GetButtonsDown()
        return [button for button in OculusTouchButtonEnum if down & button.value]

    def GetButtonsReleased(self) -> int:
        """Returns a bitmask of all buttons released in the current poll.

        Returns:
            int: Bitmask representing buttons released in the current poll.
        """
        return Func_getButtonsReleased()

    def GetButtonsReleasedList(self) -> list[OculusTouchButtonEnum]:
        """Returns a list of all buttons released in the current poll.

        Returns:
            list[OculusTouchButtonEnum]: List of buttons released in the current poll.
        """
        released = self.GetButtonsReleased()
        return [button for button in OculusTouchButtonEnum if released & button.value]

    def GetButtonsPressed(self) -> int:
        """Returns a bitmask of all buttons pressed in the current poll. "Pressed" and "Down" are not the same thing.

        Returns:
            int: Bitmask representing buttons pressed in the current poll.
        """
        return Func_getButtonsPressed()

    def GetButtonsPressedList(self) -> list[OculusTouchButtonEnum]:
        """Returns a list of all buttons pressed in the current poll. "Pressed" and "Down" are not the same thing.

        Returns:
            list[OculusTouchButtonEnum]: List of buttons pressed in the current poll.
        """
        pressed = self.GetButtonsPressed()
        return [button for button in OculusTouchButtonEnum if pressed & button.value]

    def GetTouchDown(self) -> int:
        """Returns a bitmask of all buttons currently being touched. "Pressed" and "Down" are not the same thing.

        Returns:
            int: Bitmask representing buttons currently being touched.
        """
        return Func_getTouchDown()

    def GetTouchDownList(self) -> list[OculusTouchSensorEnum]:
        """Returns a list of all buttons currently being touched. "Pressed" and "Down" are not the same thing.

        Returns:
            list[OculusTouchSensorEnum]: List of buttons currently being touched.
        """
        down = self.GetTouchDown()
        return [button for button in OculusTouchSensorEnum if down & button.value]

    def GetTouchPressed(self) -> int:
        """Returns a bitmask of all buttons whose capacitors were touched in the current poll. "Pressed" and "Down" are not the same thing.

        Returns:
            int: Bitmask representing buttons whose capacitors were touched.
        """
        return Func_getTouchPressed()

    def GetTouchPressedList(self) -> list[OculusTouchSensorEnum]:
        """Returns a list of all buttons whose capacitors were touched in the current poll. "Pressed" and "Down" are not the same thing.

        Returns:
            list[OculusTouchSensorEnum]: List of buttons whose capacitors were touched.
        """
        pressed = self.GetTouchPressed()
        return [button for button in OculusTouchSensorEnum if pressed & button.value]

    def GetTouchReleased(self) -> int:
        """Returns a bitmask of all buttons whose capacitors were released in the current poll.

        Returns:
            int: Bitmask representing buttons whose capacitors were released.
        """
        return Func_getTouchReleased()

    def GetTouchReleasedList(self) -> list[OculusTouchSensorEnum]:
        """Returns a list of all buttons whose capacitors were released in the current poll.

        Returns:
            list[OculusTouchSensorEnum]: List of buttons whose capacitors were released.
        """
        released = self.GetTouchReleased()
        return [button for button in OculusTouchSensorEnum if released & button.value]

    def GetTrigger(
        self, hand: OculusTouchHandEnum, trigger: OculusTouchTriggerEnum
    ) -> float:
        """Returns the value of a specified trigger.

        Args:
            hand (OculusTouchHandEnum): The hand (left or right) of the trigger.
            trigger (OculusTouchTriggerEnum): The trigger (index or hand) to query.

        Returns:
            float: The current value of the specified trigger.
        """
        return Func_getTrigger(hand, trigger)

    def GetThumbStick(
        self, hand: OculusTouchHandEnum, axis: OculusTouchAxisEnum
    ) -> float:
        """Returns the value of a specified thumbstick's axis.

        Args:
            hand (OculusTouchHandEnum): The hand (left or right) of the thumbstick.
            axis (OculusTouchAxisEnum): The axis (x or y) of the thumbstick to query.

        Returns:
            float: The current value of the specified thumbstick's axis.
        """
        return Func_getThumbStick(hand, axis.value)

    def Vibrate(
        self,
        controller: OculusTouchControllerEnum,
        frequency: OculusTouchVibrationFrequencyEnum = OculusTouchVibrationFrequencyEnum.Medium,
        amplitude: int = 128,
        length: float = 1.0,
    ) -> None:
        """Vibrates a specified controller.

        Args:
            controller (OculusTouchControllerEnum): The controller to vibrate.
            frequency (OculusTouchVibrationFrequencyEnum): The vibration frequency.
            amplitude (int): The amplitude of the vibration, range [0, 255].
            length (float): The length of vibration in seconds, 0 for infinite.

        Raises:
            ValueError: If the amplitude is not in the range [0, 255].
        """
        if amplitude < 0 or amplitude > 255:
            raise ValueError("The amplitude must be in the range [0, 255].")
        amplitude = ctypes.c_ubyte(amplitude)
        return Func_setVibration(controller.value, frequency.value, amplitude, length)

    def GetYaw(self, controller: OculusTouchControllerEnum) -> float:
        """Returns the yaw of a specified controller. Yaw is rotation around the y-axis.

        Args:
            controller (OculusTouchControllerEnum): The controller to query.

        Returns:
            float: The yaw (rotation around the y-axis) of the specified controller.
        """
        return Func_getYaw(controller.value)

    def GetPitch(self, controller: OculusTouchControllerEnum) -> float:
        """Returns the pitch of a specified controller. Pitch is rotation around the x-axis.

        Args:
            controller (OculusTouchControllerEnum): The controller to query.

        Returns:
            float: The pitch (rotation around the x-axis) of the specified controller.
        """
        return Func_getPitch(controller.value)

    def GetRoll(self, controller: OculusTouchControllerEnum) -> float:
        """Returns the roll of a specified controller. Roll is rotation around the z-axis.

        Args:
            controller (OculusTouchControllerEnum): The controller to query.

        Returns:
            float: The roll (rotation around the z-axis) of the specified controller.
        """
        return Func_getRoll(controller.value)

    def GetPositionX(self, controller: OculusTouchControllerEnum) -> float:
        """Returns the x position of a specified controller.

        Args:
            controller (OculusTouchControllerEnum): The controller to query.

        Returns:
            float: The x position of the specified controller.
        """
        return Func_getPositionX(controller.value)

    def GetPositionY(self, controller: OculusTouchControllerEnum) -> float:
        """Returns the y position of a specified controller.

        Args:
            controller (OculusTouchControllerEnum): The controller to query.

        Returns:
            float: The y position of the specified controller.
        """
        return Func_getPositionY(controller.value)

    def GetPositionZ(self, controller: OculusTouchControllerEnum) -> float:
        """Returns the z position of a specified controller.

        Args:
            controller (OculusTouchControllerEnum): The controller to query.

        Returns:
            float: The z position of the specified controller.
        """
        return Func_getPositionZ(controller.value)

    def SetTrackingOrigin(self, origin: OculusTouchTrackingOriginEnum) -> None:
        """Sets the tracking origin of the headset. This is the point in space that the headset will consider to be the origin (0, 0, 0).

        Args:
            origin (OculusTouchTrackingOriginEnum): The tracking origin to set.
        """
        return Func_setTrackingOrigin(origin.value)

    def ResetFacing(self, controller: OculusTouchControllerEnum) -> None:
        """Resets the yaw of a specified controller. Yaw is rotation around the y-axis.

        Args:
            controller (OculusTouchControllerEnum): The controller for which to reset the yaw.
        """
        return Func_resetFacing(controller.value)

    def InitvJoy(self, device: int) -> None:
        """Initializes the vJoy driver. This must be called before any vJoy functions can be used.

        Args:
            device (int): The vJoy device number to initialize.

        Raises:
            RuntimeError: If there is an error during initialization.

        """
        result: str = Func_initvJoy(device)
        if len(result) > 0:
            raise RuntimeError(result)

    def SetvJoyAxis(self, axis: OculusTouchvJoyDeviceEnum, value: float) -> None:
        """Sets the value of a specified vJoy axis.

        Args:
            axis (OculusTouchvJoyDeviceEnum): The vJoy axis to set.
            value (float): The value to set, range [0.0, 1.0].
        """
        return Func_setvJoyAxis(value, axis.value)

    def SetvJoyAxisU(self, axis: OculusTouchvJoyDeviceEnum, value: float) -> None:
        """Sets the value of a specified vJoy axis using a different range.

        Args:
            axis (OculusTouchvJoyDeviceEnum): The vJoy axis to set.
            value (float): The value to set, range [0.0, 1.0], mapped to [-1.0, 1.0].
        """
        return Func_setvJoyAxis(value * 2 - 1, axis.value)

    def SetvJoyButton(self, button: OculusTouchButtonEnum, value: int) -> None:
        """Sets the value of a specified vJoy button.

        Args:
            button (OculusTouchButtonEnum): The vJoy button to set.
            value (int): The value to set, range [0, 1].
        """
        return Func_setvJoyButton(value, button.value)

    def SendRawMouseMove(self, x: int, y: int, z: int) -> None:
        """Sends a raw mouse move event to the host computer.

        Args:
            x (int): The relative movement in the x direction.
            y (int): The relative movement in the y direction.
            z (int): The relative movement in the z direction.
        """
        return Func_sendRawMouseMove(x, y, z)

    def SendRawMouseButtonDown(self, button: OculusTouchRawMouseButtonEnum) -> None:
        """Sends a raw mouse button down event to the host computer.

        Args:
            button (OculusTouchRawMouseButtonEnum): The mouse button to send a down event for.
        """
        return Func_sendRawMouseButtonDown(button.value)

    def SendRawMouseButtonUp(self, button: OculusTouchRawMouseButtonEnum) -> None:
        """Sends a raw mouse button up event to the host computer.

        Args:
            button (OculusTouchRawMouseButtonEnum): The mouse button to send an up event for.
        """
        return Func_sendRawMouseButtonUp(button.value)
