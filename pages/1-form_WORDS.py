import streamlit as st
import pandas as pd
from DB import Words, insert_word, get_latest_words, get_random_updated_word
from datetime import datetime


st.title("Registro de Palavras")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    palavra = st.text_input("PALAVRA")
    significado = st.text_input("SIGNIFICADO")
    complemento = st.text_input("COMPLEMENTO")
    formalidade = st.text_input("FORMALIDADE")
    gramatical = st.text_input("CLASSE GRAMATICAL")

    if st.button("INSERIR PALAVRAS"):
        if not palavra or not significado:
            st.error("PALAVRA e SIGNIFICADO são obrigatórios.")
        else:
            nova_palavra = Words(
                word=palavra,
                translation=significado,
                description=complemento,
                formality_level=formalidade,
                grammatical_class=gramatical,
                user_id=1
            )
            insert_word(nova_palavra)

with col2:
    palavras = get_latest_words()
    if palavras:
        df = pd.DataFrame(palavras)
        st.dataframe(df.reset_index(drop=True))
    else:
        st.write("Nenhuma palavra encontrada.")

    st.markdown("---")

    palavra_aleatoria = get_random_updated_word()
    if palavra_aleatoria:
        st.write(f"<table style='margin:0 auto; background-color: white;' width= '100%'><tr><td style='text-align: center; color: black'>{palavra_aleatoria['word']}</td><td style='text-align: center; color: black'>{palavra_aleatoria['translation']}</td></tr></table>", unsafe_allow_html=True)
    else:
        st.write("Nenhuma palavra atualizada encontrada.")

    st.markdown("")
    st.markdown("")
    st.markdown("")
    
    if st.button("ATUALIZAR"):
        try:
            st.experimental_rerun()
        except AttributeError:
            st.rerun()
