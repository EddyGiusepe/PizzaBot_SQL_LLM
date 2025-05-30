#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script create_database.py
=========================
Este script cria um banco de dados SQLite chamado 
"pizzas.db" e insere dados de pizzas nele.

Run:
    uv run create_database.py
"""
import sqlite3
import logging
from utils.constants_ansi import *

def setup_logging() -> None:
    """Configures the logging system"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("LOGs_pizzabot.log"),
            logging.StreamHandler(),
        ],
    )


setup_logging()
logger = logging.getLogger(__name__)

# Conectar ao DB (irá criar se não existir):
conn = sqlite3.connect("pizzas.db", timeout=30) # chinook  ou  pizzas
cursor = conn.cursor()

# Configurando PRAGMAs para melhorar o gerenciamento de bloqueio
cursor.execute("PRAGMA journal_mode=WAL")
cursor.execute("PRAGMA busy_timeout=5000")

cursor.execute('''
CREATE TABLE IF NOT EXISTS pizza (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    tamanho TEXT NOT NULL,
    preco REAL NOT NULL,
    ingredientes TEXT NOT NULL
)
''')

# Inserir dados de pizzas:
pizzas = [
    (1, 'Margherita', 'Pequena', 30.99, 'Tomate, Mozzarella, Manjericão'),
    (2, 'Pepperoni', 'Média', 20.99, 'Pepperoni, Mozzarella'),
    (3, 'Quatro Queijos', 'Grande', 25.99, 'Mozzarella, Cheddar, Parmesão, Gorgonzola'),
    (4, 'Mussarela', 'Média', 27.99, 'Mussarela, rodelas de tomate e orégano'),
    (5, 'Escarola', 'Pequena', 29.50, 'Escarola refogada, mussarela e orégano'),
    (6, 'Marguerita', 'Grande', 32.99, 'Mussarela, rodelas de tomate e manjericão'),
    (7, 'Atum', 'Média', 34.50, 'Mussarela, atum e cebola e orégano'),
    (8, 'Romana', 'Grande', 36.99, 'Mussarela aliche e queijo parmesão e orégano'),
    (9, 'Calabresa', 'Pequena', 28.50, 'Mussarela, linguiça calabresa e cebola'),
    (10, 'Napolitana', 'Média', 31.99, 'Mussarela, rodelas de tomate, queijo parmesão e orégano'),
    (11, 'Brócolis', 'Grande', 33.50, 'Brócolis refogado coberto com mussarela e alho'),
    (12, 'Siciliana', 'Pequena', 35.99, 'Mussarela, bacon e champignon ao molho rose'),
    (13, 'Lombinho', 'Média', 30.50, 'Mussarela, lombo defumado e cebola'),
    (14, 'Portuguesa', 'Grande', 38.99, 'Mussarela, ovos, palmito, pimentão, ervilha, presunto e cebola'),
    (15, 'Alho e óleo', 'Pequena', 26.50, 'Mussarela, alho e queijo parmesão'),
    (16, 'Palmito', 'Média', 32.99, 'Mussarela, palmito e orégano'),
    (17, 'Camarão', 'Grande', 42.50, 'Camarão, molho de tomate, mussarela e catupiry'),
    (18, 'Toscana', 'Pequena', 33.99, 'Linguiça calabresa bacon e catupiry'),
    (19, 'Mineira', 'Média', 29.50, 'Mussarela, catupiry e milho verde'),
    (20, 'Pepperoni', 'Grande', 34.99, 'Mussarela, pepperoni e cebola'),
    (21, 'Bacon', 'Pequena', 31.50, 'Mussarela coberta com bacon e orégano'),
    (22, 'Mista', 'Média', 28.99, 'Mussarela, presunto e orégano'),
    (23, 'Califórnia', 'Grande', 36.50, 'Mussarela, presunto, salada de frutas e orégano'),
    (24, 'Vegetariana', 'Pequena', 33.99, 'Mussarela, pimentão, cebola, azeitona, ervilha, tomate, palmito, milho e orégano'),
    (25, 'Frango', 'Média', 29.50, 'Molho de tomate, mussarela e frango'),
    (26, 'Frango com Catupiry', 'Grande', 35.99, 'Molho de tomate, mussarela, frango e catupiry'),
    (27, 'Bolonhesa', 'Pequena', 32.50, 'Mussarela, molho a bolonhesa e orégano'),
    (28, 'Rúcula com Tomate Seco', 'Média', 36.99, 'Mussarela, rúcula, tomate seco e orégano'),
    (29, 'Champignon', 'Grande', 34.50, 'Mussarela, champignon e orégano'),
    (30, 'Espanhola', 'Pequena', 30.99, 'Presunto, mussarela, calabresa e cebola'),
    (31, 'Berinjela', 'Média', 32.50, 'Berinjela, cebola, parmesão, mussarela e azeitona preta'),
    (32, 'Brasileira', 'Grande', 35.99, 'Ervilha, milho, palmito, tomate, mussarela e manjericão'),
    (33, 'Aliche', 'Pequena', 33.50, 'Mussarela, aliche e tomates'),
    (34, 'Quatro queijos', 'Média', 37.99, 'Mussarela, provolone, parmesão e catupiry'),
    (35, 'Havaiana', 'Grande', 34.50, 'Mussarela, lombo e abacaxi'),
    (36, 'Italiana', 'Pequena', 32.99, 'Mussarela, parmesão, salame italiano e tomates'),
    (37, 'Parmegiana', 'Média', 31.50, 'Presunto, mussarela, molho parmegiana'),
    (38, 'Tropical', 'Grande', 38.99, 'Mussarela, frango, milho, ervilha, ovos e catupiry'),
    (39, 'Canadense', 'Pequena', 39.50, 'Mussarela, lombo, champignon, palmito e catupiry'),
    (40, 'Strogonoff', 'Média', 40.99, 'Mussarela, champignon, strogonoff de frango e batata palha'),
    (41, 'Bauru', 'Grande', 31.50, 'Presunto, mussarela, tomate, orégano e azeitonas'),
    (42, 'Carne Seca', 'Pequena', 41.99, 'Carne seca, mussarela, cebola, parmesão e orégano'),
    (43, 'Gorgonzola', 'Média', 38.50, 'Gorgonzola, tomate, orégano e azeitonas')
]

# Remover todos os registros da tabela "pizza" existentes para evitar duplicação:
cursor.execute("DELETE FROM pizza")
# Inserir os dados das pizzas no DB:
cursor.executemany("INSERT INTO pizza VALUES (?, ?, ?, ?, ?)", pizzas) # ? -> São espaços reservados para os valores que serão inseridos
# Salvar alterações e fechar conexão:
conn.commit()
conn.close()

logger.info(f"{GREEN}Banco de dados de pizzas criado com sucesso!{RESET}")
