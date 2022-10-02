# Importações de Bibliotecas:
import os, sys

bibliotecas = ['Str', 'psutil', 'time', 'datetime', 'platform', 'mysql-connector-python', 'pyodbc','sys']

def validLibrary(bibliotecas):
 for i in bibliotecas:
        command = 'pip list | findstr /c:"{}"'.format(i)
        exibir = os.popen(command).read()

        if (exibir == ''):
            print("Biblioteca", i ,"não encontrada!")
            ins = 'pip install {}'.format(i)
            instal = os.system(ins)
            
        else:
            print(exibir)
            
def desinstalarBibliotecas(bibliotecas):

    for i in bibliotecas:        
        command = 'pip uninstall {}'.format(i)
        os.system(command)
        validLibrary(bibliotecas)
        
validLibrary(bibliotecas)

from ast import Str
import psutil
import time
from datetime import datetime
import platform
import mysql.connector
from mysql.connector import errorcode
import pyodbc
def buscar_serial():
	os_type = sys.platform.lower()
	if "win" in os_type:
		command = "wmic bios get serialnumber"
	elif "linux" in os_type:
		command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
	elif "darwin" in os_type:
		command = "ioreg -l | grep IOPlatformSerialNumber"
	return os.popen(command).read().replace("\n","").replace("	","").replace(" ","")

def captura(cursor):
    print("Seja bem-vindo ao sistema de captura de dados do seu Hardware \U0001F604")

    tempo = 2
    numero = 10

    if (tempo > 0):
        print("\U0001F750 Iniciando captura dos dados...", "\n--------")
        meu_sistema = platform.uname()
        sistema = meu_sistema.system
        arqmaquina = meu_sistema.machine
        nomeMaquina = meu_sistema.node
        modelo = meu_sistema.processor
        numero_serial = buscar_serial()
        
        numeros_serial = [numero_serial, "SerialNumberF2A3913", "SerialNumberB1M2932"]
        nomemaquinas = [nomeMaquina, "Ubuntu", "Monterey"]
        processadores = [modelo, "Intel Core i7-8650 CPU @ 1.90GHz","Intel Xeon Silver 4114 2.2GHz, 10C/20T, 9.6GT/s"]
        arquiteturas = [arqmaquina, "Intel86","Intel86"]
        sistemas = [sistema, "Linux", "MacOS"]
        
        cursor.execute(
            "SELECT COUNT(idEquipamento) FROM `healthsystem`.`Equipamento`")
        row = cursor.fetchone()
        Equip = int(''.join(map(str, row)))
        print("\U0001F916 Equipamentos detectados:", Equip, "\n--------")

        if Equip < 1:
            cursor.execute(
                "SELECT COUNT(idLocal) FROM `healthsystem`.`local`")
            rowLocal = cursor.fetchone()
            Locais = int(''.join(map(str, rowLocal)))
            print("\U0001F916 Locais detectados:", Locais)
            for i in range(Locais):
                i = i + 1
                a = i - 1
                cursor.execute("INSERT INTO `healthsystem`.`Equipamento` (fkFilial, fkLocal, serialNumber, nome,modelo,arqMaquina, sistemaOp) VALUES (%s,%s,%s, %s,%s, %s,%s);",
                               (1000, i, numeros_serial[a],nomemaquinas[a], processadores[a], arquiteturas[a], sistemas[a]))
                print("\U0001F916 Inserção de dados de Equipamento:", i)
                conn.commit()
            leitura(cursor, numero, tempo)
        else:
            leitura(cursor, numero, tempo)

