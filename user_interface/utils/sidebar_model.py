def sidebar_load(st):
    st.sidebar.title("Ambiente Virtual de Estudos")

    selected_page = st.sidebar.radio("", ["Desempenho Geral","Registro de Palavras","Registro de Frases"])

    if selected_page == "Registro de Palavras" and st.session_state.page != "form_WORD":
        st.session_state.page = "form_WORD"
        st.rerun()
    elif selected_page == "Registro de Frases"  and st.session_state.page != "form_SENTENCES":
        st.session_state.page = "form_SENTENCES"
        st.rerun()
    elif selected_page == "Desempenho Geral" and st.session_state.page != "begin":
        st.session_state.page = "begin"
        st.rerun()
    