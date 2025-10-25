from pydantic import BaseModel
import pyodbc
from datetime import datetime
import streamlit as st

#from user_interface.utils.DB import Words, Database, Sentences

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
    def validar_login(username, password):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE username = ? AND password = ?"

            cursor.execute(query, (username, password))

            row = cursor.fetchone()

            conn.commit()
            cursor.close()
            conn.close()

            if not row:
                return False
            else:
                return True
        except Exception as e:
            print(e)


    @staticmethod
    def validar_signup(username, email, pwd, confirm):
        try:
            if not all([username, email, pwd, confirm]):
                st.warning("Por favor, preencha todos os campos.")
                return False

            if pwd != confirm:
                st.error("As senhas não coincidem.")
                return False

            conn = Database.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                st.warning("Este e-mail já está registrado.")
                cursor.close()
                conn.close()
                return False

            query = """
                INSERT INTO users (username, email, password, last_activity)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (username, email, pwd, datetime.now()))
            conn.commit()

            cursor.close()
            conn.close()

            st.success("Cadastro realizado com sucesso!")
            return True

        except Exception as e:
            st.error(f"Erro ao realizar cadastro: {e}")
            return False

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
                "SELECT sentence_id, sentence, grammar_score, vocabulary_score, naturalness_score, punctuation_score FROM sentences WHERE word_id = ? ORDER BY updated_at DESC",
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
            
            cursor.execute("SELECT TOP 30 word, word_id FROM words ORDER BY NEWID()") 
            palavras = cursor.fetchall() 

            if not palavras:
                cursor.close()
                conn.close()
                return [] 
            
            resultado = []
            for p in palavras:
                word = p[0]
                word_id = p[1]

                frases = Database.buscar_frases_por_word_id(word_id)
                
                total_occurrences = 0
                for frase in frases:   
                    total_occurrences += 1

                resultado.append({"word": word, "quantidade_frases": total_occurrences})
            
            cursor.close()
            conn.close()
            
            return resultado
                
        except Exception as e:
            st.error(f"Erro ao buscar palavras: {e}")
            return []

    @staticmethod
    def buscar_frases_por_word_id(word_id):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT sentence FROM sentences WHERE word_id = ?", (word_id,))
            frases = cursor.fetchall()


            return [frase[0] for frase in frases] 
        except Exception as e:
            st.error(f"Erro ao buscar frases para o word_id {word_id}: {e}")
            return []
        finally: 
            cursor.close()
            conn.close()

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

    @staticmethod
    def get_dashboard_metrics():
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()

            # 1. Total de Palavras Descobertas
            cursor.execute("SELECT COUNT(word_id) FROM words")
            total_palavras = cursor.fetchone()[0]

            # 2. Total de Frases Criadas
            cursor.execute("SELECT COUNT(sentence_id) FROM sentences")
            total_frases = cursor.fetchone()[0]

            # 3. Média de Avaliação Geral e por Categoria
            cursor.execute("""
                SELECT 
                    AVG(grammar_score), 
                    AVG(vocabulary_score), 
                    AVG(naturalness_score), 
                    AVG(punctuation_score)
                FROM sentences
            """)
            avg_scores = cursor.fetchone()
            
            # Se não houver frases, as médias serão None, trate para 0.0
            grammar_avg = avg_scores[0] if avg_scores[0] is not None else 0.0
            vocabulary_avg = avg_scores[1] if avg_scores[1] is not None else 0.0
            naturalness_avg = avg_scores[2] if avg_scores[2] is not None else 0.0
            punctuation_avg = avg_scores[3] if avg_scores[3] is not None else 0.0
            
            geral_avg = (grammar_avg + vocabulary_avg + naturalness_avg + punctuation_avg) / 4

            cursor.close()
            conn.close()
            
            return {
                "total_palavras": total_palavras,
                "total_frases": total_frases,
                "media_geral": geral_avg,
                "media_gramatica": grammar_avg,
                "media_vocabulario": vocabulary_avg,
                "media_naturalidade": naturalness_avg,
                "media_pontuacao": punctuation_avg,
            }

        except Exception as e:
            st.error(f"Erro ao buscar métricas do dashboard: {e}")
            return {
                "total_palavras": 0,
                "total_frases": 0,
                "media_geral": 0.0,
                "media_gramatica": 0.0,
                "media_vocabulario": 0.0,
                "media_naturalidade": 0.0,
                "media_pontuacao": 0.0,
            }
            
    @staticmethod
    def get_all_sentence_scores():
        """Busca todas as pontuações de frases para gráficos."""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    grammar_score, 
                    vocabulary_score, 
                    naturalness_score, 
                    punctuation_score
                FROM sentences
                ORDER BY registered_at DESC
            """
            cursor.execute(query)
            
            # Converte os resultados para uma lista de dicionários ou DataFrame (ideal para gráficos)
            results = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            
            conn.close()
            
            # Retorna uma lista de dicionários para fácil conversão em DataFrame
            return [dict(zip(columns, row)) for row in results]
            
        except Exception as e:
            st.error(f"Erro ao buscar todas as pontuações: {e}")
            return []

    @staticmethod
    def editar_frase(sentence_id, new_sentence, grammar_score, vocabulary_score, naturalness_score, punctuation_score):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Note: Atualizamos a frase e todas as notas (que podem ter sido re-avaliadas ou mantidas)
            query = """
            UPDATE sentences SET 
                sentence = ?, 
                grammar_score = ?, 
                vocabulary_score = ?, 
                naturalness_score = ?, 
                punctuation_score = ?, 
                updated_at = ?
            WHERE sentence_id = ?
            """
            cursor.execute(query, (
                new_sentence, 
                grammar_score, 
                vocabulary_score, 
                naturalness_score, 
                punctuation_score, 
                datetime.now(),
                sentence_id
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Erro ao editar frase com ID {sentence_id}: {e}")
            return False

    @staticmethod
    def apagar_frase(sentence_id):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM sentences WHERE sentence_id = ?"
            cursor.execute(query, (sentence_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Erro ao apagar frase com ID {sentence_id}: {e}")
            return False

# EXECUÇÃO INICIAL
if __name__ == "__main__":
    print("Banco configurado!")