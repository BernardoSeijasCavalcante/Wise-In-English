import streamlit as st
import pandas as pd
import random


# Configuração da página

st.set_page_config(page_title="Gerador de Frases", layout="wide")


# Inicialização do session_state

if "todas_palavras" not in st.session_state:
    st.session_state.todas_palavras = [
        {"Palavra": "book", "Qtd Frases": 3},
        {"Palavra": "run", "Qtd Frases": 5},
        {"Palavra": "happy", "Qtd Frases": 2},
        {"Palavra": "computer", "Qtd Frases": 4},
        {"Palavra": "play", "Qtd Frases": 6},
        {"Palavra": "fast", "Qtd Frases": 1}
    ]

if "frases_por_palavra" not in st.session_state:
    st.session_state.frases_por_palavra = {
        "book": [
            {"Frase": "I like to read books.", "Palavra": "book", "Tradução": "", "Complemento": "", "Grau de Formalidade": "", "Classe Gramatical": ""},
            {"Frase": "This book is interesting.", "Palavra": "book", "Tradução": "", "Complemento": "", "Grau de Formalidade": "", "Classe Gramatical": ""}
        ],
        "run": [],
        "happy": [],
        "computer": [],
        "play": [],
        "fast": []
    }

if "ultima_frase" not in st.session_state:
    st.session_state.ultima_frase = None

if "palavras_aleatorias" not in st.session_state:
    st.session_state.palavras_aleatorias = random.sample(st.session_state.todas_palavras, 4)


# Barra lateral - entrada de palavra

with st.sidebar:
    st.title("Wise-Englishman")
    st.markdown("---")
    st.subheader("Digite a palavra")
    palavra_input = st.text_input("", key="palavra_sidebar")
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
