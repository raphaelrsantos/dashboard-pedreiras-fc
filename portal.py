import streamlit as st

st.set_page_config(page_title="Portal Pedreiras FC", page_icon="⚽", layout="centered")

# Estilo personalizado para os Cards e visual premium
st.markdown("""
<style>
/* Importação de fonte moderna */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Outfit', sans-serif;
    background-color: #0e1117;
}

.portal-header {
    text-align: center;
    padding: 20px 0;
    margin-bottom: 20px;
}

.portal-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #FFD700;
    margin: 0;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.portal-subtitle {
    font-size: 1.1rem;
    color: #a0aec0;
    margin-top: 10px;
}

.card-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 10px;
}

.card {
    background: linear-gradient(135deg, #1e1e1e 0%, #121212 100%);
    border: 2px solid rgba(255, 215, 0, 0.4);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    text-decoration: none;
    color: white !important;
    display: block;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.card:hover {
    transform: translateY(-4px);
    border-color: #FFD700;
    box-shadow: 0 12px 30px rgba(255, 215, 0, 0.25);
}

.card-icon {
    font-size: 40px;
    margin-bottom: 15px;
}

.card h3 {
    margin: 0 0 10px 0;
    color: #FFD700;
    font-size: 24px;
    font-weight: 600;
}

.card p {
    margin: 0;
    color: #a0aec0;
    font-size: 15px;
    line-height: 1.5;
}

/* Responsividade Mobile First */
@media (max-width: 600px) {
    .portal-title {
        font-size: 1.8rem;
    }
    .card {
        padding: 20px;
    }
    .card h3 {
        font-size: 20px;
    }
    .card p {
        font-size: 13px;
    }
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho do Portal
st.markdown("""
<div class="portal-header">
    <div class="portal-title">⚽ Pedreiras FC</div>
    <div class="portal-subtitle">Selecione o painel que deseja acessar:</div>
</div>
""", unsafe_allow_html=True)

# Grid de Cards Clicáveis
st.markdown("""
<div class="card-container">
    <a href="https://pedreiras-financeiro.streamlit.app/" target="_blank" class="card">
        <div class="card-icon">💰</div>
        <h3>Painel Financeiro</h3>
        <p>Acompanhe fluxo de caixa, evolução de saldos, receitas, despesas e controle de parcelamentos ativos do time.</p>
    </a>
    
    <a href="https://pedreiras-torneio.streamlit.app/" target="_blank" class="card">
        <div class="card-icon">🏆</div>
        <h3>Torneio 2026/2 (Vigente)</h3>
        <p>Acompanhe tabela de jogos, classificação geral, artilharia, cartões e estatísticas das equipes participantes.</p>
    </a>
</div>
""", unsafe_allow_html=True)

# Rodapé simples
st.markdown("""
<div style="text-align: center; margin-top: 60px; color: #4a5568; font-size: 13px;">
    Pedreiras FC &copy; 2026 • Todos os direitos reservados.
</div>
""", unsafe_allow_html=True)
