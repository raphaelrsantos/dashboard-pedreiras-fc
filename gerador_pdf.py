import os
from fpdf import FPDF
import pandas as pd

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('helvetica', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Relatorio Financeiro - Futebol das Pedreiras', align='C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def criar_pdf_relatorio(df_periodo, mes, entradas, saidas, saldo_periodo, saldo_acumulado, fig_receitas=None, fig_despesas=None, fig_evolucao=None, fig_saldo=None, fig_parcelas=None):
    pdf = PDF(orientation="landscape")
    pdf.add_page()
    
    # Subtítulo com o Mês
    pdf.set_font("helvetica", "B", 12)
    titulo_mes = f"Competencia: {mes}" if mes != "Todos" else "Periodo: Todo o Historico"
    pdf.cell(0, 10, titulo_mes, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Resumo Financeiro
    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    
    # Format values
    ent_str = f"R$ {entradas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    sai_str = f"-R$ {abs(saidas):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    s_per_str = f"R$ {saldo_periodo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    s_acu_str = f"R$ {saldo_acumulado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    col_width = pdf.epw / 4
    pdf.cell(col_width, 10, "Total Entradas", border=1, align="C", fill=True)
    pdf.cell(col_width, 10, "Total Saidas", border=1, align="C", fill=True)
    pdf.cell(col_width, 10, "Saldo do Periodo", border=1, align="C", fill=True)
    pdf.cell(col_width, 10, "Saldo Acumulado", border=1, align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 12)
    # Cores
    pdf.set_text_color(0, 128, 0)
    pdf.cell(col_width, 10, ent_str, border=1, align="C")
    
    pdf.set_text_color(255, 0, 0)
    pdf.cell(col_width, 10, sai_str, border=1, align="C")
    
    cor_per = (0, 128, 0) if saldo_periodo >= 0 else (255, 0, 0)
    pdf.set_text_color(*cor_per)
    pdf.cell(col_width, 10, s_per_str, border=1, align="C")
    
    cor_acu = (0, 128, 0) if saldo_acumulado >= 0 else (255, 0, 0)
    pdf.set_text_color(*cor_acu)
    pdf.cell(col_width, 10, s_acu_str, border=1, align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    
    # Gráficos
    if any([fig_receitas, fig_despesas, fig_evolucao]):
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, "Analises Detalhadas", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        # Linha 1 de Gráficos
        y_top = pdf.get_y()
        pdf.set_font("helvetica", "B", 14)
        
        img_paths = []
        
        if fig_receitas:
            pdf.set_xy(10, y_top)
            pdf.cell(130, 8, "Origem das Receitas (Entradas)", align="C")
            
            fig_receitas.update_layout(
                paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black', size=36),
                margin=dict(t=20, b=50, l=450, r=20)
            )
            fig_receitas.update_traces(textfont_size=36)
            fig_receitas.write_image("temp_rec.png", width=1200, height=800, scale=2)
            pdf.image("temp_rec.png", x=10, y=y_top + 10, w=130)
            img_paths.append("temp_rec.png")
            
        if fig_despesas:
            pdf.set_xy(150, y_top)
            pdf.cell(130, 8, "Destino das Despesas (Saidas)", align="C")
            
            fig_despesas.update_layout(
                paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black', size=36),
                margin=dict(t=20, b=50, l=450, r=20),
                yaxis_title=None, xaxis_title=None, xaxis=dict(showticklabels=False)
            )
            fig_despesas.update_traces(textfont_size=36)
            fig_despesas.write_image("temp_des.png", width=1200, height=800, scale=2)
            pdf.image("temp_des.png", x=150, y=y_top + 10, w=130)
            img_paths.append("temp_des.png")
            
        if fig_receitas or fig_despesas:
            pdf.add_page()
            
        # Linha 2 de Gráficos
        y_bottom = pdf.get_y()
        pdf.set_font("helvetica", "B", 14)
        
        if fig_evolucao:
            pdf.set_xy(10, y_bottom)
            pdf.cell(130, 8, "Evolucao Mensal (Entradas vs Saidas)", align="C")
            
            fig_evolucao.update_layout(
                paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black', size=36),
                legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, font=dict(size=36)),
                margin=dict(t=20, b=100, l=100, r=20),
                yaxis_title=None, xaxis_title=None, yaxis=dict(showticklabels=False)
            )
            fig_evolucao.update_traces(textfont_size=36)
            fig_evolucao.write_image("temp_evo.png", width=1200, height=800, scale=2)
            pdf.image("temp_evo.png", x=10, y=y_bottom + 10, w=130)
            img_paths.append("temp_evo.png")
            
        if fig_evolucao:
            pdf.set_y(y_bottom + 95)
            
        if fig_parcelas:
            pdf.add_page()
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "Acompanhamento de Parcelamentos", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)
            
            fig_parcelas.update_layout(
                paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black', size=26),
                margin=dict(t=20, b=50, l=750, r=250),
                yaxis_title=None, xaxis_title=None, legend_title=None, xaxis=dict(showticklabels=False),
                legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, font=dict(size=26))
            )
            fig_parcelas.update_traces(textposition='auto', textfont_size=26, textangle=0, constraintext='none')
            fig_parcelas.write_image("temp_parc.png", width=2000, height=1000, scale=2)
            pdf.image("temp_parc.png", x=10, y=pdf.get_y(), w=260)
            img_paths.append("temp_parc.png")
            
        # Clean up images
        for p in img_paths:
            try:
                os.remove(p)
            except:
                pass
                
        pdf.add_page() # Nova página para a tabela
        
    # Tabela de Movimentações
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Extrato de Movimentacoes", new_x="LMARGIN", new_y="NEXT")
    
    # Tabela Cabeçalho
    pdf.set_font("helvetica", "B", 9)
    col_widths_ratio = [18, 15, 35, 35, 82, 25, 30]
    total_ratio = sum(col_widths_ratio)
    col_widths = [w * (pdf.epw / total_ratio) for w in col_widths_ratio]
    
    headers = ["Data", "Tipo", "Envolvido", "Categoria", "Descricao", "Valor", "Saldo"]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1, align="C", fill=True)
    pdf.ln()
    
    # Tabela Corpo
    pdf.set_font("helvetica", "", 8)
    df_linhas = df_periodo.sort_values(by="Data", ascending=False)
    
    fill = False
    for _, row in df_linhas.iterrows():
        data_str = row['Data'].strftime('%d/%m/%Y') if pd.notnull(row['Data']) else ""
        tipo_str = str(row['Tipo']).replace('í', 'i')
        env_str = str(row['Envolvido'])[:30] if 'Envolvido' in row else ""
        cat_str = str(row['Categoria'])[:30]
        desc_str = str(row['Descrição'])[:60]
        
        valor_val = row['Valor']
        valor_str = f"R$ {valor_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        saldo_val = row['Saldo']
        saldo_str = f"R$ {saldo_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notnull(saldo_val) else ""
        
        # Strip accents and weird chars to avoid fpdf encoding errors if simple font is used
        import unicodedata
        def remover_acentos(texto):
            return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        
        env_str = remover_acentos(env_str)
        cat_str = remover_acentos(cat_str)
        desc_str = remover_acentos(desc_str)
        
        pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
        
        pdf.cell(col_widths[0], 6, data_str, border="LR", align="C", fill=True)
        pdf.cell(col_widths[1], 6, tipo_str, border="LR", align="C", fill=True)
        pdf.cell(col_widths[2], 6, env_str, border="LR", align="L", fill=True)
        pdf.cell(col_widths[3], 6, cat_str, border="LR", align="L", fill=True)
        pdf.cell(col_widths[4], 6, desc_str, border="LR", align="L", fill=True)
        
        # Color value based on type
        if tipo_str == "Entrada":
            pdf.set_text_color(0, 128, 0)
        elif tipo_str == "Saida":
            pdf.set_text_color(255, 0, 0)
        else:
            pdf.set_text_color(0, 0, 0)
            
        pdf.cell(col_widths[5], 6, valor_str, border="LR", align="R", fill=True)
        
        # Restore color
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_widths[6], 6, saldo_str, border="LR", align="R", fill=True)
        pdf.ln()
        
        fill = not fill
        
    # Close table bottom border
    pdf.cell(sum(col_widths), 0, "", border="T")
    
    # Return as bytes
    return bytes(pdf.output())
