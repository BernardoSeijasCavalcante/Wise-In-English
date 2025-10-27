import streamlit as st
import pandas as pd
import random
import openai
import json
from openai import OpenAI
import user_interface.utils.sidebar_model as sm

# Importando as classes do seu arquivo de banco de dados
from user_interface.utils.DB import UserRepository, WordRepository, SentenceRepository,Words,Sentences
# 1. Instancie o banco de dados (assumindo que Database está acessível)
# Configuração da chave da API da OpenAI
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ Chave da API da OpenAI não encontrada. Configure em `secrets.toml`.")

def get_sentence_scores(sentence_text: str):
    """
    Função para obter as pontuações da frase usando a API da OpenAI.
    """
    if not sentence_text or not sentence_text.strip():
        st.warning("A frase não pode estar vazia.")
        return None

    system_prompt = (
        "Você é um avaliador de proficiência em inglês. Sua tarefa é analisar a frase fornecida "
        "e atribuir uma nota de 0.0 a 10.0 para cada categoria: gramática, vocabulário, naturalidade e pontuação. "
        "A saída DEVE ser um objeto JSON estritamente conforme os atributos a seguir, sem texto adicional: "
        "grammar_score, vocabulary_score, naturalness_score, punctuation_score and explanation "
        "(Uma explicação detalhada do porquê de cada nota. Descreva a explanation como um texto em prosa e não como um corpo json)."
    )
    
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Avalie a seguinte frase em inglês: '{sentence_text}'"}
            ],
            response_format={"type": "json_object"},
        )
        json_output = response.choices[0].message.content
        return json.loads(json_output)
        
    except Exception as e:
        st.error(f"❌ Erro ao chamar a API da OpenAI: {e}")
        return None

