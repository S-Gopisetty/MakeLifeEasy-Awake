import ctypes
import time

# Constants
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

# Keep system and display awake
ctypes.windll.kernel32.SetThreadExecutionState(
    ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
)

# Define INPUT structure for mouse movement
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", _INPUT)]

def move_mouse():
    # Simulate a 0-pixel move — enough to register activity
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(0, 0, 0, 0x0001, 0, ctypes.pointer(extra))
    input_structure = INPUT(0, INPUT._INPUT(mi))
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_structure), ctypes.sizeof(input_structure))

try:
    print("System and Teams will stay active. Press Ctrl+C to stop.")
    while True:
        move_mouse()  # Simulate real input
        time.sleep(60)  # Repeat every 1 minute
except KeyboardInterrupt:
    # Restore system sleep settings
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    print("\nSleep and Teams status behavior restored.")
