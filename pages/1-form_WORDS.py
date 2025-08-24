import streamlit as st
import pandas as pd
import pymysql
from pydantic import BaseModel
from datetime import datetime

server = 'localhost'
database = 'wordDatabase'
username = 'root'
password = 'eduardo2005'

def get_connection():
    return pymysql.connect(
        host=server,
        user=username,
        password=password,
        database=database,
        port=3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

class Words(BaseModel):
    word_id: int = 0
    word: str
    translation: str
    description: str = ""
    formality_level: str = ""
    grammatical_class: str = ""
    user_id: int = 1

def insert_word(word: Words):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO words 
        (user_id, word, translation, description, formality_level, grammatical_class)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            word.user_id,
            word.word,
            word.translation,
            word.description,
            word.formality_level,
            word.grammatical_class
        ))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Palavra inserida com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inserir palavra: {e}")

def get_latest_words(limit=5):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT word, translation FROM words
        ORDER BY created_at DESC
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        st.error(f"Erro ao buscar palavras: {e}")
        return []

def get_random_updated_word():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT word, translation FROM words
        WHERE updated_at IS NOT NULL
        ORDER BY RAND()
        LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        st.error(f"Erro ao buscar palavra aleatória: {e}")
        return None

st.title("Registro de Palavras")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    palavra = st.text_input("PALAVRA")
    significado = st.text_input("SIGNIFICADO")
    complemento = st.text_input("COMPLEMENTO")
    formalidade = st.text_input("FORMALIDADE")
    gramatical = st.text_input("CLASSE GRAMATICAL")

    if st.button("INSERIR PALAVRAS"):
        if not palavra or not significado:
            st.error("PALAVRA e SIGNIFICADO são obrigatórios.")
        else:
            nova_palavra = Words(
                word=palavra,
                translation=significado,
                description=complemento,
                formality_level=formalidade,
                grammatical_class=gramatical,
                user_id=1
            )
            insert_word(nova_palavra)

with col2:
    palavras = get_latest_words()
    if palavras:
        df = pd.DataFrame(palavras)
        st.dataframe(df.reset_index(drop=True))
    else:
        st.write("Nenhuma palavra encontrada.")

    st.markdown("---")

    palavra_aleatoria = get_random_updated_word()
    if palavra_aleatoria:
        st.write(f"<table style='margin:0 auto; background-color: white;' width= '100%'><tr><td style='text-align: center; color: black'>{palavra_aleatoria['word']}</td><td style='text-align: center; color: black'>{palavra_aleatoria['translation']}</td></tr></table>", unsafe_allow_html=True)
    else:
        st.write("Nenhuma palavra atualizada encontrada.")

    st.markdown("")
    st.markdown("")
    st.markdown("")
    
    if st.button("ATUALIZAR"):
        try:
            st.experimental_rerun()
        except AttributeError:
            st.rerun()
