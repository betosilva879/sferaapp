from dash import Input, Output
import pandas as pd
import plotly.graph_objects as go
import base64
from dash.exceptions import PreventUpdate
from PIL import Image, ImageDraw, ImageFont, ImageOps
import tempfile
import os


def register_jogador_callbacks(app):
    # Atualiza o dropdown de jogadores
    @app.callback(
    Output('dropdown-jogador', 'options'),
    Output('dropdown-jogador', 'value'),  # novo output
    Input('dropdown-posicao', 'value')
    )
    def update_jogadores_dropdown(posicao_selecionada):
        atletas_df = pd.read_excel('data/atletas.xlsx')
        jogadores = atletas_df[atletas_df['Posição'] == posicao_selecionada]['Jogador'].sort_values()
        options = [{'label': jogador, 'value': jogador} for jogador in jogadores]
        value = jogadores.iloc[0] if not jogadores.empty else None
        return options, value
    

    # Atualiza o radar chart
    @app.callback(
        Output('radar-jogador', 'figure'),
        [Input('dropdown-posicao', 'value'),
         Input('dropdown-jogador', 'value')]
    )
    def update_radar_chart(posicao, jogador):
        if not posicao or not jogador:
            return go.Figure()

        try:
            df = pd.read_excel('data/fatores.xlsx')
        except Exception:
            return go.Figure()

        categorias = ["marcação", "competitividade", "distribuição", "criação", "superação", "finalização"]

        # Converter as colunas para numérico
        for col in categorias:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        jogador_df = df[(df["posição"] == posicao) & (df["jogador"] == jogador)]

        if jogador_df.empty or jogador_df[categorias].isnull().any(axis=1).all():
            return go.Figure()

        valores = jogador_df[categorias].iloc[0].tolist()
        valores += [valores[0]]  # Fechar o radar
        categorias += [categorias[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias,
            fill='toself',
            name=jogador,
            line=dict(color="#3CBBB1", width=1)
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False,
                    gridcolor="rgba(255,255,255,0.1)"
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=False,
            title=dict(
                text=f"{jogador}",
                font=dict(size=14, color="#C0C0C0", family="Arial Black"),
                x=0.5
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=30, l=30, r=30),
            font=dict(color='white',size=11)
        )

        return fig
    
    @app.callback(
        Output('grafico-indicadores-habilidade', 'figure'),
        [
            Input('dropdown-categoria', 'value'),
            Input('dropdown-ano', 'value'),
            Input('dropdown-posicao', 'value'),
            Input('dropdown-jogador', 'value'),
            Input('dropdown-habilidade-principal', 'value')
        ]
    )
    def update_grafico_indicadores(categoria, ano, posicao, jogador, habilidade):
        import numpy as np
        if not all([categoria, ano, posicao, jogador, habilidade]):
            return go.Figure()

        habilidade_dict = {
            'finalização': ['Gols', 'ChutesAoGol', 'ChutesNoGol', 'xG', 'DisputasOfensivas', 'Impedimentos'],
            'distribuição': ['Passes', 'PassesCorretos', 'PassesLongos', 'PassesTerçoFinal', 'PassesTerçoFinalCorretos', 'PassesLongosCorretos'],
            'criação': ['Assistências', 'AssistênciasChute', 'xA', 'PassesCriativos', 'PassesCriativosCorretos',  'PassesGrandeÁreaCorretos'],
            'superação': ['Cruzamentos', 'CruzamentosCorretos', 'Dribles', 'DriblesCorretos', 'FaltasSofridas', 'Progressão'],
            'marcação': ['AçõesTotais', 'Interceptações', 'RecuperaçãoPosse', 'DisputasDefensivas', 'Carrinhos', 'CarrinhosVencidos'],
            'competitividade': ['AçõesBemSucedidas', 'DisputasVencidas', 'DisputasAéreasVencidas', 'DisputasDefensivasVencidas', 'DisputasOfensivasVencidas', 'Faltas']
        }

        variaveis = habilidade_dict.get(habilidade, [])
        if not variaveis:
            return go.Figure()

        df = pd.read_excel("data/u17br.xlsx")
        df = df[df["Posição"] == posicao]

        fig = go.Figure()

        for i, var in enumerate(variaveis):
            df[var] = pd.to_numeric(df[var], errors="coerce")

            #Normalização local por variável
            min_val = df[var].min()
            max_val = df[var].max()
            range_val = max_val - min_val if max_val != min_val else 1
            df_normalizado = (df[var] - min_val) / range_val

            # Linha horizontal de fundo para cada segmento
            fig.add_trace(go.Scatter(
                x=[0, 1],
                y=[i, i],
                mode='lines',
                line=dict(color='rgba(255,255,255,0.1)', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))


            #Plotar todos os jogadores da posição com valores normalizados
            fig.add_trace(go.Scatter(
                x=df_normalizado,
                y=[i] * len(df),
                mode='markers',
                marker=dict(size=8, color='rgba(192,192,192,0.25)'),
                name="Outros",
                showlegend=(i == 0),
                hoverinfo='skip'
            ))

            #Jogador selecionado (usa valor real para texto, mas normalizado para posição)
            jogador_val = df[df["Jogador"] == jogador][var]
            if not jogador_val.empty and not pd.isna(jogador_val.values[0]):
                val_real = jogador_val.values[0]
                val_norm = (val_real - min_val) / range_val
                fig.add_trace(go.Scatter(
                    x=[val_norm],
                    y=[i],
                    mode='markers',
                    marker=dict(size=11, color='#3CBBB1'),
                    name=jogador,
                    showlegend=(i == 0),
                    text=[jogador],
                    hovertemplate="%{text}<extra></extra>"
                ))

            #Média da variável (mesma ideia: posição normalizada, valor real no hover)
            media = df[var].mean()
            if not pd.isna(media):
                media_norm = (media - min_val) / range_val
                fig.add_trace(go.Scatter(
                    x=[media_norm],
                    y=[i],
                    mode='markers',
                    marker=dict(size=10, color='#D3AF37', symbol='circle-open'),
                    name='Média',
                    showlegend=(i == 0),
                    hovertemplate=f"Média {var}: {media:.2f}<extra></extra>"
                ))

        for var in variaveis:
            for i, var in enumerate(variaveis):
                fig.add_annotation(
                    xref="paper", yref="y",
                    x=0.0, y=i,
                    text=var,
                    showarrow=False,
                    font=dict(size=9, color="#c0c0c0", family="Arial"),
                    align="left",
                    xanchor="left",
                    yshift=15
                )

        fig.update_layout(
            title=dict(
                text=f"Indicadores – {habilidade.capitalize()}",
                x=0.5,
                font=dict(size=14, color="#C0C0C0", family="Arial Black")
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, color="white"),
            yaxis=dict(
                tickmode="array",
                tickvals=list(range(len(variaveis))),
                ticktext=[""] * len(variaveis),
                showgrid=False,
                showticklabels=False,
                zeroline=False
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=290,
            #margin=dict(l=30, r=30, t=50, b=30),
            font=dict(size=11, color="white"),
            legend=dict(
                orientation="h",
                yanchor="top",
                y= 0,  # ou -0.3 se precisar afastar mais
                xanchor="center",
                x=0.5,
                font=dict(size=8, color="#c0c0c0")
            ),
            margin=dict(l=50, r=30, t=50, b=50),
            showlegend=True
        )

        return fig
    
    @app.callback(
        Output('scatterplot-indicadores', 'figure'),
        [
            Input('dropdown-posicao', 'value'),
            Input('dropdown-jogador', 'value'),
            Input('dropdown-scatter-x', 'value'),
            Input('dropdown-scatter-y', 'value')
        ]
    )
    def update_scatterplot(posicao, jogador, var_x, var_y):
        # Evita erro caso algum campo esteja vazio
        if not all([posicao, jogador, var_x, var_y]):
            return go.Figure()

        # Carrega e filtra a base de dados
        df = pd.read_excel("data/u17br.xlsx")
        df = df[df["Posição"] == posicao].copy()
        df[var_x] = pd.to_numeric(df[var_x], errors="coerce")
        df[var_y] = pd.to_numeric(df[var_y], errors="coerce")

        fig = go.Figure()

        # Pontos de todos os jogadores da posição
        fig.add_trace(go.Scatter(
            x=df[var_x],
            y=df[var_y],
            mode='markers',
            marker=dict(size=10, color='rgba(192,192,192,0.4)'),
            hoverinfo='skip',
            showlegend=False
        ))

        # Jogador escolhido
        jogador_row = df[df["Jogador"] == jogador]
        if not jogador_row.empty:
            fig.add_trace(go.Scatter(
                x=jogador_row[var_x],
                y=jogador_row[var_y],
                mode='markers',
                marker=dict(size=11, color='#3CBBB1'),
                text=[jogador],
                hovertemplate="%{text}<extra></extra>",
                name=jogador
            ))

        # Centróide (média dos jogadores da posição)
        mean_x = df[var_x].mean()
        mean_y = df[var_y].mean()
        fig.add_trace(go.Scatter(
            x=[mean_x],
            y=[mean_y],
            mode='markers',
            marker=dict(size=10, color='#D3AF37', symbol='circle-open'),
            name='Média',
            hovertemplate=f"Média<br>{var_x}: {mean_x:.2f}<br>{var_y}: {mean_y:.2f}<extra></extra>"
        ))

        # Estilo do gráfico
        fig.update_layout(
            title=dict(
                text=f"{var_y} vs {var_x}",
                x=0.5,
                font=dict(size=14, color="#C0C0C0", family="Arial Black")
            ),
            xaxis=dict(title=var_x, color="white", showgrid=False),
            yaxis=dict(title=var_y, color="white", showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=270,
            margin=dict(l=30, r=30, t=50, b=50),
            font=dict(size=8, color="white"),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="right",
                x=1,
                font=dict(size=8, color="#c0c0c0"),
                bgcolor='rgba(255,255,255,0.05)',  
                bordercolor='white',               
                borderwidth=1                      
            ),
            showlegend=True
        )

        return fig
    
    @app.callback(
    Output('imagem-card', 'src'),
    Input('dropdown-jogador', 'value')
    )
    def atualizar_card(jogador_nome):
        if not jogador_nome:
            raise PreventUpdate

        df = pd.read_excel("data/card.xlsx")
        if jogador_nome not in df['Jogador'].values:
            raise PreventUpdate

        jogador = df[df['Jogador'] == jogador_nome].iloc[0]
        atributos = {k: int(jogador[k]) for k in ['MAR','COM','SUP','CRI','DIS','FIN']}
        overall = int(jogador['KPI'])

        posicoes = {
            "LD": "LATERAL DIREITO", "LE": "LATERAL ESQUERDO", "ZD": "ZAGUEIRO DIREITO",
            "ZE": "ZAGUEIRO ESQUERDO", "VO": "VOLANTE", "MA": "MEIA ARMADOR",
            "AD": "ATACANTE DIREITO", "AE": "ATACANTE ESQUERDO", "CA": "CENTROAVANTE"
        }
        posicao_extenso = posicoes.get(jogador["Posição"], jogador["Posição"])

        template = Image.open("static/assets/template2.png").convert("RGBA")
        card = template.copy()
        draw = ImageDraw.Draw(card)

        font_path = "fonts/DejaVuSans.ttf"
        font_giga = ImageFont.truetype(font_path, 120)
        font_big = ImageFont.truetype(font_path, 90)
        font_small = ImageFont.truetype(font_path, 30)
        font_xsmall = ImageFont.truetype(font_path, 24)

        player = Image.open("static/assets/icone.png").convert("RGBA").resize((500, 500))
        circle_center = (template.width // 2, 500)
        circle_radius = 215
        zoom_factor = 1.4
        player = player.resize((int(player.width * zoom_factor), int(player.height * zoom_factor)))
        player = ImageOps.fit(player, (circle_radius * 2, circle_radius * 2), centering=(0.5, 0.4))
        mask = Image.new("L", (circle_radius * 2, circle_radius * 2), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, circle_radius * 2, circle_radius * 2), fill=255)
        player_cropped = Image.new("RGBA", (circle_radius * 2, circle_radius * 2))
        player_cropped.paste(player, (0, 0), mask=mask)
        paste_position = (circle_center[0] - circle_radius, circle_center[1] - circle_radius)
        card.paste(player_cropped, paste_position, mask=player_cropped)

        escudo = Image.open("static/assets/logo_sfera.png").convert("RGBA").resize((170, 170))
        flag = Image.open("static/assets/brasil.png").convert("RGBA").resize((210, 210))
        beta = Image.open("static/assets/beta.png").convert("RGBA").resize((210, 42))

        card.paste(escudo, (180, 125), mask=escudo)
        card.paste(flag, (680, 115), mask=flag)
        card.paste(beta, (780, 1430), mask=beta)

        # Centralizar o nome horizontalmente
        bbox = draw.textbbox((0, 0), jogador_nome, font=font_big)
        text_width = bbox[2] - bbox[0]
        x_centro = (card.width - text_width) // 2
        draw.text((x_centro, 735), jogador_nome, font=font_big, fill="black")


        bbox = draw.textbbox((0, 0), str(overall), font=font_giga)
        text_width = bbox[2] - bbox[0]
        x_centro = (card.width - text_width) // 2
        draw.text((x_centro, 75), str(overall), font=font_giga, fill="#D3AF37")

        bbox = draw.textbbox((0, 0), "OVERALL KPI", font=font_small)
        text_width = bbox[2] - bbox[0]
        x_centro = (card.width - text_width) // 2
        draw.text((x_centro, 35), "OVERALL KPI", font=font_small, fill="white")


        bbox = draw.textbbox((0, 0), posicao_extenso, font=font_small)
        text_width = bbox[2] - bbox[0]
        x_centro = (card.width - text_width) // 2
        draw.text((x_centro, 850), posicao_extenso, font=font_small, fill="white")

        valores_pos = {
            "MAR": (398, 952),
            "COM": (398, 1057),
            "SUP": (398, 1168),
            "CRI": (795, 952),
            "DIS": (795, 1057),
            "FIN": (795, 1168),
        }

        for attr, value in atributos.items():
            x, y = valores_pos[attr]
            draw.text((x, y), str(value), font=font_big, fill="white")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            temp_path = tmp.name
            card.save(temp_path)

        with open(temp_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()

        # Remove o arquivo temporário após leitura (opcional)
        os.remove(temp_path)

        return f"data:image/png;base64,{encoded}"

