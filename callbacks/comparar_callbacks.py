from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
import base64
from PIL import Image, ImageDraw, ImageFont, ImageOps
import tempfile, os

def register_comparar_callbacks(app):

    @app.callback(
        Output('dropdown-comp-jogador-sfera', 'options'),
        Output('dropdown-comp-jogador-sfera', 'value'),
        Input('dropdown-comp-posicao-sfera', 'value')
    )
    def atualizar_jogadores_sfera(posicao):
        if not posicao:
            raise PreventUpdate
        df = pd.read_excel("data/atletas.xlsx")
        jogadores = df[df["Posição"] == posicao]["Jogador"].sort_values()
        options = [{'label': j, 'value': j} for j in jogadores]
        value = 'Gustavo' if 'Gustavo' in jogadores.values else (jogadores.iloc[0] if not jogadores.empty else None)
        return options, value

    @app.callback(
        Output('dropdown-comp-jogador-comp', 'options'),
        Output('dropdown-comp-jogador-comp', 'value'),
        Input('dropdown-comp-clube', 'value'),
        Input('dropdown-comp-posicao-comp', 'value')
    )
    def atualizar_jogadores_comparado(clube, posicao):
        if not clube or not posicao:
            raise PreventUpdate
        df = pd.read_excel("data/card2.xlsx")
        df.columns = df.columns.str.strip()
        jogadores = df[(df["Clube"] == clube) & (df["Posição"] == posicao)]["Jogador"].sort_values()
        options = [{'label': j, 'value': j} for j in jogadores]
        value = 'Matheus Reis' if 'Matheus Reis' in jogadores.values else (jogadores.iloc[0] if not jogadores.empty else None)
        return options, value

    @app.callback(
        Output('imagem-card-sfera', 'src'),
        Input('dropdown-comp-jogador-sfera', 'value')
    )
    def gerar_card_sfera(jogador_nome):
        return gerar_card_img(jogador_nome)

    @app.callback(
        Output('imagem-card-comp', 'src'),
        Input('dropdown-comp-jogador-comp', 'value')
    )
    def gerar_card_comparado(jogador_nome):
        return gerar_card_img(jogador_nome)

    @app.callback(
        Output('radar-comparativo', 'figure'),
        Input('dropdown-comp-jogador-sfera', 'value'),
        Input('dropdown-comp-posicao-sfera', 'value'),
        Input('dropdown-comp-jogador-comp', 'value'),
        Input('dropdown-comp-posicao-comp', 'value')
    )
    def radar_comparativo(jogador1, pos1, jogador2, pos2):
        if not all([jogador1, jogador2, pos1, pos2]):
            raise PreventUpdate

        df = pd.read_excel("data/fatores.xlsx")
        categorias = ["marcação", "competitividade", "distribuição", "criação", "superação", "finalização"]
        df[categorias] = df[categorias].apply(pd.to_numeric, errors='coerce')

        fig = go.Figure()
        for jogador, posicao, cor in [
            (jogador1, pos1, "#3CBBB1"),
            (jogador2, pos2, "#D3AF37")
        ]:
            linha = df[(df['jogador'] == jogador) & (df['posição'] == posicao)]
            if not linha.empty:
                valores = linha[categorias].iloc[0].tolist()
                valores += [valores[0]]
                fig.add_trace(go.Scatterpolar(
                    r=valores,
                    theta=categorias + [categorias[0]],
                    fill='toself',
                    name=jogador,
                    line=dict(color=cor, width=2),
                    opacity=0.5,
                    hovertemplate=f"{jogador}<extra></extra>"
                ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False,
                    showline=False,
                    tickwidth=1,
                    gridcolor='rgba(255,255,255,0.15)',  # linhas circulares suaves
                    gridwidth=0.5
                ), bgcolor='rgba(0,0,0,0)',
                angularaxis=dict(
                    showline=False,
                    gridcolor='rgba(255,255,255,0.15)',  # linhas radiais suaves
                    gridwidth=0.5,
                    tickfont=dict(color='white', size=10)
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=40, b=20, l=20, r=20),
            showlegend = False, # dict(font=dict(color="white", size=8), orientation="h", x=0.5, y=0,xanchor="right"),
            title=dict(
                text="Comparação de habilidades",
                x=0.5,
                y=0.95,
                xanchor="center",
                font=dict(size=13, color="#c0c0c0")
            ),
        )
        return fig

    @app.callback(
        Output('grafico-indicadores-comparativo', 'figure'),
        Input('dropdown-comp-jogador-sfera', 'value'),
        Input('dropdown-comp-posicao-sfera', 'value'),
        Input('dropdown-comp-jogador-comp', 'value'),
        Input('dropdown-comp-posicao-comp', 'value'),
        Input('dropdown-comp-habilidade', 'value')
    )
    def grafico_indicadores_comparativo(j1, pos1, j2, pos2, habilidade):
        if not all([j1, j2, pos1, pos2, habilidade]):
            raise PreventUpdate

        df = pd.read_excel("data/u17br.xlsx")
        habilidade_dict = {
            'finalização': ['Gols', 'ChutesAoGol', 'ChutesNoGol', 'xG', 'DisputasOfensivas', 'Impedimentos'],
            'distribuição': ['Passes', 'PassesCorretos', 'PassesLongos', 'PassesTerçoFinal', 'PassesTerçoFinalCorretos', 'PassesLongosCorretos'],
            'criação': ['Assistências', 'AssistênciasChute', 'xA', 'PassesCriativos', 'PassesCriativosCorretos',  'PassesGrandeÁreaCorretos'],
            'superação': ['Cruzamentos', 'CruzamentosCorretos', 'Dribles', 'DriblesCorretos', 'FaltasSofridas', 'Progressão'],
            'marcação': ['AçõesTotais', 'Interceptações', 'RecuperaçãoPosse', 'DisputasDefensivas', 'Carrinhos', 'CarrinhosVencidos'],
            'competitividade': ['AçõesBemSucedidas', 'DisputasVencidas', 'DisputasAéreasVencidas', 'DisputasDefensivasVencidas', 'DisputasOfensivasVencidas', 'Faltas']
        }
        vars = habilidade_dict.get(habilidade, [])
        df = df[df["Posição"].isin([pos1, pos2])]

        fig = go.Figure()
        for i, var in enumerate(vars):
            df[var] = pd.to_numeric(df[var], errors='coerce')
            min_v, max_v = df[var].min(), df[var].max()
            range_v = max_v - min_v if max_v != min_v else 1
            df_norm = (df[var] - min_v) / range_v

            fig.add_trace(go.Scatter(x=[0,1], y=[i,i], mode='lines', line=dict(color='rgba(255,255,255,0.1)'), showlegend=False))
            fig.add_trace(go.Scatter(x=df_norm, y=[i]*len(df), mode='markers', marker=dict(size=8, color='rgba(192,192,192,0.25)'), hoverinfo='skip', showlegend=False))

            for jogador, cor in [(j1, "#3CBBB1"), (j2, "#D3AF37")]:
                val = df[df["Jogador"] == jogador][var]
                if not val.empty:
                    norm = (val.values[0] - min_v) / range_v
                    fig.add_trace(go.Scatter(
                        x=[norm], y=[i], mode='markers',
                        marker=dict(size=11, color=cor), name=jogador,
                        hovertemplate=f"{jogador}<extra></extra>", showlegend=(i==0)
                    ))

            fig.add_annotation(xref="paper", yref="y", x=0, y=i, text=var,
                               showarrow=False, font=dict(size=9, color="#c0c0c0"), align="left", xanchor="left", yshift=15)

        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=60, r=30, t=50, b=50),
            font=dict(size=11, color="white"),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=0, font=dict(size=8, color="white")),
            title=dict(
                text="Comparação de indicadores",
                x=0.5,
                xanchor="center",
                font=dict(size=13, color="#c0c0c0")
            )
        )
        return fig

