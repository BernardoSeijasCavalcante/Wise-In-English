import streamlit as st
import pandas as pd
import random
import user_interface.utils.sidebar_model as sm

def app():

    st.title("Registro de Palavras")
    st.markdown("---")

    list = ["NEUTRO", "FORMAL", "INFORMAL"]

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(label="PALAVRA",key="palavra")
        st.text_input(label="SIGNIFICADO",key="significado")
        st.text_input(label="COMPLEMENTO",key="complemento")
        st.text_input(label="FORMALIDADE",key="formalidade")
        st.text_input(label="CLASSE GRAMATICAL",key="classe_gramatical")

        if st.button("INSERIR PALAVRAS"):
            st.text("inserir palavras")

    


    with col2:
        st.markdown(f"<table style='margin:0 auto; background-color: white;' width= '100%'><tr style='background-color: black ; color: white'><td style='text-align: center;'>PALAVRAS</td><td style='text-align: center; '>SIGNIFICADOS</td></tr><tr><td style='text-align: center;'>AFFORDABLE</td><td style='text-align: center; '>ACESSÍVEL/ECONÔMICO</td></tr><tr><td style='text-align: center;'>AFTERWARD</td><td style='text-align: center; '>DEPOIS</td></tr><tr><td style='text-align: center;'>ALWAYS</td><td style='text-align: center; '>SEMPRE</td></tr><tr><td style='text-align: center;'>AMAZING</td><td style='text-align: center; '>INCRÍVEL</td></tr><tr><td style='text-align: center;'>ANYWHERE</td><td style='text-align: center; '>QUALQUER LUGAR</td></tr></table>", unsafe_allow_html=True)
        st.text("")
        st.text("")
        st.text("")
        st.text("")

        st.markdown(f"<table style='margin:0 auto; background-color: white;' width= '100%'><tr><td style='text-align: center;'>DOES</td><td style='text-align: center; '>FAZER</td></tr></table>", unsafe_allow_html=True)

        st.text("")
        atualizar1, atualizar2, atualizar3 = st.columns([1, 1, 1])

        with atualizar2:
            if st.button("ATUALIZAR"):
                st.text("atualizar")

    sm.sidebar_load(st)
        
