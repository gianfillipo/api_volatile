from sqlite3 import Cursor
import mysql.connector;
from dotenv import load_dotenv;
import os;
import traceback;
import sys;
sys.path.append('../')
from model.Computer import Computador;

class BancoMySql:

    @staticmethod
    def realizar_conexao_banco():
        
        load_dotenv('../.env');
        
        try:
            return mysql.connector.connect(
                host = os.getenv('HOST'),
                user = os.getenv('USER-BANCO'),
                password = os.getenv('PASSWORD'),
                database = os.getenv('DATABASE'),
            )

        except Exception:
            print("Houve um erro na conexão com o banco");
            traceback.print_exc();
            

conn = BancoMySql.realizar_conexao_banco();
cursor = conn.cursor();
sql =  'INSERT INTO computador (serial_number) VALUES ("%s")'
values = [Computador.buscar_serial()];
cursor.execute(sql, values)

