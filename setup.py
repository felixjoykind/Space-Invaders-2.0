import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Space invaders 0.2.0",
        version = "0.2.0",
        description = "Simple Space Shooter",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Space Invaders.py", base=base)])
