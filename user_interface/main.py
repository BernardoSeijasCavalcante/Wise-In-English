import streamlit as st
import user_interface.utils.sidebar_model as sm
from user_interface.utils.DB import Words, Database, Sentences
import pandas as pd
import plotly.express as px

# 1. Instancie o banco de dados (assumindo que Database está acessível)
db = Database()

def app():
    # Configuração de página para melhor visualização (pode ser globalmente no main.py)
    # st.set_page_config(layout="wide") # Use 'wide' para dashboards

    st.title("🏡 Dashboard do Estudante")
    st.markdown("Acompanhe seu progresso e o desempenho das suas frases.")

    # --- 1. Carregar Métricas ---
    metrics = db.get_dashboard_metrics()
    
    # Simula a 'Total de Palavras Aprendidas' (assumindo que palavras com > 3 frases são 'aprendidas')
    # Este é um cálculo mais complexo, por simplicidade, vamos usar um valor fictício ou adicionar a função
    # Se você quiser a função de BD, diga-me, mas por hora, vamos simular ou usar total_palavras.
    total_palavras = metrics["total_palavras"]
    total_frases = metrics["total_frases"]
    
    # 2. Exibição das Métricas Principais (Usando st.columns e st.metric)
    
    st.header("📈 Seus Números")
    col1, col2, col3 = st.columns(3)
    
    # Métrica de Palavras
    with col1:
        st.metric(
            label="Total de Palavras Descobertas 💡", 
            value=f"{total_palavras}", 
            delta_color="off"
        )
        
    # Métrica de Frases
    with col2:
        st.metric(
            label="Total de Frases Criadas ✍️", 
            value=f"{total_frases}", 
            delta_color="off"
        )

    # Métrica de Média Geral
    with col3:
        # Use o total de frases para dar contexto à média
        if total_frases > 0:
            st.metric(
                label="Média de Avaliação Geral ⭐", 
                value=f"{metrics['media_geral']:.2f}",
                # Podemos usar um delta se tivermos um valor anterior
                delta="10.0", # Valor fictício
                delta_color="normal"
            )
        else:
             st.metric(label="Média de Avaliação Geral ⭐", value="N/A")

    st.markdown("---")

    # --- 3. Média de Avaliações por Categoria ---
    
    st.header("📊 Desempenho por Habilidade")
    
    col4, col5, col6, col7 = st.columns(4)
    
    with col4:
        st.metric(label="Gramática (G) 📚", value=f"{metrics['media_gramatica']:.2f}")
    
    with col5:
        st.metric(label="Vocabulário (V) 🔠", value=f"{metrics['media_vocabulario']:.2f}")

    with col6:
        st.metric(label="Naturalidade (N) 🗣️", value=f"{metrics['media_naturalidade']:.2f}")

    with col7:
        st.metric(label="Pontuação (P) ❕", value=f"{metrics['media_pontuacao']:.2f}")

    st.markdown("---")

    # --- 4. Visualização de Dados (Gráficos) ---
    
    st.header("Gráficos de Desempenho")
    
    scores_data = db.get_all_sentence_scores()
    
    if scores_data:
        df_scores = pd.DataFrame(scores_data)
        
        # Gráfico 1: Desempenho Médio por Categoria (Gráfico de Barras)
        st.subheader("Média de Notas por Habilidade")
        avg_df = pd.DataFrame({
            'Habilidade': ['Gramática', 'Vocabulário', 'Naturalidade', 'Pontuação'],
            'Média': [metrics['media_gramatica'], metrics['media_vocabulario'], 
                      metrics['media_naturalidade'], metrics['media_pontuacao']]
        })
        fig_avg = px.bar(
            avg_df, 
            x='Habilidade', 
            y='Média', 
            range_y=[0, 10], 
            color='Habilidade',
            text_auto=True,
            title="Sua Força e Pontos Fracos"
        )
        st.plotly_chart(fig_avg, use_container_width=True)

        # Gráfico 2: Evolução das Notas (Gráfico de Linha ou Dispersão)
        st.subheader("Evolução do Desempenho (Últimas Frases)")
        
        # Para um gráfico de evolução, o índice é a ordem de criação
        df_scores['Frase #'] = range(1, len(df_scores) + 1)
        
        # Cria um DataFrame 'long' para o Plotly
        df_long = df_scores.melt(
            id_vars=['Frase #'], 
            value_vars=['grammar_score', 'vocabulary_score', 'naturalness_score', 'punctuation_score'], 
            var_name='Categoria', 
            value_name='Nota'
        )

        fig_evol = px.line(
            df_long, 
            x='Frase #', 
            y='Nota', 
            color='Categoria', 
            markers=True,
            title="Evolução das Notas das Frases ao Longo do Tempo"
        )
        st.plotly_chart(fig_evol, use_container_width=True)

    else:
        st.info("Crie suas primeiras frases para ver seus gráficos de desempenho!")

    # Carrega a Sidebar
    sm.sidebar_load(st)
    
if __name__ == "__main__":
    # db = Database() # A instância já deve existir se a função app for chamada
    app()