import pymysql
import random
import streamlit as st
from pydantic import BaseModel
from datetime import datetime
from datetime import datetime

# CONFIGURAÇÃO DO BANCO DE DADOS
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


class Databese:
    server = 'localhost'
    database = 'wordDatabase'
    username = 'root'
    password = 'eduardo2005'

    @staticmethod
    def get_connection():
        return pymysql.connect(
        host=Databese.server,
        user=Databese.username,
        password=Databese.password,
        database=Databese.database,
        port=3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )

    @staticmethod
    def adicionar_frase(sentences:Sentences):
        try:
            conn = Databese.get_connection()
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
    def buscar_frases(sentence):
    
        # Busca todas as frases associadas a uma palavra
        try:
            conn = Databese.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT word_id FROM sentences WHERE sentence=%s", (sentence,))
            result = cursor.fetchone()
            if not result:
                return []
            word_id = result['word_id']
            cursor.execute("SELECT * FROM sentences WHERE word_id=%s ORDER BY created_at DESC", (word_id,))
            frases = cursor.fetchall()
        except Exception as e:
            print(f"error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_palavras_nao_aprendidas():
        conn = Databese.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM words")
            todas = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        nao_aprendidas = []
        for p in todas:
            frases = Databese.buscar_frases(p['word'])
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
    def detalhes_da_palavra(word_id):

        conn = Databese.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT translation, description, formality_level, grammatical_class
                FROM sentences
                WHERE word_id = %s
                ORDER BY created_at DESC
                LIMIT 1
                """, (word_id,))
            row = cursor.fetchone() or {}
        finally:
            cursor.close()
            conn.close()
    
        return {
            "Tradução": row.get("translation") or "",
            "Descrição": row.get("description") or "",
            "Grau de Formalidade": row.get("formality_level") or "",
            "Classe Gramatical": row.get("grammatical_class") or "",
            }

# EXECUÇÃO INICIAL
    if __name__ == "__main__":
        print("Banco configurado!")