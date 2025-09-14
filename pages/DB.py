import pymysql
from pydantic import BaseModel
import streamlit as st

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