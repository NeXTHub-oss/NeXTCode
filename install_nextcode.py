#!/usr/bin/env python3
import shutil
import os

script_path = os.path.abspath("tools/nextcode.py")
destination_path = os.path.join("/usr/local/bin", "nextcode")

try:
    shutil.copy(script_path, destination_path)
    print("Successfully installed NeXTCode.")
except PermissionError:
    print("Error: Permission denied. Try running as administrator.")
except FileNotFoundError:
    print("Error: Script not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
