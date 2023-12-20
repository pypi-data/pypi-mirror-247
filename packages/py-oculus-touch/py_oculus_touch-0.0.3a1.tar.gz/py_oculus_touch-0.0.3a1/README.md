# py_oculus_touch

## What is it?

This is a python library that allows you to interface with your Oculus Touch controllers and headset. It is a wrapper for the [auto_oculus_touch](https://github.com/rajetic/auto_oculus_touch/) project.

With it, you can read the current state of the controllers and headset, send button presses to the controller, or move the thumbsticks.

### Installation

```bash
pip install py_oculus_touch
```

### API Reference (Under Construction)

### Example Usage

Below is a short program that will vibrate both controllers for 1 second whenever the X button is pressed while the headset is being worn.

```python
from py_oculus_touch import OculusTouch, OculusTouchControllerEnum

oculus = OculusTouch()

while True:
    print("\n")

    wearing = oculus.Wearing()
    print(f"Headset is {'ON' if wearing else 'OFF'} your head")

    x = oculus.GetPositionX(OculusTouchControllerEnum.Head)
    y = oculus.GetPositionY(OculusTouchControllerEnum.Head)
    z = oculus.GetPositionZ(OculusTouchControllerEnum.Head)
    yaw = oculus.GetYaw(OculusTouchControllerEnum.Head)
    pitch = oculus.GetPitch(OculusTouchControllerEnum.Head)
    roll = oculus.GetRoll(OculusTouchControllerEnum.Head)
    print(
        f"Headset Position: ({x}, {y}, {z}), Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}"
    )

    buttons_down: list = oculus.GetButtonsDownList() # Get a list of buttons that are currently held down
    sensors_touched: list = oculus.GetTouchDownList() # Get a list of capacitive sensors that are currently being touched
    print(f"These buttons are down: {buttons_down}")
    print(f"These sensors are touched: {sensors_touched}")

    print("Here's a vibration for fun")
    oculus.Vibrate(OculusTouchControllerEnum.Left) # Vibrate the left controller
    oculus.Vibrate(OculusTouchControllerEnum.Right) # Vibrate the right controller

    oculus.PollAndSleep(1.0) # Poll and wait for 1 second
```

This is a smaple output from the above program:

```
Headset is ON your head
Headset Position: (0.002324591390788555, 0.0881958156824112, -0.02958393096923828), Yaw: 0.26628559827804565, Pitch: 32.98610305786133, Roll: -2.244016647338867
These buttons are down: []
These sensors are touched: []
Here's a vibration for fun


Headset is ON your head
Headset Position: (0.0005310606211423874, 0.09536674618721008, 0.0015068724751472473), Yaw: -0.9234217405319214, Pitch: 35.654449462890625, Roll: -3.4883065223693848
These buttons are down: []
These sensors are touched: [<OculusTouchButtonEnum.RThumb: 4>, <OculusTouchButtonEnum.LThumb: 1024>]
Here's a vibration for fun


Headset is ON your head
Headset Position: (3.6899931728839874e-05, 0.09039056301116943, -0.018536627292633057), Yaw: 3.5531980991363525, Pitch: 33.512542724609375, Roll: -5.120441913604736
These buttons are down: [<OculusTouchButtonEnum.RThumb: 4>, <OculusTouchButtonEnum.LThumb: 1024>]
These sensors are touched: [<OculusTouchButtonEnum.RThumb: 4>, <OculusTouchButtonEnum.LThumb: 1024>]
Here's a vibration for fun


Headset is ON your head
Headset Position: (0.009187383577227592, 0.0899086445569992, -0.02320261299610138), Yaw: 5.528964042663574, Pitch: 33.527103424072266, Roll: -5.911553382873535
These buttons are down: []
These sensors are touched: [<OculusTouchButtonEnum.A: 1>, <OculusTouchButtonEnum.B: 2>, <OculusTouchButtonEnum.X: 256>, <OculusTouchButtonEnum.Y: 512>, <OculusTouchButtonEnum.LThumb: 1024>]
Here's a vibration for fun
```