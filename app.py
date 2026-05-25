import streamlit as st
import pandas as pd
import plotly.express as px
from gerador_pdf import criar_pdf_relatorio

st.set_page_config(page_title="Dashboard Financeiro - Pedreiras FC", page_icon="⚽", layout="wide")

def clean_currency(x):
    if pd.isna(x):
        return 0.0
    if isinstance(x, str):
        x = x.replace('R$', '').replace('\xa0', '').replace(' ', '').strip()
        x = x.replace('.', '')
        x = x.replace(',', '.')
    try:
        return float(x)
    except:
        return 0.0

# URL Pública do Google Sheets em formato CSV (Cole seu link aqui para não precisar digitar toda vez)
URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSc7AsbQs9d5DOGXGHE8_3o4AFnNjSwIycCLynZ204QG7eUKSDdoLBfnrRm-WHNMWgosvOxs8S7alW1/pub?gid=0&single=true&output=csv"

st.markdown(
    '<h1 style="font-size:1.8rem;font-weight:800;line-height:1.3;margin:0 0 0.5rem 0;padding:0">'
    '⚽ Dashboard Financeiro · Futebol das Pedreiras</h1>',
    unsafe_allow_html=True
)



if URL_GOOGLE_SHEETS:
    try:
        # Lê diretamente do link do Google Sheets
        df = pd.read_csv(URL_GOOGLE_SHEETS)
        
        # O Google Sheets pode exportar colunas vazias extras se houver formatação.
        # Limitamos até a coluna J (as 10 primeiras colunas).
        df = df.iloc[:, :10]
        
        # Converter colunas
        df['Valor'] = df['Valor'].apply(clean_currency)
        df['Saldo'] = df['Saldo'].apply(clean_currency)
        
        # Converter datas
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
        
        # Ignorar lançamentos anteriores a 01/01/2026
        df = df[df['Data'] >= pd.to_datetime('2026-01-01')].copy()
        df = df.sort_values('Data').reset_index(drop=True)
        

        
        # Filtro de Mês
        df['Mes_Ano'] = df['Ref']
        meses_disponiveis = df['Mes_Ano'].dropna().unique().tolist()
        try:
            meses_disponiveis.sort(key=lambda x: pd.to_datetime(x, format='%m/%Y'))
        except:
            pass
            
        mes_atual_str = pd.Timestamp.now().strftime('%m/%Y')
        opcoes_mes = ["Todos"] + meses_disponiveis
        idx_padrao = opcoes_mes.index(mes_atual_str) if mes_atual_str in opcoes_mes else 0
        
        st.markdown("### 📅 Escolha o mês para analisar:")
        st.markdown("""
        <style>
        .stSelectbox div[data-baseweb="select"] {
            font-size: 22px !important;
            border: 2px solid #FFD700 !important;
            border-radius: 8px !important;
            box-shadow: 0 0 8px rgba(255, 215, 0, 0.5) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        mes_selecionado = st.selectbox("Selecione o Mês:", options=opcoes_mes, index=idx_padrao, label_visibility="collapsed")
        
        # Definir saldo inicial (primeira linha antes de qualquer filtro)
        saldo_inicial = df.iloc[0]['Saldo'] - df.iloc[0]['Valor'] if not df.empty else 0
        
        # Filtrar df para as métricas superiores
        df_periodo = df.copy()
        if mes_selecionado != "Todos":
            df_periodo = df_periodo[df_periodo['Mes_Ano'] == mes_selecionado]
        
        # Métricas
        st.header("Visão Geral")
        
        entradas = df_periodo[df_periodo['Tipo'] == 'Entrada']['Valor'].sum()
        saidas = df_periodo[df_periodo['Tipo'] == 'Saída']['Valor'].sum()
        if saidas < 0:
            saidas = saidas * -1
            
        # Saldo do Período
        saldo_periodo = entradas - saidas
            
        # Calcular Saldo Acumulado até o mês selecionado
        if mes_selecionado == "Todos":
            saldo_atual = df['Valor'].sum() + saldo_inicial
        else:
            df_temp = df.copy()
            df_temp['Data_Ord'] = pd.to_datetime(df_temp['Mes_Ano'], format='%m/%Y', errors='coerce')
            data_sel = pd.to_datetime(mes_selecionado, format='%m/%Y')
            saldo_atual = df_temp[df_temp['Data_Ord'] <= data_sel]['Valor'].sum() + saldo_inicial
        
        col1, col2, col3, col4 = st.columns(4)
        
        entradas_str = f"R$ {entradas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        saidas_str = f"-R$ {saidas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        saldo_periodo_str = f"R$ {saldo_periodo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        saldo_str = f"R$ {saldo_atual:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        cor_saldo_periodo = "#00cc96" if saldo_periodo >= 0 else "#ff4b4b"
        cor_texto_saldo_periodo = "#111111" if saldo_periodo >= 0 else "#ffffff"
        
        cor_saldo = "#00cc96" if saldo_atual >= 0 else "#ff4b4b"
        cor_texto_saldo = "#111111" if saldo_atual >= 0 else "#ffffff"
        
        with col1:
            st.markdown(f"""
            <div style="background-color: #00cc96; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 16px; color: #111111; font-weight: 500;">Total Entradas</p>
                <p style="margin: 0; font-size: 28px; color: #111111; font-weight: bold;">{entradas_str}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background-color: #ff4b4b; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 16px; color: #ffffff; font-weight: bold;">Total Saídas</p>
                <p style="margin: 0; font-size: 28px; color: #ffffff; font-weight: bold;">{saidas_str}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background-color: {cor_saldo_periodo}; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 16px; color: {cor_texto_saldo_periodo}; font-weight: bold;">Saldo do Período</p>
                <p style="margin: 0; font-size: 28px; color: {cor_texto_saldo_periodo}; font-weight: bold;">{saldo_periodo_str}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="background-color: {cor_saldo}; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 16px; color: {cor_texto_saldo}; font-weight: bold;">Saldo Acumulado</p>
                <p style="margin: 0; font-size: 28px; color: {cor_texto_saldo}; font-weight: bold;">{saldo_str}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Gráficos
        st.header("Análises Detalhadas")
        
        # Variáveis para armazenar as figuras para o PDF
        fig_receitas = None
        fig_despesas = None
        fig_evolucao = None
        fig_saldo = None
        fig_parcelas = None
        
        # Remover "Ajuste Comissão Organizadora" apenas dos gráficos
        df_graficos = df[df['Categoria'] != 'Ajuste Comissão Organizadora'].copy()
        df_graficos_periodo = df_periodo[df_periodo['Categoria'] != 'Ajuste Comissão Organizadora'].copy()
        
        col_row1_1, col_row1_2 = st.columns(2)
        
        with col_row1_1:
            # Origem das Receitas (Entradas)
            st.subheader("Origem das Receitas (Entradas)")
            df_entradas = df_graficos_periodo[df_graficos_periodo['Tipo'] == 'Entrada']
            if not df_entradas.empty:
                receitas_por_categoria = df_entradas.groupby('Categoria')['Valor'].sum().reset_index()
                receitas_por_categoria['Texto_Valor'] = receitas_por_categoria['Valor'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                receitas_por_categoria = receitas_por_categoria.sort_values(by='Valor', ascending=True)
                # Limitar barras a 30% da largura visual
                max_rec = receitas_por_categoria['Valor'].max()
                fig_receitas = px.bar(receitas_por_categoria, x='Valor', y='Categoria', orientation='h',
                                      text='Texto_Valor',
                                      color_discrete_sequence=['#005A32'])
                fig_receitas.update_traces(textposition='outside', textfont_size=13, textangle=0)
                fig_receitas.update_layout(
                    yaxis_title=None, xaxis_title=None, dragmode=False,
                    xaxis=dict(showticklabels=False, range=[0, max_rec / 0.70]),
                    margin=dict(l=5, r=5, t=5, b=5)
                )
                st.plotly_chart(fig_receitas, use_container_width=True, config={'staticPlot': True})
            else:
                st.info("Nenhuma entrada registrada.")
                
        with col_row1_2:
            # Destino das Despesas (Saídas)
            st.subheader("Destino das Despesas (Saídas)")
            df_saidas = df_graficos_periodo[df_graficos_periodo['Tipo'] == 'Saída'].copy()
            if not df_saidas.empty:
                # Converter para positivo para o gráfico
                df_saidas['Valor'] = df_saidas['Valor'].abs()
                despesas_por_categoria = df_saidas.groupby('Categoria')['Valor'].sum().reset_index()
                despesas_por_categoria['Texto_Valor'] = despesas_por_categoria['Valor'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                despesas_por_categoria = despesas_por_categoria.sort_values(by='Valor', ascending=True)
                
                # Limitar a maior barra a no máximo 3x a segunda maior
                despesas_por_categoria['Valor_Visual'] = despesas_por_categoria['Valor']
                vals_unicos = sorted(despesas_por_categoria['Valor'].unique())
                if len(vals_unicos) >= 2:
                    maior_d = vals_unicos[-1]
                    segundo_d = vals_unicos[-2]
                    limite_d = 3.0 * segundo_d
                    if maior_d > limite_d and limite_d > 0:
                        despesas_por_categoria.loc[despesas_por_categoria['Valor'] == maior_d, 'Valor_Visual'] = limite_d
                
                max_des = despesas_por_categoria['Valor_Visual'].max()
                fig_despesas = px.bar(despesas_por_categoria, x='Valor_Visual', y='Categoria', orientation='h',
                                      text='Texto_Valor',
                                      color_discrete_sequence=['#8B0000'])
                fig_despesas.update_traces(textposition='outside', textfont_size=13, textangle=0)
                fig_despesas.update_layout(
                    yaxis_title=None, xaxis_title=None, dragmode=False,
                    xaxis=dict(showticklabels=False, range=[0, max_des / 0.30]),
                    margin=dict(l=5, r=5, t=5, b=5)
                )
                st.plotly_chart(fig_despesas, use_container_width=True, config={'staticPlot': True})
            else:
                st.info("Nenhuma saída registrada.")

        col_row2_1, col_row2_2 = st.columns(2)
        
        with col_row2_1:
            # Evolução Mensal (Entradas vs Saídas)
            st.subheader("Evolução Mensal (Entradas vs Saídas)")
            df_abs = df_graficos_periodo.copy()
            df_abs['Valor'] = df_abs['Valor'].abs()
            evolucao = df_abs.groupby(['Mes_Ano', 'Tipo'])['Valor'].sum().reset_index()
            if not evolucao.empty:
                evolucao['Texto_Valor'] = evolucao['Valor'].apply(lambda x: f"R$ {x:,.0f}".replace(',', '.'))
                fig_evolucao = px.bar(evolucao, x='Mes_Ano', y='Valor', color='Tipo', barmode='group',
                                      text='Texto_Valor',
                                      color_discrete_map={'Entrada': 'green', 'Saída': 'red'})
                fig_evolucao.update_traces(texttemplate='<b>%{text}</b>', textposition='outside', textfont_size=12, textangle=0)
                fig_evolucao.update_layout(yaxis_title=None, xaxis_title=None, yaxis=dict(showticklabels=False), dragmode=False,
                                           legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(size=11)))
                st.plotly_chart(fig_evolucao, use_container_width=True, config={'staticPlot': True})
                
        with col_row2_2:
            # Evolução do Saldo
            titulo_saldo_web = "Saldo do Mês" if mes_selecionado != "Todos" else "Evolução do Saldo (Mês a Mês)"
            st.subheader(titulo_saldo_web)
            fluxo = df.groupby('Mes_Ano')['Valor'].sum().reset_index(name='Fluxo')
            fluxo['Data_Ord'] = pd.to_datetime(fluxo['Mes_Ano'], format='%m/%Y', errors='coerce')
            fluxo = fluxo.sort_values('Data_Ord')
            fluxo['Saldo Acumulado'] = fluxo['Fluxo'].cumsum() + saldo_inicial
            
            if mes_selecionado != "Todos":
                fluxo = fluxo[fluxo['Mes_Ano'] == mes_selecionado]
            
            if not fluxo.empty:
                fluxo['Texto_Saldo'] = fluxo['Saldo Acumulado'].apply(lambda x: f"R$ {x:,.0f}".replace(',', '.'))
                fig_saldo = px.bar(fluxo, x='Mes_Ano', y='Saldo Acumulado',
                                    text='Texto_Saldo',
                                    color_discrete_sequence=['#00CC96'])
                fig_saldo.update_traces(texttemplate='<b>%{text}</b>', textposition='outside', textfont_size=12, textangle=0)
                fig_saldo.update_layout(yaxis_title=None, xaxis_title=None, yaxis=dict(showticklabels=False), dragmode=False)
                st.plotly_chart(fig_saldo, use_container_width=True, config={'staticPlot': True})
            else:
                st.info("Nenhum dado registrado.")
                
        st.markdown("---")
        st.subheader("Acompanhamento de Parcelamentos")
        
        # Lógica de extração de parcelas
        import re
        df_parcelas = df.copy()
        df_parcelas['Valor_Num'] = df_parcelas['Valor'].abs()
        
        def extrair_parcela(desc):
            desc = str(desc)
            match = re.search(r'^(.*?)[-\s,]*(?:parcela|extens[ãa]o)?\s*(\d+)/(\d+)$', desc, re.IGNORECASE)
            if match:
                curr = int(match.group(2))
                tot = int(match.group(3))
                
                # Uma parcela atual não pode ser maior que o total de parcelas (evita pegar datas como 03/01)
                if curr > tot:
                    return pd.Series([None, None, None])
                    
                base = match.group(1).strip()
                # Remove data do início se houver (ex: "24/03 - ")
                base = re.sub(r'^\d{1,2}/\d{1,2}\s*-\s*', '', base)
                base = re.sub(r'^\d{1,2}/\d{1,2}\s+', '', base).strip()
                
                return pd.Series([base, curr, tot])
            return pd.Series([None, None, None])
            
        df_parcelas[['Base_Item', 'Parc_Atual', 'Parc_Total']] = df_parcelas['Descrição'].apply(extrair_parcela)
        df_parc_valid = df_parcelas.dropna(subset=['Base_Item'])
        
        if not df_parc_valid.empty:
            def add_emoji_to_name(name):
                name_lower = name.lower()
                if 'grama' in name_lower or 'campo' in name_lower:
                    return f"🏟️ {name}"
                if 'arame' in name_lower or 'material' in name_lower:
                    return f"🛠️ {name}"
                if 'bola' in name_lower:
                    return f"⚽ {name}"
                if 'máquina' in name_lower or 'maquina' in name_lower:
                    return f"🚜 {name}"
                if 'tinta' in name_lower:
                    return f"🎨 {name}"
                return f"📦 {name}"
            
            resumo_parcelas = []
            hoje = pd.Timestamp.today()
            df_parc_valid['Data_Dt'] = pd.to_datetime(df_parc_valid['Data'], format="%d/%m/%Y", errors='coerce')
            
            for base, group in df_parc_valid.groupby('Base_Item'):
                # Garante que a coluna Status não tenha valores nulos e remove espaços
                group_status = group['Status'].fillna('').astype(str).str.strip().str.lower()
                
                # Falta pagar = itens com Status == 'Pendente'
                falta = group[group_status == 'pendente']['Valor_Num'].sum()
                
                # Pago que está explicitamente na planilha
                pago_planilha = group[group_status == 'pago']['Valor_Num'].sum()
                
                # Projetar o total baseado no número de parcelas informadas (ex: parcela 2/6 -> total de 6)
                valor_parcela = group['Valor_Num'].max()
                tot_parcelas = group['Parc_Total'].max()
                total_projetado = valor_parcela * tot_parcelas if pd.notnull(tot_parcelas) else 0
                
                # Pago Real = Total Projetado menos o que falta
                # (Isso garante a inclusão de parcelas pagas no ano passado que não estão no CSV atual)
                pago = max(total_projetado - falta, pago_planilha)
                
                # Truncar nomes muito longos para caber no mobile
                MAX_CHARS = 28
                nome_curto = (base[:MAX_CHARS] + '…') if len(base) > MAX_CHARS else base
                nome_com_emoji = add_emoji_to_name(nome_curto)
                
                if pago > 0:
                    resumo_parcelas.append({
                        'Item': nome_com_emoji,
                        'Status': 'Pago',
                        'Valor': pago,
                        'Texto': f"R$ {pago:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    })
                if falta > 0:
                    resumo_parcelas.append({
                        'Item': nome_com_emoji,
                        'Status': 'Falta Pagar',
                        'Valor': falta,
                        'Texto': f"R$ {falta:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    })
                    
            if resumo_parcelas:
                df_resumo_parc = pd.DataFrame(resumo_parcelas)
                
                df_totais = df_resumo_parc.groupby('Item')['Valor'].sum().reset_index(name='Total_Item')
                df_resumo_parc = df_resumo_parc.merge(df_totais, on='Item')
                df_resumo_parc = df_resumo_parc.sort_values(by=['Total_Item', 'Status'], ascending=[True, False])
                
                # Ajuste visual: Limitar a maior barra para no máximo 2x a segunda maior
                valores_totais_unicos = sorted(df_resumo_parc['Total_Item'].unique())
                df_resumo_parc['Valor_Visual'] = df_resumo_parc['Valor']
                
                if len(valores_totais_unicos) >= 2:
                    maior_valor = valores_totais_unicos[-1]
                    segundo_maior = valores_totais_unicos[-2]
                    limite_visual = 2.0 * segundo_maior
                    
                    if maior_valor > limite_visual and limite_visual > 0:
                        fator = limite_visual / maior_valor
                        df_resumo_parc.loc[df_resumo_parc['Total_Item'] == maior_valor, 'Valor_Visual'] = df_resumo_parc['Valor'] * fator
                
                n_itens = df_resumo_parc['Item'].nunique()
                altura_grafico = max(300, n_itens * 50)
                
                fig_parcelas = px.bar(df_resumo_parc, x='Valor_Visual', y='Item', color='Status', orientation='h',
                                      color_discrete_map={'Pago': '#005A32', 'Falta Pagar': '#8B0000'},
                                      text='Texto', height=altura_grafico)
                fig_parcelas.update_traces(texttemplate='<b>%{text}</b>', textposition='outside', textfont_size=12, textangle=0, constraintext='none', hovertemplate='%{y}<br><b>%{text}</b>')
                fig_parcelas.update_layout(
                    barmode='stack', yaxis_title=None, xaxis_title=None,
                    xaxis=dict(showticklabels=False),
                    dragmode=False,
                    margin=dict(l=10, r=80, t=10, b=10),
                    yaxis=dict(tickfont=dict(size=11)),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(size=11))
                )
                st.plotly_chart(fig_parcelas, use_container_width=True, config={'staticPlot': True})
            else:
                st.info("Nenhuma parcela ativa neste período.")
        else:
            st.info("Nenhuma despesa parcelada encontrada.")
            
        st.markdown("---")
        
        col_header, col_btn = st.columns([3, 1])
        with col_header:
            st.header("Últimas Movimentações")
            
        with col_btn:
            pdf_bytes = criar_pdf_relatorio(
                df_periodo, mes_selecionado, entradas, saidas, saldo_periodo, saldo_atual,
                fig_receitas, fig_despesas, fig_evolucao, fig_saldo, fig_parcelas
            )
            st.download_button(
                label="📄 Baixar PDF do Relatório",
                data=pdf_bytes,
                file_name=f"Relatorio_Pedreiras_{mes_selecionado.replace('/', '_')}.pdf" if mes_selecionado != "Todos" else "Relatorio_Pedreiras_Completo.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        def highlight_tipo(row):
            if row['Tipo'] == 'Entrada':
                color = 'rgba(0, 255, 0, 0.15)'
            elif row['Tipo'] == 'Saída':
                color = 'rgba(255, 0, 0, 0.15)'
            else:
                color = ''
            return [f'background-color: {color}'] * len(row)
            
        df_todas = df_periodo.sort_values(by='Data', ascending=False)
        
        # Formatar colunas e tamanho da fonte
        styler = df_todas.style.apply(highlight_tipo, axis=1).set_properties(**{'font-size': '20px'}).format({
            'Data': lambda t: t.strftime('%d/%m/%Y') if pd.notnull(t) else '',
            'Valor': lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notnull(x) else "",
            'Saldo': lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notnull(x) else ""
        })
        
        st.dataframe(styler, use_container_width=True, height=800)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Aguardando o upload do arquivo CSV para gerar o dashboard.")