def leitura(cursor, numero, tempo):
    Quantidade = range(numero)
    for x in Quantidade:
        dataHora = datetime.now()
        dataHoraFormat = dataHora.strftime('%Y/%m/%d %H:%M:%S')

        percentualCPU = psutil.cpu_percent(
            interval=None, percpu=False)
        percentualDisco = psutil.disk_usage('/').percent
        percentualMemoria = psutil.virtual_memory().percent

        # Simulação de valores dos componentes de equipamentos

        percentualCPU3 = percentualCPU * 1.15
        percentualCPU2 = percentualCPU3 - (percentualCPU3 * 0.05)

        percentualMemoria3 = percentualMemoria * 1.10
        percentualMemoria2 = percentualMemoria * 1.15

        percentualDisco2 = percentualDisco - (percentualDisco * 0.05)
        percentualDisco3 = percentualDisco2 * 3

        # Simulação de Equipamentos:

        vetorHardware = [percentualCPU, percentualMemoria, percentualDisco]
        vetorHardware2 = [percentualCPU2, percentualMemoria2, percentualDisco2]
        vetorHardware3 = [percentualCPU3, percentualMemoria3, percentualDisco3]
        vetorEquip = [vetorHardware, vetorHardware2, vetorHardware3]

        cursor.execute(
            "SELECT COUNT(idEquipamento) FROM `healthsystem`.`Equipamento`")
        rowEquip = cursor.fetchone()
        Equipamentos = int(''.join(map(str, rowEquip)))
        print(
            "\U0001F916 Quantidade de Equipamentos detectados: ", Equipamentos)

        cursor.execute(
            "SELECT COUNT(idComponente) FROM `healthsystem`.`Componente`")
        rowComp = cursor.fetchone()
        Componentes = int(''.join(map(str, rowComp)))
        print(
            "\U0001F916 Quantidade de Componentes de Hardware detectados: ", Componentes, "\n--------")

        valor = 0
        for i in range(Equipamentos):
            i = i + 1
            for a in range(Componentes):
                valor = vetorEquip[i-1][a]
                a = a + 1
                cursor.execute("INSERT INTO `healthsystem`.`Leitura` (fkEquipamento, fkComponente, valor, momento) VALUES (%s,%s, %s, %s);",
                               (i, a, valor, dataHoraFormat))
                conn.commit()

        print("\U0001F4BB - Porcentagem de Utilização da CPU: {:.1f}%".format(percentualCPU),
              "\n\U0001F4BB - Porcentagem de Utilização do Disco:", percentualDisco, '%',
              "\n\U0001F4BB - Porcentagem de Utilização da Memoria:", percentualMemoria, '%',
              "\n\U0001F55B - Data e Hora:", dataHoraFormat, "\n--------")

        conn.commit()
        time.sleep(tempo)
    print("Captura de dados finalizada!")
    
# Validações banco local:

