import streamlit as st
import pandas as pd

st.set_page_config(page_title="Torneio das Pedreiras - 2ª Temporada 2026", page_icon="🏆", layout="wide")

def render_html(html_str):
    # Remove quebras de linha e colapsa múltiplos espaços para evitar que o parser de markdown quebre
    cleaned = " ".join(html_str.split())
    st.markdown(cleaned, unsafe_allow_html=True)

# URLs das abas da planilha
URL_CLASSIFICACAO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjDTToac4PiSRhO2U-7IUKmklwHa_nYpIe2f7F00hNd_cdZm7HnaSu2boggd5BkWnOlpiOqaRiysjI/pub?gid=1791764253&single=true&output=csv"
URL_JOGOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjDTToac4PiSRhO2U-7IUKmklwHa_nYpIe2f7F00hNd_cdZm7HnaSu2boggd5BkWnOlpiOqaRiysjI/pub?gid=298235476&single=true&output=csv"
URL_EVENTOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjDTToac4PiSRhO2U-7IUKmklwHa_nYpIe2f7F00hNd_cdZm7HnaSu2boggd5BkWnOlpiOqaRiysjI/pub?gid=1934038280&single=true&output=csv"
URL_ARTILHARIA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjDTToac4PiSRhO2U-7IUKmklwHa_nYpIe2f7F00hNd_cdZm7HnaSu2boggd5BkWnOlpiOqaRiysjI/pub?gid=1324913652&single=true&output=csv"
URL_ASSISTENCIAS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjDTToac4PiSRhO2U-7IUKmklwHa_nYpIe2f7F00hNd_cdZm7HnaSu2boggd5BkWnOlpiOqaRiysjI/pub?gid=1514136485&single=true&output=csv"
URL_CARTOES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjDTToac4PiSRhO2U-7IUKmklwHa_nYpIe2f7F00hNd_cdZm7HnaSu2boggd5BkWnOlpiOqaRiysjI/pub?gid=1503475378&single=true&output=csv"

@st.cache_data(ttl=600)
def carregar_dados(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Erro ao carregar dados do link: {url}. Detalhes: {e}")
        return pd.DataFrame()

# Carregamento em cache
df_classif = carregar_dados(URL_CLASSIFICACAO)
df_jogos = carregar_dados(URL_JOGOS)
df_eventos = carregar_dados(URL_EVENTOS)
df_artilharia = carregar_dados(URL_ARTILHARIA)
df_assistencias = carregar_dados(URL_ASSISTENCIAS)
df_cartoes = carregar_dados(URL_CARTOES)

# Dicionário de Escudos SVG dos Times
ESCUDOS = {
    "Napoli": """
    <svg width="28" height="28" viewBox="0 0 100 100" style="vertical-align: middle; margin-right: 8px;">
        <path d="M10 20 L50 5 L90 20 L90 60 C90 85 50 98 50 98 C50 98 10 85 10 60 Z" fill="#0c4b85" stroke="#fff" stroke-width="4"/>
        <path d="M10 20 L50 5 L90 20 L90 35 L10 35 Z" fill="#082d52"/>
        <text x="50" y="27" fill="#fff" font-size="13" font-weight="bold" font-family="'Outfit', sans-serif" text-anchor="middle">NAPOLI</text>
        <text x="50" y="72" fill="#fff" font-size="38" font-weight="bold" font-family="'Outfit', sans-serif" text-anchor="middle">N</text>
    </svg>
    """,
    "Sol Nascente": """
    <svg width="28" height="28" viewBox="0 0 100 100" style="vertical-align: middle; margin-right: 8px;">
        <path d="M10 20 L50 5 L90 20 L90 60 C90 85 50 98 50 98 C50 98 10 85 10 60 Z" fill="#d97706" stroke="#fbbf24" stroke-width="4"/>
        <circle cx="50" cy="50" r="16" fill="#fbbf24" stroke="#b45309" stroke-width="2"/>
        <path d="M50 20 L50 80 M20 50 L80 50 M29 29 L71 71 M29 71 L71 29" stroke="#fbbf24" stroke-width="2"/>
        <text x="50" y="85" fill="#fff" font-size="9" font-weight="bold" font-family="'Outfit', sans-serif" text-anchor="middle">SOL NASCENTE</text>
    </svg>
    """,
    "Falcões FC": """
    <svg width="28" height="28" viewBox="0 0 100 100" style="vertical-align: middle; margin-right: 8px;">
        <path d="M10 20 L50 5 L90 20 L90 60 C90 85 50 98 50 98 C50 98 10 85 10 60 Z" fill="#0f172a" stroke="#1d4ed8" stroke-width="4"/>
        <path d="M30 42 L50 26 L70 42 L55 58 L50 50 L45 58 Z" fill="#1d4ed8"/>
        <path d="M25 47 L50 32 L75 47 L50 67 Z" fill="none" stroke="#fff" stroke-width="2"/>
        <text x="50" y="84" fill="#fff" font-size="10" font-weight="bold" font-family="'Outfit', sans-serif" text-anchor="middle">FALCÕES</text>
    </svg>
    """,
    "Demolidor": """
    <svg width="28" height="28" viewBox="0 0 100 100" style="vertical-align: middle; margin-right: 8px;">
        <path d="M10 20 L50 5 L90 20 L90 60 C90 85 50 98 50 98 C50 98 10 85 10 60 Z" fill="#991b1b" stroke="#000" stroke-width="4"/>
        <text x="50" y="66" fill="#fff" font-size="44" font-weight="bold" font-family="Georgia, serif" text-anchor="middle">D</text>
        <text x="50" y="86" fill="#ccc" font-size="9" font-weight="bold" font-family="'Outfit', sans-serif" text-anchor="middle">DEMOLIDOR</text>
    </svg>
    """
}

# Estilos CSS premium
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Outfit', sans-serif;
    background-color: #0e1117;
}

