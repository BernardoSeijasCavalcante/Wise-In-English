import streamlit as st
import pandas as pd
import random
import user_interface.utils.sidebar_model as sm
from user_interface.utils.DB import Words, Database

db = Database()

def app():
    st.set_page_config(page_title="Gerador de Frases", layout="wide")

    total_word = db.buscar_palavras_nao_aprendidas()
    buscar_sentences = db.buscar_frases()


    if "todas_palavras" not in st.session_state:
        st.session_state.todas_palavras = []

        for f in total_word:
            st.session_state.todas_palavras.append({"Palavra": f[0], "Qtd Frases": f[1]})

    if "frases_por_palavra" not in st.session_state:
        st.session_state.frases_por_palavra = []

        for f in buscar_sentences:
            st.session_state.frases_por_palavra.append({"Frase": f[0]})


    if "ultima_frase" not in st.session_state:
        st.session_state.ultima_frase = None

    if "palavras_aleatorias" not in st.session_state:
        st.session_state.palavras_aleatorias = random.sample(st.session_state.todas_palavras, 4)


    # Barra lateral - entrada de palavra

    with st.sidebar:
        sm.sidebar_load(st)
        
        st.subheader("Digite a palavra")
        palavra_input = st.text_input("palavra", key="palavra_sidebar")
        if palavra_input:
            st.markdown("✅ Entrada realizada com sucesso")


    # Área principal - palavras aleatórias

    st.subheader("Palavras Aleatórias")
    col_refresh, col_blank = st.columns([1, 5])
    with col_refresh:
        if st.button("🔄 Sortear Novas Palavras"):
            st.session_state.palavras_aleatorias = random.sample(st.session_state.todas_palavras, 4)

    df_palavras = pd.DataFrame(st.session_state.palavras_aleatorias)
    st.dataframe(df_palavras, use_container_width=True)

    st.markdown("---")


    # Área principal - entrada de frases

    frase_input = st.text_area("Digite a frase em inglês:")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        # Botão para salvar a frase
        if st.button("💾 Salvar Frase"):
            if palavra_input and frase_input:
                nova_frase = {
                    "Frase": frase_input,
                    "Palavra": palavra_input,
                    "Tradução": "",
                    "Complemento": "",
                    "Grau de Formalidade": "",
                    "Classe Gramatical": ""
                }
                if palavra_input not in st.session_state.frases_por_palavra:
                    st.session_state.frases_por_palavra[palavra_input] = []
                st.session_state.frases_por_palavra[palavra_input].append(nova_frase)
                st.session_state.ultima_frase = nova_frase
                st.success("✅ Frase salva com sucesso!")
            else:
                st.warning("⚠️ Preencha a palavra e a frase antes de salvar.")

    with col_btn2:
        # Botão para resgatar a última frase salva
        if st.button("📜 Resgatar Última Frase"):
            if st.session_state.ultima_frase:
                st.info(f"Última frase: {st.session_state.ultima_frase['Frase']}")
            else:
                st.warning("Nenhuma frase salva ainda.")

    st.markdown("---")


    # Área de detalhes da palavra

    if palavra_input:
        st.subheader("Detalhes da Palavra (preenchidos pelo backend)")
        col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
        with col_d1:
            st.text_input("Palavra", palavra_input, disabled=True)
        with col_d2:
            st.text_input("Tradução", "", disabled=True)
        with col_d3:
            st.text_input("Complemento", "", disabled=True)
        with col_d4:
            st.text_input("Grau de Formalidade", "", disabled=True)
        with col_d5:
            st.text_input("Classe Gramatical", "", disabled=True)

        st.markdown("---")


    # Exibe as frases da palavra selecionada

    st.subheader("Frases da Palavra Selecionada")
    if palavra_input in st.session_state.frases_por_palavra:
        df_frases = pd.DataFrame(st.session_state.frases_por_palavra[palavra_input])
        if not df_frases.empty:
            st.dataframe(df_frases, use_container_width=True)
        else:
            st.info("Nenhuma frase para esta palavra ainda.")
    else:
        st.info("Digite uma palavra para ver suas frases.")

    