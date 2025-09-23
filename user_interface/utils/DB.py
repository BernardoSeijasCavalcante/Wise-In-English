from pydantic import BaseModel
import pymssql
from datetime import datetime
import random
from datetime import datetime


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
    word_id: int
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


    def get_connection():
        return pymssql.connect(server=Database.server, user=Database.username, password=Database.password, database=Database.database)

    @staticmethod
    def insert_word(word: Words):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO words 
            (user_id, word, translation, description, formality_level, grammatical_class, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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
            print(e)

    @staticmethod
    def get_latest_words(limit=5):
        try:
            conn = Database.get_connection()
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
            return []

    @staticmethod
    def get_random_word():
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            query = """
            SELECT TOP 5 word, translation FROM words
            ORDER BY NEWID()
            """

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(e)
    


    @staticmethod
    def adicionar_frase(sentences:Sentences):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO sentences 
            (word_id, sentence, grammar_score, vocabulary_score, naturalness_score, punctuation_score, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query,(
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
        except Exception as e:
            st.error(f"Erro ao inserir palavra: {e}")

    @staticmethod
    def buscar_frases(word):
    
        # Busca todas as frases associadas a uma palavra
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 1 words.word_id FROM words WHERE word=%s", (word))
            result = cursor.fetchone()
            if not result:
                return []
            word_id = result['word_id']
            cursor.execute("SELECT sentence FROM sentences WHERE word_id=%s ORDER BY created_at DESC", (word_id))
            frases = cursor.fetchall()
        except Exception as e:
            print(f"error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_palavras_nao_aprendidas():
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT word FROM words")
            todas = cursor.fetchall()
        except Exception as e:
            print(f"error: {e}")
            return[]
        finally:
            cursor.close()
            conn.close()

        nao_aprendidas = []
        for p in todas:
            frases = Database.buscar_frases(p['word'])
            if not frases:
                nao_aprendidas.append({"word": p['word'], "quantidade_frases": 0})
                continue
            media = sum(
                (f['grammar_score'] + f['vocabulary_score'] + f['naturalness_score'] + f['punctuation_score']) / 4
                for f in frases
                ) / len(frases)

            if media <= 7:
                nao_aprendidas.append({"word": p['word'], "quantidade_frases": len(frases)})

        return nao_aprendidas

    @staticmethod
    def detalhes_da_palavra(word):

        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT translation, description, formality_level, grammatical_class
                TOP 1
                FROM words
                WHERE words.word = %s
                ORDER BY created_at DESC
                """, (word.word))
            row = cursor.fetchone() or {}
            return row
        except Exception as e:
            print(f"error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


# EXECUÇÃO INICIAL
    if __name__ == "__main__":
        print("Banco configurado!")