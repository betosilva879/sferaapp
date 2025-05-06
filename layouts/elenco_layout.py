from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm


def elenco_layout():
    # Carregar dados (substituiremos por MySQL depois)
    atletas_df = pd.read_excel('data/atletas.xlsx')

    # Carregar dados para o gráfico (u17br.xlsx)
    u17_df = pd.read_excel('data/u17br.xlsx')
    sfera_df = u17_df[u17_df['Clube'] == 'Sfera'].copy()
    sfera_df["MinutosJogados"] = pd.to_numeric(sfera_df["MinutosJogados"], errors="coerce")

    # Filtro inicial (MA - Meia Armador)
    posicao_df = atletas_df[atletas_df['Posição'] == 'MA']
    
    # Criar tabela Dash
    tabela = dash_table.DataTable(
        id='tabela-jogadores',
        columns=[
            {"name": "Jogador", "id": "Jogador"},
            {"name": "KPI", "id": "KPI"},
            {"name": "Minutagem", "id": "Minutagem"},
            {"name": "Ranking na posição", "id": "Ranking na posição"}
        ],
        data=posicao_df.to_dict('records'),
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#011f4B",
            "color": "#3CBBB1",
            "borderBottom": "1px solid #3CBBB1"
        },
        style_cell={
            "backgroundColor": "#011f4B",
            "color": "white",
            "fontSize": "12px",
            "border": "1px solid #3CBBB1",
            "textAlign": "left"
        },
        style_cell_conditional=[
            {"if": {"column_id": "Ranking na posição"}, "textAlign": "right"},
            {"if": {"column_id": "Minutagem"}, "textAlign": "right"}
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(60, 187, 177, 0.1)'
            }
        ],
        style_as_list_view=True
    )

    # faixa da minutagem
    bins = [0, 250, 500, 750, 1000, float("inf")]
    labels_bins = ["0–250", "250–500", "500–750", "750–1000", "1000+"]
    sfera_df["Faixa Minutos"] = pd.cut(sfera_df["MinutosJogados"], bins=bins, labels=labels_bins, right=False)

    contagem = sfera_df["Faixa Minutos"].value_counts().sort_index()


    fig = go.Figure(go.Bar(
    x=contagem.values,
    y=contagem.index,
    orientation='h',
    marker=dict(color="#3CBBB1"),
    text=contagem.values,
    textposition="auto"
    ))

    fig.update_layout(
        title=dict(
            text="Distribuição de minutos jogados (elenco)",
            x=0.5,  # centraliza
            y=0.97,
            font=dict(size=14, color="#c0c0c0",family="Arial Black")
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=9),
        xaxis=dict(
            title=dict(text="Número de Jogadores", font=dict(size=9, color="white")),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text="Minutos Jogados", font=dict(size=9, color="white")),
            showgrid=False
        ),
        margin=dict(l=5, r=5, t=50, b=30),
        height=260
    )

    # CURVA NORMAL
    # Vamos iniciar como posição MA (padrão), igual ao dropdown inicial.

    posicao_inicial = "MA"

    # Todos os jogadores da posição
    df_geral = u17_df[u17_df["Posição"] == posicao_inicial].copy()
    df_geral["KPI"] = pd.to_numeric(df_geral["KPI"], errors="coerce")
    kpis_gerais = df_geral["KPI"].dropna()

    # Jogadores do Sfera na posição
    df_sfera = atletas_df[atletas_df["Posição"] == posicao_inicial].copy()
    df_sfera["KPI"] = pd.to_numeric(df_sfera["KPI"], errors="coerce")
    kpis_sfera = df_sfera["KPI"].dropna()

    # Cálculo da curva normal
    media = kpis_gerais.mean()
    desvio = kpis_gerais.std()
    x_vals = np.linspace(media - 3*desvio, media + 3*desvio, 500)
    y_vals = norm.pdf(x_vals, media, desvio)

    # Montar a figura
    fig_kpi = go.Figure()

    # Curva normal
    fig_kpi.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode="lines",
        name="Distribuição",
        line=dict(color="#3CBBB1", width=2)
    ))

    # Linha de base
    fig_kpi.add_trace(go.Scatter(
        x=[x_vals.min(), x_vals.max()],
        y=[0, 0],
        mode="lines",
        line=dict(color="#C0C0C0", width=1),
        showlegend=False
    ))

    # Pontos de todos os times
    fig_kpi.add_trace(go.Scatter(
        x=kpis_gerais,
        y=[0] * len(kpis_gerais),
        mode="markers",
        marker=dict(size=8, color='rgba(255, 255, 255, 0.2)'),
        name="Brasileiro sub-17",
        hoverinfo="skip"
    ))

    # Pontos do Sfera
    fig_kpi.add_trace(go.Scatter(
        x=kpis_sfera,
        y=[0] * len(kpis_sfera),
        mode="markers",
        marker=dict(size=10, color="#3CBBB1"),
        name="Sfera sub-17",
        text=df_sfera["Jogador"],
        hovertemplate="%{text}<br>KPI: %{x:.2f}<extra></extra>"
    ))

    # Layout geral do gráfico
    fig_kpi.update_layout(
        title=dict(
            text="Distribuição do desempenho por posição",
            x=0.5,
            y=1,
            font=dict(size=14, color="#C0C0C0", family="Arial Black")
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=260,
        font=dict(size=10, color="white"),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="white"
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1,
            font=dict(size=10, color="white")
        )
    )

    # DONUTS

    acima_media = 0
    abaixo_media = 0

    for _, jogador in atletas_df.iterrows():
        posicao_jogador = jogador["Posição"]
        kpi_jogador = jogador["KPI"]
        media_posicao = u17_df[u17_df["Posição"] == posicao_jogador]["KPI"].mean()
        if kpi_jogador > media_posicao:
            acima_media += 1
        else:
            abaixo_media += 1

    labels = ["Acima da média", "Abaixo da média"]
    values = [acima_media, abaixo_media]
    colors = ["#3CBBB1", "#C0C0C0"]

    fig_donut = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color="#011f4B", width=2)),
        textinfo="percent+label",
        textfont=dict(color="white", size=10),
        insidetextorientation="radial"
    )])

    fig_donut.update_layout(
        title=dict(
            text="Proporção dos destaques (elenco)",
            x=0.5,
            y=0.97,
            font=dict(size=14, color="#C0C0C0", family="Arial Black")
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="white")
        ),
        height=250,
        margin=dict(t=60, b=0, l=0, r=0)
    )

    return html.Div([
        dbc.Container([
            dbc.Row([
                # Sidebar
                dbc.Col([
                    html.Div([
                        # Logo
                        html.Div([
                            html.Img(
                                src="/assets/logo_sfera.png",
                                style={
                                    'height': '70px',
                                    'display': 'block',
                                    'margin': '25px auto 25px'
                                }
                            )
                        ], className="text-center"),
                        
                        # Título
                        html.H3(
                            "Análise do Elenco",
                            style={
                                'color': '#C0C0C0',
                                    'text-align': 'center',
                                    'margin-bottom': '0px',  # Reduzido de 30px
                                    'font-size': '24px',     # Reduzido de 28px
                                    'font-weight': 'bold',
                                    'letter-spacing': '1px'
                            }
                        ),
                        
                        # Dropdowns
                        html.Div([
                            dbc.Label("Categoria:", className="dropdown-label"),
                            dcc.Dropdown(
                                id='dropdown-categoria',
                                options=[
                                    {'label': 'Sub-20', 'value': 'sub20'},
                                    {'label': 'Sub-17', 'value': 'sub17'},
                                    {'label': 'Sub-15', 'value': 'sub15'}
                                ],
                                value='sub17',
                                clearable=False,
                                className="dropdown-style"
                            ),
                            
                            dbc.Label("Ano de Análise:", className="dropdown-label"),
                            dcc.Dropdown(
                                id='dropdown-ano',
                                options=[
                                    {'label': '2023', 'value': '2023'},
                                    {'label': '2024', 'value': '2024'},
                                    {'label': '2025', 'value': '2025'}
                                ],
                                value='2024',
                                clearable=False,
                                className="dropdown-style"
                            ),
                            
                            dbc.Label("Posição:", className="dropdown-label"),
                            dcc.Dropdown(
                                id='dropdown-posicao',
                                options=[
                                    {'label': 'Lateral Direito', 'value': 'LD'},
                                    {'label': 'Zagueiro Direito', 'value': 'ZD'},
                                    {'label': 'Zagueiro Esquerdo', 'value': 'ZE'},
                                    {'label': 'Lateral Esquerdo', 'value': 'LE'},
                                    {'label': 'Volante', 'value': 'VO'},
                                    {'label': 'Meia Armador', 'value': 'MA'},
                                    {'label': 'Atacante Direito', 'value': 'AD'},
                                    {'label': 'Atacante Esquerdo', 'value': 'AE'},
                                    {'label': 'Centroavante', 'value': 'CA'}
                                ],
                                value='MA',
                                clearable=False,
                                className="dropdown-style"
                            ),
                            # Espaço flexível entre dropdowns e botão
                            
                        ], className="dropdown-container"),

                        html.Div(style={'flex': '1'}),

                        # Botão Voltar
                        html.Div([
                            dbc.Button(
                                "Voltar",
                                id="back-btn-elenco",
                                className="circular-button",
                                n_clicks=0
                            ),                  
                        ], className="button-containerele"),

                        # Rodapé
                        
                    ], className="sidebar-elenco")
                ], md=3, style={'padding': '0'}),
                
                # Área de conteúdo
                dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5(
                                        "Ranking de desempenho por posição",
                                        style={
                                            'color': '#C0C0C0',
                                            'fontSize': '16px',
                                            'marginBottom': '15px',
                                            'fontWeight': 'bold',
                                            'textAlign': 'center'
                                        }
                                    ),
                                    html.Div(
                                        tabela,
                                        style={'marginTop': '35px'}
                                    )
                                ], className="analysis-box")
                            ], md=6),
                            dbc.Col([
                                html.Div([
                                    dcc.Graph(
                                        id='grafico-minutagem',
                                        figure=fig,
                                        config={'displayModeBar': False}
                                    )
                                ], className="analysis-box")
                            ], md=6)
                        ], className="mb-4"),

                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    dcc.Graph(
                                        id='grafico-distribuicao-kpi',
                                        figure=fig_kpi,
                                        config={'displayModeBar': False}
                                    )
                                ], className="analysis-box")
                            ], md=6),
                            dbc.Col([
                                html.Div([
                                    dcc.Graph(
                                        id='grafico-donut-destaques',
                                        figure=fig_donut,
                                        config={'displayModeBar': False}
                                    )
                                ], className="analysis-box")
                            ], md=6)
                        ])
                    ], className="content-area")
                ], md=9, style={'padding': '0'})
            ], style={'height': '100vh', 'margin': '0'})
        ], fluid=True, style={'padding': '0'})
    ], className="main-container")