/* Títulos */
.torneio-header {
    text-align: center;
    padding: 10px 0;
    margin-bottom: 20px;
}
.torneio-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #FFD700;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.torneio-subtitle {
    font-size: 1.2rem;
    color: #a0aec0;
    margin-top: 5px;
}

/* Estilo do painel de Jogos (Fim de Jogo) */
.fim-de-jogo-container {
    background-color: #161a22;
    border: 2px solid rgba(255, 215, 0, 0.2);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 25px;
}
.fim-de-jogo-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #4ade80;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 15px;
}
.partida-card {
    background-color: #1e2430;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
    border-left: 4px solid #FFD700;
}
.partida-meta {
    text-align: center;
    font-size: 0.85rem;
    color: #a0aec0;
    margin-bottom: 10px;
    font-weight: 600;
}
.partida-placar-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.partida-time-col {
    display: flex;
    align-items: center;
    width: 38%;
}
.partida-time-col.mandante {
    justify-content: flex-end;
    text-align: right;
}
.partida-time-col.visitante {
    justify-content: flex-start;
    text-align: left;
}
.partida-time-nome {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
}
.partida-gols-badge {
    background-color: #84cc16;
    color: #0e1117;
    font-size: 1.6rem;
    font-weight: 800;
    padding: 4px 14px;
    border-radius: 8px;
    min-width: 45px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(132, 204, 22, 0.3);
}
.partida-vs {
    font-size: 1rem;
    font-weight: 800;
    color: #ffffff;
    font-style: italic;
    padding: 0 10px;
}

/* Eventos da Partida */
.eventos-row {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 10px;
    font-size: 0.8rem;
    color: #cbd5e1;
}
.eventos-col {
    width: 48%;
}
.eventos-col.mandante {
    text-align: right;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    padding-right: 10px;
}
.eventos-col.visitante {
    text-align: left;
    padding-left: 10px;
}
.evento-item {
    margin-bottom: 4px;
}
.evento-item span {
    font-weight: 600;
    color: #94a3b8;
}

