import mysql.connector
from mysql.connector import Error
import os


class DatabaseManager:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'admin',  # Seu usuário
            'password': '$enhaF0rt3',  # Sua senha
            'database': 'EyeLearnDB'
        }

    def create_connection(self):
        """Cria uma conexão com o banco de dados configurado."""
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def execute_query(self, query, params=None):
        """Executa comandos de escrita (INSERT, UPDATE, DELETE)."""
        connection = self.create_connection()
        if connection is None: return None

        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erro na query: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_all(self, query, params=None):
        """Busca todos os registros (SELECT)."""
        connection = self.create_connection()
        if connection is None: return []

        cursor = connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro no fetch_all: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_one(self, query, params=None):
        """Busca um único registro (SELECT)."""
        connection = self.create_connection()
        if connection is None: return None

        cursor = connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Error as e:
            print(f"Erro no fetch_one: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()



def setup():
    """Função para criar/resetar o banco de dados a partir do arquivo SQL."""
    print("--- Iniciando Setup do Banco de Dados ---")

    # Configuração inicial SEM o banco (para poder criá-lo)
    config_root = {
        'host': 'localhost',
        'user': 'admin',
        'password': '$enhaF0rt3'
    }

    sql_file = 'EyeLearnDB.sql'

    if not os.path.exists(sql_file):
        print(f"❌ Erro: Arquivo '{sql_file}' não encontrado.")
        return

    try:
        # 1. Conectar ao MySQL (sem banco)
        conn = mysql.connector.connect(**config_root)
        cursor = conn.cursor()

        # 2. Ler o arquivo SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # 3. Executar os comandos
        # O arquivo SQL já deve ter o "DROP DATABASE", "CREATE DATABASE" e "USE"
        # Se não tiver, é bom garantir que o banco seja limpo antes:
        try:
            cursor.execute("DROP DATABASE IF EXISTS EyeLearnDB")
            print("Banco antigo removido (se existia).")
        except:
            pass

        commands = sql_script.split(';')
        count = 0
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                    count += 1
                except mysql.connector.Error as err:
                    # Ignora erros simples ou avisos
                    pass

        conn.commit()
        print(f"✅ Sucesso! Banco 'EyeLearnDB' recriado com {count} comandos.")

    except mysql.connector.Error as err:
        print(f"❌ Erro crítico no MySQL: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    setup()