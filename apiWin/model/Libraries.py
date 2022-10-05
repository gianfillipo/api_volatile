from OperationalSystem import OperationalSystem
import os

class Libraries:
    
    @staticmethod
    def valid_libraries():
        bibliotecas = ['Str', 'psutil', 'time', 'datetime', 'platform', 'mysql-connector-python', 'pyodbc','sys']
        for i in bibliotecas:
                command = "pip list | grep {}".format(i)
                exibir = os.popen(command).read()

                if (exibir == ''):
                    print("Instalando biblioteca {}".format(i))
                    ins = 'pip install {}'.format(i)
                    instal = os.system(ins)

                else:
                    print(exibir)