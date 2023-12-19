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
from py_oculus_touch import OculusTouch, OculusTouchButtonEnum

# Initialize the OculusTouch object
oculus = OculusTouch()

while True:
    isWearing = oculus.Wearing()
    isXButtonDown = oculus.IsDown(OculusTouchButtonEnum.X)

    if isWearing and isXButtonDown:
        oculus.Vibrate(0, 1, 128, 1)
        oculus.Vibrate(1, 1, 128, 1)

    oculus.PollAndSleep()
```
