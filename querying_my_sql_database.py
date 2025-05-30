#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script querying_my_sql_database.py
==================================
Este script mostra como realizar uma consulta ao meu
DB SQLite chamado "pizzas.db". Ou seja, cada consulta
pode ser realizada usando linguagem natural.

Run:
    uv run querying_my_sql_database.py
"""
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq
import logging
from utils.constants_ansi import *
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
groq_api_key = os.getenv("GROQ_API_KEY")


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

# Adicionando parâmetros de conexão para evitar bloqueios
connect_args = {"timeout": 30, "check_same_thread": False}
db = SQLDatabase.from_uri("sqlite:///pizzas.db", connect_args=connect_args)

llm = ChatGroq(model_name="llama3-70b-8192", api_key=groq_api_key, temperature=0)

agent_executor = create_sql_agent(
    llm=llm, db=db, agent_type="openai-tools", verbose=False
)


def querying_interactively():
    """Função que cria uma interface interativa para consultas sobre pizzas"""
    logger.info(f"{BLUE}🤖 Bem-vindo ao Sistema de Consulta de Pizzas 🤖!{RESET}")
    logger.info(f"{YELLOW}Digite 'sair' para encerrar o programa.{RESET}")

    while True:
        question = input(f"\n{GREEN}Digite sua pergunta sobre pizzas 🍕: {RESET}")

        # Verificar se o usuário quer sair:
        if question.lower() in ["sair", "exit", "quit"]:
            logger.info(
                f"{BLUE}👋 Obrigado por usar o Sistema de Consulta de Pizzas!{RESET}"
            )
            break

        # Processar pergunta com o PizzaBot:
        try:
            result = agent_executor.invoke(
                f"Responda em português a seguinte pergunta: {question}"
            )
            print(f"\n{CYAN}Resposta:{RESET} {result['output']}")
        except Exception as e:
            logger.error(f"{RED}Erro ao processar sua pergunta: {str(e)}{RESET}")


if __name__ == "__main__":
    querying_interactively()
