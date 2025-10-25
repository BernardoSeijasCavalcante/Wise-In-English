import streamlit as st

import form_LOGIN as login
import main as main
import user_interface.main as m
import user_interface.pages_aux.form_WORDS as words
import user_interface.pages_aux.form_SENTENCES as sentences


if "start" not in st.session_state:
    st.session_state.start = "No"

def app():

    st.session_state.start = "Yes"

    st.set_page_config(page_title="Wise-In-English", page_icon="🧠", layout="centered")
    if "page" not in st.session_state:
        st.session_state.page = "init"

    if st.session_state.page == "init":
        user_number = 0
        word_number = 0
        sentences_number = 0

        rating = 0.0
        functionality_rating = 0.0
        usefulness_rating = 0.0
        IA_rating = 0.0

        st.title("Bem-Vindo(a)!")
        texto_intr = f"""
            <div style='text-align: justify;'>
            Este é o <div style='display:inline;color: red;'>Wise</div> In <div style='display:inline;color:blue;'>English</div>, uma plataforma dedicada a estudantes que querem aprender inglês. Se você tem dificuldades com gramática, pontuação, vocabulário ou com a naturalidade na comunicação em inglês, este é o caminho certo. O processo de aprendizado consiste na elaboração de frases e no registro de palavras com o auxílio e a avaliação por inteligência artificial. O estudante registra suas frases a partir das palavras previamente cadastradas e recebe um feedback com uma média de seu desempenho nos quatro tópicos de avaliação mencionados acima.
            </div>
        """

        st.markdown(texto_intr, unsafe_allow_html=True)

        login_button = """
        <style>
            div.stButton{
                display: flex;
                justify-content: center;
            }
            div.stButton > button{
                border-radius: 15px;
                color: white;
                background-color: blue;
            }
        </style>
        """

        st.markdown(login_button, unsafe_allow_html=True)

        if st.button("Entre para Continuar!"):
            st.session_state.page="login"
            st.rerun()

        project_performance = f"""
        <hr>
            <div style='font-weight: bold;font-size: 30px;'>Desempenho do Projeto</div>
            <div style='height: 180px;display:flex; justify-content:center;'>
                <div style='margin: 2%;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius: 50px; background-color: red;height: 100%; width:30%;float: left;'>
                    <div style='font-size:80px; font-weight: bold;'>{user_number}</div>
                    <div style='font-size:30px; font-weight: bold;'>USUÁRIOS</div>
                </div>
                <div style='margin: 2%;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius: 50px; background-color: white;height: 100%; width:30%;color: black;float: left;'>
                    <div style='margin-bottom:-15px;font-size:80px; font-weight: bold;'>{word_number}</div>
                    <div style='font-size:20px; font-weight: bold;text-align:center;'>PALAVRAS REGISTRADAS</div>
                </div>
                <div style='margin: 2%;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius: 50px; background-color: blue;height: 100%; width:30%;float: left;'>
                    <div style='margin-bottom:-15px;font-size:80px; font-weight: bold;'>{sentences_number}</div>
                    <div style='width: 60%;font-size:20px; font-weight: bold;text-align:center;'>FRASES REGISTRADAS</div>
                </div>
            </div>
            <br>z
            <br>
            <div style='height: 180px;display:flex; align-items:center;justify-content:center;'>
                <div style='border-radius:50px;background-color: #0d0e0e;width: 50%; height: 100%; display:flex;flex-direction:column; align-items:center;justify-content:center;'>
                    <div style='font-size:50px;text-shadow: 0px 2px 10px white;'>{rating}/10.0</div>
                    <div style='font-size:20px;'>Avaliação Geral dos Usuários</div>
                </div>
            </div>
            <div style='height: 180px;display:flex; justify-content:center;'>
                <div style='margin: 2%;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius: 50px; background-color: #0d0e0e;height: 100%; color:white; width:30%;float: left;'>
                    <div style='font-size:50px;text-shadow: 0px 2px 10px white;'>{usefulness_rating}/10.0</div>
                    <div style='font-size:20px;'>Avaliação da Utilidade</div>
                </div>
                <div style='margin: 2%;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius: 50px; background-color: #0d0e0e;height: 100%; width:30%;color: white;float: left;'>
                    <div style='font-size:50px;text-shadow: 0px 2px 10px white;'>{functionality_rating}/10.0</div>
                    <div style='font-size:20px;text-align:center;'>Avaliação da Funcionalidade</div>
                </div>
                <div style='margin: 2%;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius: 50px; background-color: #0d0e0e;height: 100%; width:30%;color:white;float: left;'>
                    <div style='font-size:50px;text-shadow: 0px 2px 10px white;'>{IA_rating}/10.0</div>
                    <div style='width: 60%;font-size:15px;text-align:center;'>Avaliação do Nosso Modelo de IA</div>
                </div>
            </div>
            <br>
            <hr>
        """
        st.markdown(project_performance, unsafe_allow_html=True)
    elif st.session_state.page == "login":
        login.login()
    elif st.session_state.page == "signup":
        login.register()
    elif st.session_state.page == "begin":
        m.app()
    elif st.session_state.page == "form_WORD":
        words.app()
    elif st.session_state.page == "form_SENTENCES":
        sentences.app()

app()

