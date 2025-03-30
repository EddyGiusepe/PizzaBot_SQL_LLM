#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script user_interface_with_mesop.py
==================================
Este script mostra como realizar uma consulta ao meu
DB SQLite chamado "pizzas.db". Ou seja, cada consulta
pode ser realizada usando linguagem natural.

Run:
    uv run user_interface_with_mesop.py
"""
import logging
import mesop as me
import mesop.labs as mel
from mesop import stateclass
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from utils.constants_ansi import *
from langchain_groq import ChatGroq
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

logger.info("Iniciando aplicação Pizzaria Delícia de Vitória-ES")

try:
    logger.info(f"{GREEN}Conectando ao banco de dados SQLite 'pizzas.db' . . .{RESET}")
    db = SQLDatabase.from_uri("sqlite:///pizzas.db")
    logger.info(f"{GREEN}Banco de dados conectado com sucesso!{RESET}")
except Exception as e:
    logger.error(f"{RED}Erro ao conectar ao banco de dados: {e}{RESET}")
    raise

try:
    logger.info(
        f"{GREEN}Inicializando o modelo LLM 'llama3-70b-8192' da Groq . . .{RESET}"
    )
    llm = ChatGroq(model_name="llama3-70b-8192", api_key=groq_api_key, temperature=0)
    logger.info(f"{GREEN}Modelo LLM inicializado com sucesso!{RESET}")
except Exception as e:
    logger.error(
        f"{RED}Erro ao inicializar o modelo LLM 'llama3-70b-8192' da Groq: {e}{RESET}"
    )
    raise

try:
    logger.info(f"{GREEN}Criando o agente SQL . . .{RESET}")
    agent_executor = create_sql_agent(
        llm=llm, db=db, agent_type="openai-tools", verbose=False
    )
    logger.info(f"{GREEN}Agente SQL criado com sucesso!{RESET}")
except Exception as e:
    logger.error(f"{RED}Erro ao criar o agente SQL: {e}{RESET}")
    raise


@stateclass  # Gerencia o estado da aplicação
class State:
    pass


logger.info(f"{GREEN}Configurando interface web com Mesop . . .{RESET}")


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
    path="/",
    title="Pizzaria Delícia de Vitória-ES",
)
def page():
    """Interface da página da Pizzaria Delícia de Vitória-ES"""
    logger.info(
        f"{GREEN}Página Mesop inicializada e pronta para receber interações . . .{RESET}"
    )
    mel.chat(transform, title="Pizzaria Delícia de Vitória-ES", bot_user="Pizzabot")


def transform(input: str, history: list[mel.ChatMessage]):
    """
    Processa a entrada do usuário e obtém a resposta do Pizzabot.
    Garante que as respostas sejam sempre em português.
    """
    result = agent_executor.invoke("Responda sempre em português a questão: " + input)

    content = result["output"]
    if content:
        yield content


logger.info(f"{GREEN}Aplicação Pizzabot inicializada e pronta para uso.{RESET}")
