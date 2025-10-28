import streamlit as st
import pandas as pd
import random
import user_interface.utils.sidebar_model as sm
from user_interface.utils.DB import UserRepository, WordRepository, SentenceRepository, Words, Sentences

# Instâncias
UserRepository = UserRepository()
db = SentenceRepository()

def app():
    wordRepository = WordRepository()
    
    # CSS para evitar que o dataframe quebre o layout
    st.markdown("""
    <style>
    [data-testid="column"] {
        overflow: visible !important;
    }
    [data-testid="stDataFrame"] {
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Registro de Palavras")
    st.markdown("---")

    # 🔹 Define proporção das colunas — mais espaço pro formulário
    col1, col2 = st.columns([1.2, 1])

    # 🔹 Recupera o usuário logado
    user_id = st.session_state.get("user_id", None)
    if not user_id:
        st.error("Usuário não identificado. Faça login novamente.")
        return

    # -------------------------------------------------------
    # LADO ESQUERDO — FORMULÁRIO DE INSERÇÃO
    # -------------------------------------------------------
    with col1:
        palavra = st.text_input(label="PALAVRA", key="palavra")
        significado = st.text_input(label="SIGNIFICADO", key="significado")
        complemento = st.text_input(label="COMPLEMENTO", key="complemento")
        formalidade = st.text_input(label="FORMALIDADE", key="formalidade")
        classe_gramatical = st.text_input(label="CLASSE GRAMATICAL", key="classe_gramatical")

        if st.button("INSERIR PALAVRAS"):
            if not palavra or not significado:
                st.error("PALAVRA e SIGNIFICADO são obrigatórios.")
            else:
                nova_palavra = Words(
                    word=palavra,
                    translation=significado,
                    description=complemento,
                    formality_level=formalidade,
                    grammatical_class=classe_gramatical,
                    user_id=user_id
                )
                wordRepository.insert_word(nova_palavra)
                st.success("Palavra registrada com sucesso!")

    # -------------------------------------------------------
    # LADO DIREITO — TABELA DE PALAVRAS DO USUÁRIO
    # -------------------------------------------------------
    with col2:
        results = wordRepository.get_words_by_user(user_id)

        if not results:
            st.info("Nenhuma palavra registrada ainda.")
        else:
            # Converte resultados em DataFrame
            try:
                df = pd.DataFrame(results, columns=["PALAVRAS", "SIGNIFICADOS"])
            except Exception:
                df = pd.DataFrame(
                    [(r.word, r.translation) for r in results],
                    columns=["PALAVRAS", "SIGNIFICADOS"]
                )

            # Aplica estilo visual dark
            styled_df = df.style.set_table_styles([
                {'selector': 'th',
                 'props': [('background-color', '#000'),
                           ('color', 'white'),
                           ('text-align', 'center'),
                           ('font-weight', 'bold')]},
                {'selector': 'td',
                 'props': [('background-color', '#1e1e1e'),
                           ('color', 'white'),
                           ('border', '1px solid #444'),
                           ('text-align', 'center'),
                           ('padding', '8px')]},
                {'selector': 'tr:nth-child(even)',
                 'props': [('background-color', '#2b2b2b')]}
            ])

            # Exibe a tabela ajustada
            st.dataframe(styled_df, height=240)

        st.text("")
        atualizar1, atualizar2, atualizar3 = st.columns([1, 1, 1])
        with atualizar2:
            if st.button("ATUALIZAR"):
                st.rerun()

    sm.sidebar_load(st)
