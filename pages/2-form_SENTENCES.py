import pymysql
from pydantic import BaseModel
from datetime import datetime

# CONFIGURAÇÃO DO BANCO DE DADOS
class Words(BaseModel):
    word_id: int = 0
    word: str
    translation: str
    description: str = ""
    formality_level: str = ""
    grammatical_class: str = ""
    user_id: int = 1


class Databese:
    server = 'localhost'
    database = 'wordDatabase'
    username = 'root'
    password = 'eduardo2005'


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

# FUNÇÕES PARA PALAVRAS
def adicionar_palavra(word):
    
    # Adiciona uma palavra na tabela 'palavras' se não existir
    # Retorna o ID da palavra
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT IGNORE INTO words (word) VALUES (%s)", (word,))
        conn.commit()
        cursor.execute("SELECT id FROM words WHERE word=%s", (word,))
        word_id = cursor.fetchone()['id']
    finally:
        cursor.close()
        conn.close()
    return word_id

# FUNÇÕES PARA FRASES
def adicionar_frase(word, frase, translation="", description="", formality_level="", grammatical_class="", avaliacao=10):
   
    # Adiciona uma nova frase associada a uma palavra no banco
    
    word_id = adicionar_palavra(word)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO frases 
            (word_id, frase, translation, description, formality_level, grammatical_class, avaliacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (word_id, frase, translation, description, formality_level, grammatical_class, avaliacao))
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

def buscar_frases(word):
    
    # Busca todas as frases associadas a uma palavra
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM words WHERE word=%s", (word,))
        result = cursor.fetchone()
        if not result:
            return []
        word_id = result['id']
        cursor.execute("SELECT * FROM frases WHERE word_id=%s ORDER BY created_at DESC", (word_id,))
        frases = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return frases

def palavra_aprendida(word):
    
    # Verifica se a word pode ser considerada "aprendida"
    # Critério: média de avaliações das frases > 7
    
    frases = buscar_frases(word)
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
        cursor.execute("SELECT * FROM words")
        todas = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    nao_aprendidas = []
    for p in todas:
        frases = buscar_frases(p['word'])
        if not frases:
            nao_aprendidas.append({"word": p['word'], "quantidade_frases": 0})
            continue
        media = sum(f['avaliacao'] for f in frases) / len(frases)
        if media <= 7:
            nao_aprendidas.append({"word": p['word'], "quantidade_frases": len(frases)})

    return nao_aprendidas

# FUNÇÕES DE APOIO PARA O FRONTEND
def _map_frase_row_to_ui(row):
    
    # Mapeia um registro de frase do banco para um formato amigável para o frontend
    
    return {
        "Frase": row.get("frase", ""),
        "Palavra": row.get("word", ""),
        "Tradução": row.get("translation", "") or "",
        "description": row.get("description", "") or "",
        "Grau de Formalidade": row.get("formality_level", "") or "",
        "Classe Gramatical": row.get("grammatical_class", "") or "",
    }

def buscar_frases_ui(word):
    
    # Busca frases formatadas para exibição no frontend
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT f.*, p.word AS word
            FROM frases f
            JOIN words p ON p.id = f.word_id
            WHERE p.word = %s
            ORDER BY f.created_at DESC
        """, (word,))
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return [_map_frase_row_to_ui(r) for r in rows]

def salvar_frase_ui(word, frase, translation="", description="", formality_level="", grammatical_class=""):
    
    # Salva uma frase e retorna os dados formatados para uso no frontend
    
    word_id = adicionar_palavra(word)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO frases 
            (word_id, frase, translation, description, formality_level, grammatical_class, avaliacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (word_id, frase, translation, description, formality_level, grammatical_class, 10))
        conn.commit()
        return {
            "Frase": frase,
            "Palavra": word,
            "Tradução": translation or "",
            "description": description or "",
            "Grau de Formalidade": formality_level or "",
            "Classe Gramatical": grammatical_class or "",
        }
    finally:
        cursor.close()
        conn.close()

def palavras_aleatorias_ui(limit=4):
    
    # Retorna até 'limit' palavras aleatórias que ainda não foram aprendidas
    
    base = buscar_palavras_nao_aprendidas()
    adaptada = [{"word": x["word"], "Qtd Frases": x["quantidade_frases"]} for x in base]
    if not adaptada:
        return []
    return random.sample(adaptada, min(limit, len(adaptada)))

def detalhes_da_palavra_ui(word):
    
    # Retorna os detalhes mais recentes de uma palavra (última frase adicionada)
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT f.translation, f.description, f.formality_level, f.grammatical_class
            FROM frases f
            JOIN words p ON p.id = f.word_id
            WHERE p.word = %s
            ORDER BY f.created_at DESC
            LIMIT 1
        """, (word,))
        row = cursor.fetchone() or {}
    finally:
        cursor.close()
        conn.close()
    return {
        "Tradução": (row.get("translation") if row else "") or "",
        "description": (row.get("description") if row else "") or "",
        "Grau de Formalidade": (row.get("formality_level") if row else "") or "",
        "Classe Gramatical": (row.get("grammatical_class") if row else "") or "",
    }

# EXECUÇÃO INICIAL
if __name__ == "__main__":
    print("Banco configurado!")
