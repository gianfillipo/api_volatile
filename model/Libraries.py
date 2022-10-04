import os
from OperationalSystem import OperationalSystem

class Libraries:

    @staticmethod
    def get_command(biblioteca):
        os_type = OperationalSystem.get()
        command = "pip list | "

        if "win" in os_type:
            command += 'findstr /c:"{}"'.format(biblioteca)
        elif "linux" in os_type:
            command += "grep {}".format(biblioteca) 

        return command

    @staticmethod
    def valid_libraries():
        bibliotecas = ['Str', 'psutil', 'time', 'datetime', 'platform', 'mysql-connector-python', 'pyodbc','sys']
        for i in bibliotecas:
                command = Libraries.get_command(i)
                exibir = os.popen(command).read()

                if (exibir == ''):
                    print("Instalando biblioteca {}".format(i))
                    ins = 'pip install {}'.format(i)
                    instal = os.system(ins)

                else:
                    print(exibir)