def gerar_card_img(jogador_nome):
    if not jogador_nome:
        raise PreventUpdate
    df = pd.read_excel("data/card2.xlsx")
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

    font_path = "C:/Windows/Fonts/arialbd.ttf"
    font_giga = ImageFont.truetype(font_path, 120)
    font_big = ImageFont.truetype(font_path, 90)
    font_small = ImageFont.truetype(font_path, 28)
    font_xsmall = ImageFont.truetype(font_path, 24)

    player = Image.open("static/assets/icone.png").convert("RGBA").resize((500, 500))
    circle_center = (template.width // 2, 500)
    circle_radius = 215
    player = player.resize((int(player.width * 1.4), int(player.height * 1.4)))
    player = ImageOps.fit(player, (circle_radius * 2, circle_radius * 2), centering=(0.5, 0.4))
    mask = Image.new("L", (circle_radius * 2, circle_radius * 2), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, circle_radius * 2, circle_radius * 2), fill=255)
    player_cropped = Image.new("RGBA", (circle_radius * 2, circle_radius * 2))
    player_cropped.paste(player, (0, 0), mask=mask)
    paste_position = (circle_center[0] - circle_radius, circle_center[1] - circle_radius)
    card.paste(player_cropped, paste_position, mask=player_cropped)

    # Dicionário de clubes e arquivos de escudo
    logos = {
        "Sfera": "logo_sfera.png",
        "Atletico MG": "galo.png",
        "Bahia": "bahia.png",
        "Botafogo": "botafogo.png",
        "Ceara": "ceara.png",
        "Corinthians": "corinthians.png",
        "Cruzeiro": "cruzeiro.png",
        "Cuiaba": "cuiaba.png",
        "Flamengo": "flamengo.png",
        "Fluminense": "fluminense.png",
        "Fortaleza": "fortaleza.png",
        "Goias": "goias.png",
        "Inter": "inter.png",
        "Palmeiras": "palmeiras.png",
        "RB Bragantino": "RB Bragantino.png",
        "Santos": "santos.png",
        "São Paulo": "são paulo.png",
        "America MG": "america.png"
    }

    clube = jogador["Clube"]
    logo_filename = logos.get(clube, "logo_sfera.png")  # default: logo_sfera.png
    logo_path = os.path.join("static", "assets", logo_filename)
    escudo = Image.open(logo_path).convert("RGBA").resize((170, 170))

    flag = Image.open("static/assets/brasil.png").convert("RGBA").resize((210, 210))
    beta = Image.open("static/assets/beta.png").convert("RGBA").resize((210, 42))

    card.paste(escudo, (180, 125), mask=escudo)
    card.paste(flag, (680, 115), mask=flag)
    card.paste(beta, (780, 1430), mask=beta)

    bbox = draw.textbbox((0, 0), jogador_nome, font=font_big)
    x_centro = (card.width - (bbox[2] - bbox[0])) // 2
    draw.text((x_centro, 755), jogador_nome, font=font_big, fill="black")

    bbox = draw.textbbox((0, 0), str(overall), font=font_giga)
    x_centro = (card.width - (bbox[2] - bbox[0])) // 2
    draw.text((x_centro, 55), str(overall), font=font_giga, fill="#D3AF37")

    bbox = draw.textbbox((0, 0), "Overall KPI", font=font_xsmall)
    x_centro = (card.width - (bbox[2] - bbox[0])) // 2
    draw.text((x_centro, 35), "Overall KPI", font=font_xsmall, fill="white")

    bbox = draw.textbbox((0, 0), posicao_extenso, font=font_small)
    x_centro = (card.width - (bbox[2] - bbox[0])) // 2
    draw.text((x_centro, 850), posicao_extenso, font=font_small, fill="white")

    pos_coord = {"MAR": (398, 952), "COM": (398, 1057), "SUP": (398, 1168),
                 "CRI": (795, 952), "DIS": (795, 1057), "FIN": (795, 1168)}
    for k, v in atributos.items():
        draw.text(pos_coord[k], str(v), font=font_big, fill="white")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        temp_path = tmp.name
        card.save(temp_path)

    with open(temp_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    os.remove(temp_path)
    return f"data:image/png;base64,{encoded}"
