from pydantic import BaseModel
import pyodbc
from datetime import datetime
import streamlit as st


class Words(BaseModel):
    word_id: int = 0
    word: str
    translation: str
    description: str = ""
    formality_level: str = ""
    grammatical_class: str = ""
    updated_at: datetime = datetime.now()
    user_id: int = 1


class Sentences(BaseModel):
    sentence_id: int = 0
    word_id: int = 0
    sentence: str
    grammar_score: float
    vocabulary_score: float
    naturalness_score: float
    punctuation_score: float
    registered_at: datetime = None
    updated_at: datetime = None


class Database:
    server = 'restdb.database.windows.net'
    database = 'Wise-Englishman-Database'
    username = 'boss'
    password = 'STUDY!english'

    @staticmethod
    def get_connection():
        connection_string = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={Database.server},1433;"
            f"DATABASE={Database.database};"
            f"UID={Database.username};"
            f"PWD={Database.password};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        return pyodbc.connect(connection_string)

    @staticmethod
    def insert_word(word: Words):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO words 
            (user_id, word, translation, description, formality_level, grammatical_class, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                word.user_id,
                word.word,
                word.translation,
                word.description,
                word.formality_level,
                word.grammatical_class,
                word.updated_at
            ))

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Erro ao inserir palavra: {e}")

    @staticmethod
    def get_latest_words(limit=5):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT TOP {limit} word, translation 
            FROM words
            ORDER BY updated_at DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            st.error(f"Erro ao buscar últimas palavras: {e}")
            return []

    @staticmethod
    def get_random_word():
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            query = """
            SELECT TOP 5 word, translation 
            FROM words
            ORDER BY NEWID()
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            st.error(f"Erro ao buscar palavra aleatória: {e}")
            return []
        
    @staticmethod
    def buscar_word_id(word):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT word_id FROM words WHERE word = ?", (word))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            st.error(f"Erro ao buscar word_id: {e}")
            return None

    @staticmethod
    def adicionar_frase(sentences: Sentences):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO sentences 
            (word_id, sentence, grammar_score, vocabulary_score, naturalness_score, punctuation_score, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                sentences.word_id,
                sentences.sentence,
                sentences.grammar_score,
                sentences.vocabulary_score,
                sentences.naturalness_score,
                sentences.punctuation_score,
                datetime.now()
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Erro ao inserir frase: {e}")
            return False

    @staticmethod
    def buscar_frases(word):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 1 word_id FROM words WHERE word = ?", (word))
            result = cursor.fetchone()
            if not result:
                return []

            word_id = result[0]
            cursor.execute(
                "SELECT sentence, grammar_score, vocabulary_score, naturalness_score, punctuation_score FROM sentences WHERE word_id = ? ORDER BY updated_at DESC",
                (word_id)
            )
            frases = cursor.fetchall()
            return frases
        except Exception as e:
            st.error(f"Erro ao buscar frases: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_palavras_nao_aprendidas():
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM words ORDER BY RAND()")
            todas = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Erro ao buscar palavras: {e}")
            return []

        nao_aprendidas = []
        limit_nao_aprendidas = 0
        media = 0
        for p in todas:
            if limit_nao_aprendidas >= 4:
                break
            
            frases = Database.buscar_frases(p[0])
            if not frases:
                nao_aprendidas.append({"word": p[0], "quantidade_frases": len(frases)})
                limit_nao_aprendidas += 1
                continue
            
            for f in frases:
                media += float(f[1] + f[2] + f[3] + f[4]) / 4.0 / (len(frases))
            
            if media <= 7:
                print(len(frases) , "")
                nao_aprendidas.append({"word": p.word, "quantidade_frases": (len(frases))})
                limit_nao_aprendidas += 1

        return nao_aprendidas

    @staticmethod
    def detalhes_da_palavra(word: Words):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT TOP 1 translation, description, formality_level, grammatical_class
                FROM words
                WHERE word = ?
                ORDER BY updated_at DESC
            """, (word.word,))
            row = cursor.fetchone()
            return row if row else {}
        except Exception as e:
            st.error(f"Erro ao buscar detalhes da palavra: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()


# EXECUÇÃO INICIAL
if __name__ == "__main__":
    print("Banco configurado!")