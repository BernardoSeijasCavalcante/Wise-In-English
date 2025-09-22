from pydantic import BaseModel
import pymssql
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
    
    # FUNÇÕES PARA PALAVRAS
    def adicionar_palavra(palavra):
        
        # Adiciona uma palavra na tabela 'palavras' se não existir
        # Retorna o ID da palavra
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT IGNORE INTO palavras (palavra) VALUES (%s)", (palavra,))
            conn.commit()
            cursor.execute("SELECT id FROM palavras WHERE palavra=%s", (palavra,))
            palavra_id = cursor.fetchone()['id']
        finally:
            cursor.close()
            conn.close()
        return palavra_id

    # FUNÇÕES PARA FRASES
    def adicionar_frase(palavra, frase, traducao="", complemento="", grau_formalidade="", classe_gramatical="", avaliacao=10):
    
        # Adiciona uma nova frase associada a uma palavra no banco
        
        palavra_id = adicionar_palavra(palavra)
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO frases 
                (palavra_id, frase, traducao, complemento, grau_formalidade, classe_gramatical, avaliacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (palavra_id, frase, traducao, complemento, grau_formalidade, classe_gramatical, avaliacao))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def atualizar_avaliacao(frase_id, nova_avaliacao):
        
        # Atualiza a avaliação de uma frase específica
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE frases 
                SET avaliacao=%s, updated_at=%s 
                WHERE id=%s
            """, (nova_avaliacao, datetime.now(), frase_id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def buscar_frases(palavra):
        
        # Busca todas as frases associadas a uma palavra
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM palavras WHERE palavra=%s", (palavra,))
            result = cursor.fetchone()
            if not result:
                return []
            palavra_id = result['id']
            cursor.execute("SELECT * FROM frases WHERE palavra_id=%s ORDER BY created_at DESC", (palavra_id,))
            frases = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
        return frases

    def palavra_aprendida(palavra):
        
        # Verifica se a palavra pode ser considerada "aprendida"
        # Critério: média de avaliações das frases > 7
        
        frases = buscar_frases(palavra)
        if not frases:
            return False
        media = sum(f['avaliacao'] for f in frases) / len(frases)
        return media > 7

    def buscar_palavras_nao_aprendidas():
        
        # Retorna uma lista de palavras que ainda não foram aprendidas
        # (média de avaliação <= 7)
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM palavras")
            todas = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        nao_aprendidas = []
        for p in todas:
            frases = buscar_frases(p['palavra'])
            if not frases:
                nao_aprendidas.append({"palavra": p['palavra'], "quantidade_frases": 0})
                continue
            media = sum(f['avaliacao'] for f in frases) / len(frases)
            if media <= 7:
                nao_aprendidas.append({"palavra": p['palavra'], "quantidade_frases": len(frases)})

        return nao_aprendidas

    # FUNÇÕES DE APOIO PARA O FRONTEND
    def _map_frase_row_to_ui(row):
        
        # Mapeia um registro de frase do banco para um formato amigável para o frontend
        
        return {
            "Frase": row.get("frase", ""),
            "Palavra": row.get("palavra", ""),
            "Tradução": row.get("traducao", "") or "",
            "Complemento": row.get("complemento", "") or "",
            "Grau de Formalidade": row.get("grau_formalidade", "") or "",
            "Classe Gramatical": row.get("classe_gramatical", "") or "",
        }

    def buscar_frases_ui(palavra):
        
        # Busca frases formatadas para exibição no frontend
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT f.*, p.palavra AS palavra
                FROM frases f
                JOIN palavras p ON p.id = f.palavra_id
                WHERE p.palavra = %s
                ORDER BY f.created_at DESC
            """, (palavra,))
            rows = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
        return [_map_frase_row_to_ui(r) for r in rows]

    def salvar_frase_ui(palavra, frase, traducao="", complemento="", grau_formalidade="", classe_gramatical=""):
        
        # Salva uma frase e retorna os dados formatados para uso no frontend
        
        palavra_id = adicionar_palavra(palavra)
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO frases 
                (palavra_id, frase, traducao, complemento, grau_formalidade, classe_gramatical, avaliacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (palavra_id, frase, traducao, complemento, grau_formalidade, classe_gramatical, 10))
            conn.commit()
            return {
                "Frase": frase,
                "Palavra": palavra,
                "Tradução": traducao or "",
                "Complemento": complemento or "",
                "Grau de Formalidade": grau_formalidade or "",
                "Classe Gramatical": classe_gramatical or "",
            }
        finally:
            cursor.close()
            conn.close()

    def palavras_aleatorias_ui(limit=4):
        
        # Retorna até 'limit' palavras aleatórias que ainda não foram aprendidas
        
        base = buscar_palavras_nao_aprendidas()
        adaptada = [{"Palavra": x["palavra"], "Qtd Frases": x["quantidade_frases"]} for x in base]
        if not adaptada:
            return []
        return random.sample(adaptada, min(limit, len(adaptada)))

    def detalhes_da_palavra_ui(palavra):
        
        # Retorna os detalhes mais recentes de uma palavra (última frase adicionada)
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT f.traducao, f.complemento, f.grau_formalidade, f.classe_gramatical
                FROM frases f
                JOIN palavras p ON p.id = f.palavra_id
                WHERE p.palavra = %s
                ORDER BY f.created_at DESC
                LIMIT 1
            """, (palavra,))
            row = cursor.fetchone() or {}
        finally:
            cursor.close()
            conn.close()
        return {
            "Tradução": (row.get("traducao") if row else "") or "",
            "Complemento": (row.get("complemento") if row else "") or "",
            "Grau de Formalidade": (row.get("grau_formalidade") if row else "") or "",
            "Classe Gramatical": (row.get("classe_gramatical") if row else "") or "",
        }