/* Tabela de Classificação Premium */
.classificacao-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.classificacao-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
    margin-top: 5px;
}
.classificacao-table th {
    background-color: #1e2430;
    color: #a0aec0;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.8rem;
    padding: 10px;
    text-align: center;
    border: none;
}
.classificacao-table th.time-header {
    text-align: left;
    border-radius: 6px 0 0 6px;
}
.classificacao-table th.last-header {
    border-radius: 0 6px 6px 0;
}
.classificacao-row {
    background-color: #161a22;
    transition: transform 0.2s;
}
.classificacao-row:hover {
    transform: scale(1.01);
    background-color: #1c212c;
}
.classificacao-cell {
    padding: 12px 10px;
    text-align: center;
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.classificacao-cell.time-cell {
    text-align: left;
    font-weight: 700;
    border-left: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px 0 0 8px;
}
.classificacao-cell.last-cell {
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 0 8px 8px 0;
}
.classificacao-cell.destaque {
    color: #FFD700;
    font-size: 1rem;
    font-weight: 800;
}

/* Estatísticas Base */
.stat-box {
    background-color: #161a22;
    border: 2px solid rgba(255, 215, 0, 0.2);
    border-radius: 12px;
    padding: 20px;
    height: 100%;
}
.stat-box-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFD700;
    border-bottom: 2px solid #FFD700;
    padding-bottom: 8px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 0.95rem;
}
.stat-row:last-child {
    border-bottom: none;
}
.stat-jogador {
    font-weight: 700;
    color: #ffffff;
}
.stat-valor {
    font-weight: 800;
    color: #FFD700;
}

