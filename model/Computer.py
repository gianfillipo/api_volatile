import os, sys

class Computer:

	@staticmethod
	def get_operational_system():
		return sys.platform.lower()

	@staticmethod
	def get_serial_number():
		os_type = Computer.get_serial_number()
		
		if "win" in os_type:
			command = "wmic bios get serialnumber"
		elif "linux" in os_type:
			command = "sudo dmidecode -t system | grep Serial"
		elif "darwin" in os_type:
			command = "ioreg -l | grep IOPlatformSerialNumber"

		return os.popen(command).read().replace("\n","").replace("	","").replace(" ","").replace(":", "")[12:]