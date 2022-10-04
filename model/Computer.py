from OperationalSystem import OperationalSystem
import os

class Computer:

	@staticmethod
	def get_serial_number():
		os_type = OperationalSystem.get()
		
		if "win" in os_type:
			command = "wmic bios get serialnumber"
		elif "linux" in os_type:
			command = "sudo dmidecode -t system | grep Serial"

		return os.popen(command).read().replace("\n","").replace("	","").replace(" ","").replace(":", "")[12:]