/* Seletor do Sidebar */
[data-testid="stSidebar"] {
    background-color: #0e1117;
    border-right: 1px solid rgba(255, 215, 0, 0.2);
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal do Torneio
render_html("""
<div class="torneio-header">
    <div class="torneio-title">Torneio das Pedreiras</div>
    <div class="torneio-subtitle">2ª Temporada 2026</div>
</div>
""")

# Lógica de Rodadas/Filtros
if not df_jogos.empty:
    # Agrupar rodadas por data única de jogo
    datas_ordenadas = pd.to_datetime(df_jogos['Data'], format='%d/%m/%Y').sort_values().unique()
    datas_str = [d.strftime('%d/%m/%Y') for d in datas_ordenadas]
    
    # Criar mapeamento de rodadas
    opcoes_rodada = {}
    for idx, data_str in enumerate(datas_str):
        opcoes_rodada[f"{idx + 1}ª Rodada ({data_str[:-5]})"] = data_str
        
    st.sidebar.markdown("<h3 style='color: #FFD700;'>⚙️ Filtros</h3>", unsafe_allow_html=True)
    # Seleção de rodada (padrão é a última rodada jogada)
    rodada_selecionada = st.sidebar.selectbox("Selecione a Rodada:", list(opcoes_rodada.keys()), index=len(opcoes_rodada)-1)
    data_filtro = opcoes_rodada[rodada_selecionada]
else:
    data_filtro = None
    rodada_selecionada = ""

# Layout Principal: Duas Colunas
col_esquerda, col_direita = st.columns([1.1, 1.2])

# COLUNA ESQUERDA: Jogos ("Fim de Jogo")
with col_esquerda:
    st.markdown(f"<div class='classificacao-title'>Jogos - {rodada_selecionada}</div>", unsafe_allow_html=True)
    
    if data_filtro and not df_jogos.empty:
        # Filtrar jogos da data selecionada
        jogos_rodada = df_jogos[df_jogos['Data'] == data_filtro]
        
        for _, jogo in jogos_rodada.iterrows():
            id_partida = jogo['ID_Partida']
            mandante = jogo['Mandante']
            visitante = jogo['Visitante']
            gols_m = int(jogo['Gols_Mandante'])
            gols_v = int(jogo['Gols_Visitante'])
            hora = jogo['Hora']
            
            # Gerar HTML do Card da Partida
            escudo_m = ESCUDOS.get(mandante, "")
            escudo_v = ESCUDOS.get(visitante, "")
            
            # Buscar eventos dessa partida
            eventos_partida = df_eventos[df_eventos['ID_Partida'] == id_partida] if not df_eventos.empty else pd.DataFrame()
            
            # Separar eventos de mandante e visitante
            gols_m_lista, assists_m_lista, cartoes_m_lista = [], [], []
            gols_v_lista, assists_v_lista, cartoes_v_lista = [], [], []
            
            for _, ev in eventos_partida.iterrows():
                time_ev = ev['Time']
                jogador = ev['Jogador']
                tipo = ev['Tipo_Evento']
                qtd = int(ev['Quantidade'])
                obs = f" {ev['Observacao']}" if pd.notna(ev['Observacao']) and str(ev['Observacao']).strip() != "" else ""
                
                txt = f"{jogador} - {qtd}{obs}" if qtd > 1 else f"{jogador}{obs}"
                
                # Se for Gol Contra, a contagem de gols vai para o adversário, mas no card exibe no lado de quem fez
                if tipo == "Gol Contra":
                    txt = f"Gol contra - {qtd}"
                
                if time_ev == mandante:
                    if tipo in ["Gol", "Gol Contra"]:
                        gols_m_lista.append(txt)
                    elif tipo == "Assistência":
                        assists_m_lista.append(txt)
                    elif tipo == "Cartão Amarelo":
                        cartoes_m_lista.append(txt)
                elif time_ev == visitante:
                    if tipo in ["Gol", "Gol Contra"]:
                        gols_v_lista.append(txt)
                    elif tipo == "Assistência":
                        assists_v_lista.append(txt)
                    elif tipo == "Cartão Amarelo":
                        cartoes_v_lista.append(txt)
            
            # Montar HTML do Card
            card_html = f"""
            <div class="partida-card">
                <div class="partida-meta">🕒 {jogo['Data']} às {hora}H</div>
                <div class="partida-placar-row">
                    <div class="partida-time-col mandante">
                        <span class="partida-time-nome">{mandante}</span>
                        {escudo_m}
                    </div>
                    <div class="partida-gols-badge">{gols_m}</div>
                    <div class="partida-vs">VS</div>
                    <div class="partida-gols-badge">{gols_v}</div>
                    <div class="partida-time-col visitante">
                        {escudo_v}
                        <span class="partida-time-nome">{visitante}</span>
                    </div>
                </div>
                <div class="eventos-row">
                    <div class="eventos-col mandante">
            """
            
            # Eventos do Mandante
            if gols_m_lista:
                card_html += f'<div class="evento-item">⚽ <span>Gols:</span> {", ".join(gols_m_lista)}</div>'
            if assists_m_lista:
                card_html += f'<div class="evento-item">👟 <span>Assists:</span> {", ".join(assists_m_lista)}</div>'
            if cartoes_m_lista:
                card_html += f'<div class="evento-item">🟨 <span>C. Amarelo:</span> {", ".join(cartoes_m_lista)}</div>'
            
            card_html += """
                    </div>
                    <div class="eventos-col visitante">
            """
            
            # Eventos do Visitante
            if gols_v_lista:
                card_html += f'<div class="evento-item">⚽ <span>Gols:</span> {", ".join(gols_v_lista)}</div>'
            if assists_v_lista:
                card_html += f'<div class="evento-item">👟 <span>Assists:</span> {", ".join(assists_v_lista)}</div>'
            if cartoes_v_lista:
                card_html += f'<div class="evento-item">🟨 <span>C. Amarelo:</span> {", ".join(cartoes_v_lista)}</div>'
                
            card_html += """
                    </div>
                </div>
            </div>
            """
            render_html(card_html)
    else:
        st.info("Nenhum jogo cadastrado para esta rodada.")

# COLUNA DIREITA: Tabela de Classificação
with col_direita:
    st.markdown("<div class='classificacao-title'>Classificação Geral</div>", unsafe_allow_html=True)
    
    if not df_classif.empty:
        # Ordenar classificação conforme os critérios (Pontos desc, Vitórias desc, Saldo desc)
        # Na planilha já vem ordenado, mas vamos forçar a garantia
        df_classif_sorted = df_classif.sort_values(by=["PT", "V", "SG"], ascending=False)
        
        # Gerar a tabela HTML estilizada
        table_html = """
        <table class="classificacao-table">
            <thead>
                <tr>
                    <th class="time-header">Equipe</th>
                    <th>PT</th>
                    <th>J</th>
                    <th>V</th>
                    <th>E</th>
                    <th>D</th>
                    <th>GM</th>
                    <th>GS</th>
                    <th class="last-header">SG</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for _, row in df_classif_sorted.iterrows():
            time_nome = row['Equipe']
            escudo = ESCUDOS.get(time_nome, "")
            
            table_html += f"""
            <tr class="classificacao-row">
                <td class="classificacao-cell time-cell">{escudo} {time_nome}</td>
                <td class="classificacao-cell destaque">{row['PT']}</td>
                <td class="classificacao-cell">{row['J']}</td>
                <td class="classificacao-cell">{row['V']}</td>
                <td class="classificacao-cell">{row['E']}</td>
                <td class="classificacao-cell">{row['D']}</td>
                <td class="classificacao-cell">{row['GM']}</td>
                <td class="classificacao-cell">{row['GS']}</td>
                <td class="classificacao-cell last-cell">{row['SG']}</td>
            </tr>
            """
            
        table_html += "</tbody></table>"
        render_html(table_html)
    else:
        st.info("Tabela de classificação indisponível.")

st.markdown("<br><br>", unsafe_allow_html=True)

# PAINEL INFERIOR: Três colunas de Estatísticas Individuais
col_art, col_garc, col_cart = st.columns(3)

# 1. Artilharia
with col_art:
    html_art = '<div class="stat-box"><div class="stat-box-title">⚽ Artilheiros</div>'
    if not df_artilharia.empty:
        df_art_filtered = df_artilharia[df_artilharia['Gols'] > 0].sort_values(by="Gols", ascending=False)
        if not df_art_filtered.empty:
            for _, row in df_art_filtered.iterrows():
                html_art += f"""
                <div class="stat-row">
                    <span class="stat-jogador">{row['Jogador']}</span>
                    <span class="stat-valor">{row['Gols']} gol(s)</span>
                </div>
                """
        else:
            html_art += "<p style='color: #cbd5e1; font-size: 0.9rem;'>Nenhum gol registrado.</p>"
    else:
        html_art += "<p style='color: #cbd5e1; font-size: 0.9rem;'>Dados de artilharia indisponíveis.</p>"
    html_art += "</div>"
    render_html(html_art)

# 2. Garçom (Assistências)
with col_garc:
    html_garc = '<div class="stat-box"><div class="stat-box-title">👟 Garçom (Assistências)</div>'
    if not df_assistencias.empty:
        df_ass_filtered = df_assistencias[df_assistencias['Assistências'] > 0].sort_values(by="Assistências", ascending=False)
        if not df_ass_filtered.empty:
            for _, row in df_ass_filtered.iterrows():
                html_garc += f"""
                <div class="stat-row">
                    <span class="stat-jogador">{row['Jogador']}</span>
                    <span class="stat-valor">{row['Assistências']} assist.</span>
                </div>
                """
        else:
            html_garc += "<p style='color: #cbd5e1; font-size: 0.9rem;'>Nenhuma assistência registrada.</p>"
    else:
        html_garc += "<p style='color: #cbd5e1; font-size: 0.9rem;'>Dados de assistências indisponíveis.</p>"
    html_garc += "</div>"
    render_html(html_garc)

# 3. Cartões Amarelos
with col_cart:
    html_cart = '<div class="stat-box"><div class="stat-box-title">🟨 Cartão Amarelo</div>'
    if not df_cartoes.empty:
        df_cart_filtered = df_cartoes[df_cartoes['Cartões Amarelos'] > 0].sort_values(by="Cartões Amarelos", ascending=False)
        if not df_cart_filtered.empty:
            for _, row in df_cart_filtered.iterrows():
                html_cart += f"""
                <div class="stat-row">
                    <span class="stat-jogador">{row['Jogador']}</span>
                    <span class="stat-valor">{row['Cartões Amarelos']} cartões</span>
                </div>
                """
        else:
            html_cart += "<p style='color: #cbd5e1; font-size: 0.9rem;'>Nenhum cartão registrado.</p>"
    else:
        html_cart += "<p style='color: #cbd5e1; font-size: 0.9rem;'>Dados de cartões indisponíveis.</p>"
    html_cart += "</div>"
    render_html(html_cart)

# Rodapé simples
render_html("""
<div style="text-align: center; margin-top: 60px; color: #4a5568; font-size: 13px; padding-bottom: 20px;">
    Pedreiras FC &copy; 2026 • Todos os direitos reservados.
</div>
""")
