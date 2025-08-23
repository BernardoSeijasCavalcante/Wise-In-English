import streamlit as st
import user_interface.utils.sidebar_model as sm

def app():
    #st.set_page_config(page_title = "", page_icon = "", layout = "centered")
    st.title("Inicio")

    st.write("Total de Palavras Descobertas: 0")
    st.write("Total de Palavras Aprendidas: 0")
    st.write("Total de Frases Criadas: 0")
    st.write("Média de Avaliação Geral: 0.0")
    st.write("Média de Avaliação em Gramática: 0.0")
    st.write("...")

    sm.sidebar_load(st)
    
