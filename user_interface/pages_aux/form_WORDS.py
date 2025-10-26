import streamlit as st
import pandas as pd
import random
import user_interface.utils.sidebar_model as sm
from user_interface.utils.DB import UserRepository, WordRepository, SentenceRepository
# 1. Instancie o banco de dados (assumindo que Database está acessível)
UserRepository = UserRepository()
WordRepository = WordRepository()
SentenceRepository = SentenceRepository()

def app():

    WordRepository = WordRepository()
    
    st.title("Registro de Palavras")
    st.markdown("---")


    list = ["NEUTRO", "FORMAL", "INFORMAL"]

    col1, col2 = st.columns(2)

    with col1:
        palavra = st.text_input(label="PALAVRA",key="palavra")
        significado = st.text_input(label="SIGNIFICADO",key="significado")
        complemento = st.text_input(label="COMPLEMENTO",key="complemento")
        formalidade = st.text_input(label="FORMALIDADE",key="formalidade")
        classe_gramatical = st.text_input(label="CLASSE GRAMATICAL",key="classe_gramatical")

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
                    user_id=1
                )

                WordRepository.insert_word(nova_palavra)

                st.success("Palavra registrada com sucesso!")
            

    with col2:
        matriz = [[0 for j in range(2)] for i in range(5)]
        results = WordRepository.get_random_word()

        guia = 0

        for row in results:
            matriz[guia][0] = row[0]
            matriz[guia][1] = row[1]
            guia += 1

        st.markdown(f"<table style='margin:0 auto; background-color: white;' width= '100%'><tr style='background-color: black ; color: white'><td style='text-align: center;'>PALAVRAS</td><td style='text-align: center; '>SIGNIFICADOS</td></tr><tr><td style='text-align: center;'>{matriz[0][0]}</td><td style='text-align: center; '>{matriz[0][1]}</td></tr><tr><td style='text-align: center;'>{matriz[1][0]}</td><td style='text-align: center; '>{matriz[1][1]}</td></tr><tr><td style='text-align: center;'>{matriz[2][0]}</td><td style='text-align: center; '>{matriz[2][1]}</td></tr><tr><td style='text-align: center;'>{matriz[3][0]}</td><td style='text-align: center; '>{matriz[3][1]}</td></tr><tr><td style='text-align: center;'>{matriz[4][0]}</td><td style='text-align: center; '>{matriz[4][1]}</td></tr></table>", unsafe_allow_html=True)
        st.text("")
        st.text("")
        st.text("")
        st.text("")

        results = WordRepository.get_random_word()

        guia = 0
        for row in results:
            matriz[guia][0] = row[0]
            matriz[guia][1] = row[1]
            guia += 1

        st.markdown(f"<table style='margin:0 auto; background-color: white;' width= '100%'><tr><td style='text-align: center;'>{matriz[0][0]}</td><td style='text-align: center; '>{matriz[0][1]}</td></tr></table>", unsafe_allow_html=True)

        st.text("")
        atualizar1, atualizar2, atualizar3 = st.columns([1, 1, 1])

        with atualizar2:
            if st.button("ATUALIZAR"):
                st.text("atualizar")

    sm.sidebar_load(st)
        