def validacaoMysql(conn):
    print("Iniciando validações...")
    
    cursor = conn.cursor()

    cursor.execute("USE `HealthSystem`;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `HealthSystem`.`Empresa` (
    `idEmpresa` INT NOT NULL AUTO_INCREMENT,
    `razaoSocial` VARCHAR(45) NOT NULL,
    `cnpj` CHAR(14) NOT NULL,
    `logradouro` VARCHAR(45) NOT NULL,
    `numero` INT NOT NULL,
    `bairro` VARCHAR(45) NOT NULL,
    `cidade` VARCHAR(45) NOT NULL,
    `estado` CHAR(2) NOT NULL,
    `cep` CHAR(8) NOT NULL,
    PRIMARY KEY (`idEmpresa`)
);""")

    cursor.execute("SELECT COUNT(idEmpresa) FROM `healthsystem`.`Empresa`")
    rowEmp = cursor.fetchone()
    empresa = int(''.join(map(str, rowEmp)))

    if empresa < 1:
        cursor.execute("INSERT INTO `HealthSystem`.`Empresa` VALUES (NULL,'PHILIPS DO BRASIL LTDA',61086336000103,'Avenida Marcos Penteado de Ulhoa Rodrigues',939,'Tambore','Barueri','SP','06460040');")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Credencial` (
    `idCredencial` INT NOT NULL,
    `tipoCredencial` VARCHAR(45) NOT NULL,
    `nivelPermissao` ENUM('1', '2', '3') NOT NULL,
    PRIMARY KEY (`idCredencial`)
);""")

    cursor.execute(
        "SELECT COUNT(idCredencial) FROM `healthsystem`.`Credencial`")
    rowCre = cursor.fetchone()
    credencial = int(''.join(map(str, rowCre)))

    if credencial < 1:
        cursor.execute(
            "INSERT INTO `healthsystem`.`Credencial` VALUES (323145,'Tecnico',1), (543221,'Analista',2), (386531,'Gerente',3);")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Usuario` (`fkEmpresa` INT NOT NULL,
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `fkcredencial` INT NOT NULL,
  PRIMARY KEY(`idUsuario`),
  INDEX `fk_Usuario_Empresa1_idx` (`fkEmpresa` ASC) VISIBLE,
  INDEX `fk_Usuario_Credencial1_idx` (`fkcredencial` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Empresa1`
    FOREIGN KEY(`fkEmpresa`)
    REFERENCES `HealthSystem`.`Empresa` (`idEmpresa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Usuario_Credencial1`
    FOREIGN KEY(`fkcredencial`)
    REFERENCES `HealthSystem`.`Credencial` (`idCredencial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);""")

    cursor.execute("SELECT COUNT(idUsuario) FROM `healthsystem`.`Usuario`")
    rowUser = cursor.fetchone()
    usuario = int(''.join(map(str, rowUser)))

    if usuario < 1:
        cursor.execute(
            "INSERT INTO `healthsystem`.`Usuario` VALUES (1,NULL,'fernandoBrandao','fernando.brandao@sptech.school','1234',323145);")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Componente` (
    `idComponente` INT NOT NULL AUTO_INCREMENT,
    `nomeComponente` VARCHAR(45) NOT NULL,
    PRIMARY KEY(`idComponente`)
);
""")
    cursor.execute(
        "SELECT COUNT(idComponente) FROM `healthsystem`.`Componente`")
    rowComp = cursor.fetchone()
    componente = int(''.join(map(str, rowComp)))

    if componente < 1:
        cursor.execute(
            "INSERT INTO `HealthSystem`.`Componente` (`nomeComponente`) VALUES ('CPU'), ('Memoria'), ('Disco');")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Filial` (
    `idFilial` INT NOT NULL AUTO_INCREMENT,
    `fkEmpresa` INT NOT NULL,
    `nomeFantasia` VARCHAR(45) NOT NULL,
    `logradouro` VARCHAR(45) NOT NULL,
    `numero` INT NOT NULL,
    `bairro` VARCHAR(45) NOT NULL,
    `cidade` VARCHAR(45) NOT NULL,
    `estado` CHAR(2) NOT NULL,
    `cep` CHAR(8) NOT NULL,
    PRIMARY KEY(`idFilial`),
    INDEX `fk_Filial_Empresa1_idx` (`fkEmpresa` ASC) VISIBLE,
    CONSTRAINT `fk_Filial_Empresa1`
    FOREIGN KEY(`fkEmpresa`)
    REFERENCES `healthsystem`.`Empresa` (`idEmpresa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
    AUTO_INCREMENT = 1000;""")

    cursor.execute("SELECT COUNT(idFilial) FROM `healthsystem`.`Filial`")
    rowFil = cursor.fetchone()
    filial = int(''.join(map(str, rowFil)))

    if filial < 1:
        cursor.execute(
            "INSERT INTO `healthsystem`.`filial` VALUES (NULL,1,'HOSPITAL SAO LUIZ GONZAGA','R MICHEL OUCHANA',94,'JACANA','SÃO PAULO','SP','02276140');")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Local` (
    `idLocal` INT NOT NULL AUTO_INCREMENT,
    `identificacao` VARCHAR(45) NOT NULL,
    PRIMARY KEY(`idLocal`)
);""")

    cursor.execute("SELECT COUNT(idLocal) FROM `healthsystem`.`Local`")
    rowLoc = cursor.fetchone()
    local = int(''.join(map(str, rowLoc)))

    if local < 1:
        cursor.execute(
            "INSERT INTO `healthsystem`.`Local` (`identificacao`) VALUES ('Sala de Ultrassom'),('Enfermaria'),('Sala de Manutenção');")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Equipamento` (
  `idEquipamento` INT NOT NULL AUTO_INCREMENT,
  `fkFilial` INT NOT NULL,
  `fkLocal` INT NOT NULL,
  `serialNumber` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `modelo` VARCHAR(100) NOT NULL,
  `arqMaquina` VARCHAR(45) NOT NULL,
  `sistemaOp` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idEquipamento`),
  INDEX `fk_Equipamento_Local1_idx` (`fkLocal` ASC) VISIBLE,
  INDEX `fk_Equipamento_Filial1_idx` (`fkFilial` ASC) VISIBLE,
  CONSTRAINT `fk_Equipamento_Sala1`
    FOREIGN KEY (`fkLocal`)
    REFERENCES `HealthSystem`.`Local` (`idLocal`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Equipamento_Filial1`
    FOREIGN KEY (`fkFilial`)
    REFERENCES `HealthSystem`.`Filial` (`idFilial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Parametro` (
  `fkEquipamento` INT NOT NULL,
  `fkComponente` INT NOT NULL,
  `idParametro` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(100) NOT NULL,
  `valid` TINYINT NOT NULL,
  PRIMARY KEY (`idParametro`,`fkEquipamento`, `fkComponente`),
  INDEX `fk_Equipamento_has_Componente_Componente1_idx` (`fkComponente` ASC) VISIBLE,
  INDEX `fk_Equipamento_has_Componente_Equipamento1_idx` (`fkEquipamento` ASC) VISIBLE,
  CONSTRAINT `fk_Equipamento_has_Componente_Equipamento1`
    FOREIGN KEY (`fkEquipamento`)
    REFERENCES `HealthSystem`.`Equipamento` (`idEquipamento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Equipamento_has_Componente_Componente1`
    FOREIGN KEY (`fkComponente`)
    REFERENCES `HealthSystem`.`Componente` (`idComponente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    );""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS `HealthSystem`.`Leitura` (
  `fkEquipamento` INT NOT NULL,
  `fkComponente` INT NOT NULL,
  `idLeitura` INT NOT NULL AUTO_INCREMENT,
  `valor` FLOAT NOT NULL,
  `momento` DATETIME NOT NULL,
  PRIMARY KEY (`idLeitura`,`fkEquipamento`, `fkComponente`),
  INDEX `fk_Equipamento_has_Componente_Componente1_idx` (`fkComponente` ASC) VISIBLE,
  INDEX `fk_Equipamento_has_Componente_Equipamento1_idx` (`fkEquipamento` ASC) VISIBLE,
  CONSTRAINT `fk_Equipamento_has_Componente_Equipamento2`
    FOREIGN KEY (`fkEquipamento`)
    REFERENCES `HealthSystem`.`Equipamento` (`idEquipamento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Equipamento_has_Componente_Componente2`
    FOREIGN KEY (`fkComponente`)
    REFERENCES `HealthSystem`.`Componente` (`idComponente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    );""")

    print("Validações de tabelas finalizada com sucesso.")
    captura(cursor)

# Validações banco Cloud:

def validacaoSql(conn):
    cursor = conn.cursor()
    print('Iniciando validações...')
    
    captura(cursor)
    
try:
# Deixando a variavel com mysql.local, sera setada a configuração de acesso no banco de dados Local MySQL
    banco = "mysql.local"
# Deixando a variavel com sql.nuvem, sera setada a configuração de acesso no banco de dados na nuvem SQL Server
    # banco = "sql.nuvem"
    if banco == "mysql.local":
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='qwea1020',
            database='healthsystem'
        )
        print("Conexão com o Banco de Dados MySQL efetuada com sucesso.")
        validacaoMysql(conn)

    if banco == "sql.nuvem":
        conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=DESKTOP-T2JV7P5;'
            'Database=PythonSQL;'
            'Trusted_connection = yes;'
        )
        print("Conexão com o Banco de Dados SQL Server efetuada com sucesso.")
        validacaoSql(conn)
    # Validações de Erro:
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Algo está errado com o Usuário do Banco ou a Senha.")
        time.sleep(10)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("O banco de dados direcionado não existe.")
        time.sleep(10)
    else:
        print(err)
        time.sleep(10)
else:
    cursor = conn.cursor()
