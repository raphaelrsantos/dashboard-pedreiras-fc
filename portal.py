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
    padding: 15px 0;
    margin-bottom: 15px;
}

.portal-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #FFD700;
    margin: 0;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.portal-subtitle {
    font-size: 1rem;
    color: #a0aec0;
    margin-top: 5px;
}

.card-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 10px;
}

.card {
    background: linear-gradient(135deg, #1e1e1e 0%, #121212 100%);
    border: 2px solid rgba(255, 215, 0, 0.4);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    text-decoration: none;
    color: white !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 220px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.card:hover {
    transform: translateY(-4px);
    border-color: #FFD700;
    box-shadow: 0 10px 25px rgba(255, 215, 0, 0.25);
}

.card-icon {
    font-size: 30px;
    margin-bottom: 10px;
}

.card h3 {
    margin: 0 0 8px 0;
    color: #FFD700;
    font-size: 18px;
    font-weight: 600;
}

.card p {
    margin: 0;
    color: #a0aec0;
    font-size: 13px;
    line-height: 1.4;
    flex-grow: 1;
}

.card.finalizado {
    border-color: rgba(128, 128, 128, 0.25);
    opacity: 0.45;
    cursor: not-allowed;
}

.card.finalizado:hover {
    transform: none;
    border-color: rgba(128, 128, 128, 0.25);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.card.finalizado h3 {
    color: #888888;
}

/* Responsividade Mobile First */
@media (max-width: 768px) {
    .card-container {
        grid-template-columns: 1fr;
    }
    .card {
        height: auto;
        min-height: 160px;
        padding: 15px;
    }
    .portal-title {
        font-size: 1.8rem;
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
st.markdown("""<div class="card-container"><a href="/financeiro/" target="_self" class="card"><div><div class="card-icon">💰</div><h3>Painel Financeiro</h3><p>Acompanhe receitas, despesas, saldo e parcelamentos ativos do time.</p></div></a><a href="/torneio/" target="_self" class="card"><div><div class="card-icon">🏆</div><h3>Torneio 2026/2 (Vigente)</h3><p>Tabela de jogos, classificação geral, artilharia e estatísticas do campeonato vigente.</p></div></a><div class="card finalizado"><div><div class="card-icon">📜</div><h3>Torneio 2026/1 (Finalizado)</h3><p>Histórico completo, resultados e classificação do torneio anterior finalizado.</p></div></div></div>""", unsafe_allow_html=True)

# Rodapé simples
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #4a5568; font-size: 13px;">
    Pedreiras FC &copy; 2026 • Todos os direitos reservados.
</div>
""", unsafe_allow_html=True)