def app():
    st.set_page_config(page_title="Gerador de Frases", layout="wide")
    st.title("📝 Gerador de Frases com Avaliação IA")

    db = SentenceRepository()

    # --- Inicialização do Session State ---
    if "todas_palavras" not in st.session_state:
        st.session_state.todas_palavras = db.buscar_palavras_nao_aprendidas()

    if "frases_por_palavra" not in st.session_state:
        st.session_state.frases_por_palavra = {}

    if "palavras_aleatorias" not in st.session_state:
        todas = st.session_state.todas_palavras
        if len(todas) >= 4:
            st.session_state.palavras_aleatorias = random.sample(todas, 4)
        else:
            st.session_state.palavras_aleatorias = todas
    
    # --- Barra Lateral (Sidebar) ---
    with st.sidebar:
        sm.sidebar_load(st)
        st.header("Wise Englishman")
        st.subheader("1. Selecione ou Digite uma Palavra")
        palavra_input = st.text_input(
            "Palavra em inglês", 
            key="palavra_sidebar", 
            help="Digite a palavra que você quer praticar."
        ).strip().lower()

        # Carrega as frases da palavra selecionada no session_state
        if palavra_input and palavra_input not in st.session_state.frases_por_palavra:
            with st.spinner("Buscando frases..."):
                buscar_sentences = db.buscar_frases(palavra_input)
                st.session_state.frases_por_palavra[palavra_input] = [
                    {"ID": f[0], "Frase": f[1], "Gramática": f[2], "Vocabulário": f[3], "Naturalidade": f[4], "Pontuação": f[5]}
                    for f in buscar_sentences
                ]

    # --- Área Principal ---
    st.subheader("Palavras Aleatórias para Inspiração")
    if st.button("🔄 Sortear Novas Palavras"):
        todas = st.session_state.todas_palavras
        if len(todas) >= 4:
            st.session_state.palavras_aleatorias = random.sample(todas, 4)
        else:
            st.session_state.palavras_aleatorias = todas
        st.rerun()

    df_palavras = pd.DataFrame(st.session_state.palavras_aleatorias)
    # Renomeando colunas para melhor apresentação
    df_palavras.rename(columns={'word': 'Palavra', 'quantidade_frases': 'Qtd. Frases'}, inplace=True)
    st.dataframe(df_palavras, use_container_width=True, hide_index=True)
    st.markdown("---")

    if not palavra_input:
        st.info("👋 Bem-vindo! Digite uma palavra na barra lateral à esquerda para começar a praticar.")
        return

    # --- Seções que dependem de uma palavra ter sido inserida ---
    st.subheader(f"Detalhes sobre: **{palavra_input}**")
    detalhes = db.detalhes_da_palavra(Words(word=palavra_input, translation=""))
    if detalhes:
        col_d1, col_d2, col_d3 = st.columns(3)
        col_d1.metric("Tradução", detalhes[0])
        col_d2.metric("Classe", detalhes[3])
        col_d3.metric("Formalidade", detalhes[2])
        st.metric("Descrição", detalhes[1])
    else:
        st.warning("Palavra não encontrada no banco de dados. Adicione-a primeiro.")
    st.markdown("---")

    st.subheader("2. Adicione uma Nova Frase")
    frase_input = st.text_area("Digite sua frase em inglês aqui:", key="frase_input", height=100)

    if st.button("💾 Salvar e Avaliar Nova Frase", type="primary", use_container_width=True):
        word_id_aux = db.buscar_word_id(palavra_input)
        if not word_id_aux:
            st.error("Palavra não encontrada no banco de dados. Não é possível salvar a frase.")
        elif not frase_input:
            st.warning("⚠️ Por favor, digite uma frase antes de salvar.")
        else:
            with st.spinner("🤖 Avaliando a frase com a IA..."):
                scores = get_sentence_scores(frase_input)
            if scores:
                s_obj = Sentences(
                    word_id=word_id_aux, sentence=frase_input,
                    grammar_score=scores["grammar_score"], vocabulary_score=scores["vocabulary_score"],
                    naturalness_score=scores["naturalness_score"], punctuation_score=scores["punctuation_score"]
                )
                if db.adicionar_frase(s_obj):
                    
                    st.session_state.messages.append({"role": "user", "content": frase_input})              
                    st.session_state.messages.append({"role": "assistant", "content": scores["explanation"]})              
                    
                    st.success("✅ Frase salva e avaliada com sucesso!")
                    st.session_state.frases_por_palavra.pop(palavra_input, None) # Limpa cache
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar a frase no banco de dados.")
            else:
                st.error("❌ Não foi possível obter as notas da IA. A frase não foi salva.")
    st.markdown("---")

    # --- Seção de Gerenciamento de Frases (CRUD) ---
    st.subheader("3. Gerencie Suas Frases")
    if palavra_input in st.session_state.frases_por_palavra:
        frases_atuais = st.session_state.frases_por_palavra[palavra_input]
        if frases_atuais:
            df_frases = pd.DataFrame(frases_atuais)
            df_frases.insert(0, "Selecionar", False) # Adiciona coluna de seleção

            edited_df = st.data_editor(
                df_frases,
                key=f"editor_frases_{palavra_input}",
                column_config={
                    "Selecionar": st.column_config.CheckboxColumn("Selecionar", required=True),
                    "ID": st.column_config.Column("ID", disabled=True),
                    "Frase": st.column_config.TextColumn("Frase", width="large", required=True),
                    "Gramática": st.column_config.NumberColumn("Gramática", disabled=True, format="%.1f"),
                    "Vocabulário": st.column_config.NumberColumn("Vocabulário", disabled=True, format="%.1f"),
                    "Naturalidade": st.column_config.NumberColumn("Naturalidade", disabled=True, format="%.1f"),
                    "Pontuação": st.column_config.NumberColumn("Pontuação", disabled=True, format="%.1f"),
                },
                hide_index=True, use_container_width=True
            )

            selected_rows = edited_df[edited_df["Selecionar"]]
            col_edit, col_delete, col_reval = st.columns(3)

            with col_edit:
                if st.button("✏️ Editar Frase", disabled=len(selected_rows) != 1, use_container_width=True):
                    original_row = df_frases.loc[selected_rows.index[0]]
                    edited_row = selected_rows.iloc[0]
                    if original_row["Frase"] != edited_row["Frase"]:
                        with st.spinner("🤖 Reavaliando com a IA..."):
                            re_scores = get_sentence_scores(edited_row["Frase"])
                        if re_scores:
                            db.editar_frase(
                                int(edited_row["ID"]), edited_row["Frase"], float(re_scores["grammar_score"]),
                                float(re_scores["vocabulary_score"]), float(re_scores["naturalness_score"]),
                                float(re_scores["punctuation_score"])
                            )
                            st.success("✅ Frase editada com sucesso!")
                            st.session_state.frases_por_palavra.pop(palavra_input, None)
                            st.rerun()
                        else:
                            st.error("❌ Falha na reavaliação. Edição cancelada.")
                    else:
                        st.info("ℹ️ Nenhuma alteração detectada no texto da frase.")

            with col_delete:
                if st.button("🗑️ Apagar Frase(s)", disabled=len(selected_rows) == 0, use_container_width=True):
                    st.session_state['phrases_to_delete'] = selected_rows["ID"].tolist()
                    st.rerun()

            with col_reval:
                 if st.button("🔄 Reavaliar Notas", disabled=len(selected_rows) != 1, use_container_width=True):
                    row_data = selected_rows.iloc[0]
                    with st.spinner("🤖 Reavaliando com a IA..."):
                        re_scores = get_sentence_scores(row_data["Frase"])
                    if re_scores:
                        db.editar_frase(
                            int(row_data["ID"]), row_data["Frase"], float(re_scores["grammar_score"]),
                            float(re_scores["vocabulary_score"]), float(re_scores["naturalness_score"]),
                            float(re_scores["punctuation_score"])
                        )
                        st.success("✅ Notas reavaliadas com sucesso!")
                        st.session_state.frases_por_palavra.pop(palavra_input, None)
                        st.rerun()

            # Lógica de confirmação de exclusão
            if 'phrases_to_delete' in st.session_state and st.session_state.phrases_to_delete:
                ids_para_apagar = st.session_state['phrases_to_delete']
                st.warning(f"Você tem certeza que deseja apagar {len(ids_para_apagar)} frase(s)?")
                
                confirm_col, cancel_col = st.columns(2)
                if confirm_col.button("Sim, apagar", type="primary", use_container_width=True):
                    success_count = sum(1 for sid in ids_para_apagar if db.apagar_frase(sid))
                    st.success(f"🗑️ {success_count} frase(s) apagada(s) com sucesso!")
                    del st.session_state['phrases_to_delete']
                    st.session_state.frases_por_palavra.pop(palavra_input, None)
                    st.rerun()
                if cancel_col.button("Cancelar", use_container_width=True):
                    del st.session_state['phrases_to_delete']
                    st.rerun()
        else:
            st.info("Nenhuma frase cadastrada para esta palavra ainda. Adicione uma acima!")
    
    st.title("AI Teacher")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state:
        st.session_state.messages = []
        role = "Você é um assistente especialista em inglês que deve auxiliar estudantes na elaboração de frases gramaticalmente corretas, naturais e que demonstram um vasto repertório de palavras."
        st.session_state.messages.append({"role": "system", "content": role})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("No que você está pensando?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
if __name__ == "__main__":
    app()
