"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script streamlit_interface.py
============================
Este script implementa uma interface Streamlit para consultar
o banco de dados SQLite "pizzas.db" usando linguagem natural.

Run:
    streamlit run streamlit_interface.py
"""
import logging
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv, find_dotenv
from utils.constants_ansi import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET

# Configurar a página Streamlit:
st.set_page_config(
    page_title="Pizzaria Delícia de Vitória-ES",
    page_icon="🍕",
    layout="centered",
)

# Configurar logging:
def setup_logging() -> None:
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("LOGs_pizzabot_streamlit.log"),
            logging.StreamHandler(),
        ],
    )

setup_logging()
logger = logging.getLogger(__name__)

# Carregar a chave API da Groq
_ = load_dotenv(find_dotenv())  # lê o arquivo .env local
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializar o banco de dados e o LLM:
@st.cache_resource
def initialize_components():
    """Inicializa o banco de dados e o modelo LLM."""
    try:
        logger.info(f"{CYAN}Conectando ao banco de dados SQLite 'pizzas.db'...{RESET}")
        db = SQLDatabase.from_uri("sqlite:///pizzas.db")
        logger.info(f"{GREEN}Banco de dados conectado com sucesso!{RESET}")
    except Exception as e:
        logger.error(f"{RED}Erro ao conectar ao banco de dados: {e}{RESET}")
        st.error(f"{RED}Erro ao conectar ao banco de dados: {e}{RESET}")
        return None, None
    
    try:
        logger.info(f"{CYAN}Inicializando o modelo LLM 'llama3-70b-8192' da Groq...{RESET}")
        llm = ChatGroq(model_name="llama3-70b-8192", api_key=groq_api_key, temperature=0)
        logger.info(f"{GREEN}Modelo LLM inicializado com sucesso!{RESET}")
        
        # Definir o template do prompt para SQL:
        system_prompt = """Você é um assistente de SQL especializado em traduzir perguntas em linguagem natural para consultas SQL.
        
        Você tem acesso a um banco de dados com a seguinte tabela:
        
        # Tabela 'pizza'
        - id (INTEGER, PRIMARY KEY): Identificador único da pizza
        - name (TEXT): Nome da pizza
        - tamanho (TEXT): Tamanho da pizza (Pequena, Média, Grande)
        - preco (REAL): Preço da pizza
        - ingredientes (TEXT): Lista de ingredientes da pizza
        
        O usuário fará perguntas em linguagem natural sobre o cardápio de pizzas.
        Primeiro, traduza a pergunta para SQL. Em seguida, explique os resultados em português brasileiro, de forma amigável e útil.
        IMPORTANTE: Sempre responda em português brasileiro (pt-br).
        
        Exemplos:
        - "Quais pizzas contêm calabresa?" -> SELECT * FROM pizza WHERE ingredientes LIKE '%calabresa%'
        - "Qual a pizza mais cara?" -> SELECT * FROM pizza ORDER BY preco DESC LIMIT 1
        
        Aqui está o esquema do banco de dados:
        {schema}
        
        Lembre-se: sua resposta deve ser sempre em português brasileiro (pt-br) e ser útil para o cliente da pizzaria.
        """
        
        # Criar a corrente de processamento:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}\n\nSQL query:")
        ])

        def run_query(query):
            try:
                logger.info(f"Executando consulta SQL: {query}")
                return db.run(query)
            except Exception as e:
                logger.error(f"Erro ao executar consulta SQL: {e}")
                return f"Erro na consulta SQL: {e}"

        # Criar a cadeia de processamento:
        sql_chain = (
            RunnablePassthrough.assign(schema=lambda _: db.get_table_info())
            | prompt
            | llm
            | StrOutputParser()
        )
        
        def process_query_with_sql(query):
            try:
                # Primeiro, gerar a consulta SQL:
                sql_query_response = sql_chain.invoke({"input": query})
                
                # Extrair a consulta SQL do texto de resposta:
                sql_lines = [line for line in sql_query_response.split('\n') if line.strip().upper().startswith("SELECT")]
                
                if not sql_lines:
                    return "Não consegui gerar uma consulta SQL válida para essa pergunta."
                
                sql_query = sql_lines[0].strip()
                
                # Executar a consulta SQL:
                sql_result = run_query(sql_query)
                
                # Gerar resposta final com os resultados:
                final_prompt = ChatPromptTemplate.from_messages([
                    ("system", "Você é um atendente de pizzaria que responde perguntas sobre o cardápio. SEMPRE responda em português brasileiro (pt-br), de forma amigável e prestativa."),
                    ("human", f"Pergunta original: {query}\n\nConsulta SQL executada: {sql_query}\n\nResultados da consulta: {sql_result}\n\nForneca uma resposta útil e amigável em português brasileiro (pt-br):")
                ])
                
                final_response = final_prompt | llm | StrOutputParser()
                return final_response.invoke({})
                
            except Exception as e:
                logger.error(f"{RED}Erro ao processar consulta: {e}{RESET}")
                return f"Desculpe, não consegui processar sua pergunta. Erro: {str(e)}"
        
        return db, process_query_with_sql
        
    except Exception as e:
        logger.error(f"{RED}Erro ao inicializar o modelo LLM: {e}{RESET}")
        st.error(f"{RED}Erro ao inicializar o modelo LLM: {e}{RESET}")
        return db, None

# Interface Streamlit
def main():

    # Adicionando informações do autor na sidebar:
    st.sidebar.markdown("### Autor:")
    st.sidebar.markdown("Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro")
    st.sidebar.markdown("##### Contatos:")
    st.sidebar.markdown(
        """
    - 📧 e-mail: eddychirinos.unac@gmail.com
    - 💼 [LinkedIn](https://www.linkedin.com/in/eddy-giusepe-chirinos-isidro-phd-85a43a42/)
    - 🐱 [Repositório: Hugging Face](https://huggingface.co/EddyGiusepe)
    """
    )

    # Título e introdução
    st.title("🍕 Pizzaria Delícia de Vitória-ES")
    st.markdown("""
    Bem-vindo ao assistente virtual da Pizzaria Delícia! 
    Faça perguntas sobre nosso cardápio de pizzas em linguagem natural.
    """)
    
    # Inicializar componentes
    db, query_processor = initialize_components()
    
    if not db or not query_processor:
        st.error("Não foi possível inicializar todos os componentes necessários.")
        return
    
    # Inicializar o histórico de mensagens se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou o assistente da Pizzaria Delícia. Como posso ajudar?"}
        ]
    
    # Exibir mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Faça uma pergunta sobre nossas pizzas..."):
        # Adicionar pergunta do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Resposta do assistente
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                with st.spinner("Processando sua pergunta..."):
                    response = query_processor(prompt)
                
                # Adicionar resposta ao histórico
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Exibir resposta
                message_placeholder.markdown(response)
            except Exception as e:
                error_msg = f"Erro ao processar sua pergunta: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                message_placeholder.markdown(error_msg)
                logger.error(error_msg)

    # Adicionar um botão para limpar o histórico
    if st.sidebar.button("Limpar conversa"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou o assistente da Pizzaria Delícia. Como posso ajudar?"}
        ]
        st.rerun()
    
    # Informações sobre o banco de dados
    with st.sidebar:
        st.header("Sobre o PizzaBot")
        st.info("""
        Este assistente usa IA para responder perguntas sobre o cardápio da Pizzaria Delícia.
        
        Exemplos de perguntas:
        - Quais são as pizzas disponíveis?
        - Qual a pizza mais cara?
        - Tem pizza vegetariana?
        - Quais são os ingredientes da pizza Calabresa?
        """)

if __name__ == "__main__":
    main() 