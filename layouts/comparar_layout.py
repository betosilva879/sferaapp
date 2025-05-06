from dash import html, dcc
import dash_bootstrap_components as dbc

def comparar_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                # Sidebar
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Img(
                                src="/assets/logo_sfera.png",
                                style={
                                    'height': '70px',
                                    'display': 'block',
                                    'margin': '45px auto 30px'
                                }
                            )
                        ], className="text-center"),

                        html.H3(
                            "Comparar Jogadores",
                            style={
                                'color': '#C0C0C0',
                                'text-align': 'center',
                                'margin-bottom': '1px',
                                'font-size': '24px',
                                'font-weight': 'bold',
                                'letter-spacing': '1px'
                            }
                        ),

                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Categoria:", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-categoria',
                                        options=[
                                            {'label': 'Sub-20', 'value': 'sub20'},
                                            {'label': 'Sub-17', 'value': 'sub17'},
                                            {'label': 'Sub-15', 'value': 'sub15'}
                                        ],
                                        value='sub17',
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-right': '5px'}),

                                dbc.Col([
                                    dbc.Label("Ano:", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-ano',
                                        options=[
                                            {'label': '2023', 'value': '2023'},
                                            {'label': '2024', 'value': '2024'},
                                            {'label': '2025', 'value': '2025'}
                                        ],
                                        value='2024',
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-left': '5px'})
                            ]),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Posição (Sfera):", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-posicao-sfera',
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
                                        value="MA",
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-right': '5px'}),

                                dbc.Col([
                                    dbc.Label("Jogador (Sfera):", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-jogador-sfera',
                                        options=[],
                                        value="Gustavo",
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-left': '5px'})
                            ]),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Habilidade:", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-habilidade',
                                        options=[
                                            {'label': 'Marcação', 'value': 'marcação'},
                                            {'label': 'Competitividade', 'value': 'competitividade'},
                                            {'label': 'Superação', 'value': 'superação'},
                                            {'label': 'Distribuição', 'value': 'distribuição'},
                                            {'label': 'Criação', 'value': 'criação'},
                                            {'label': 'Finalização', 'value': 'finalização'},
                                        ],
                                        value='criação',
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-right': '5px'}),

                                
                                dbc.Col([
                                    dbc.Label("Clube (Comparado):", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-clube',
                                        options=[
                                                    {'label': 'Sfera', 'value': 'Sfera'},
                                                    {'label': 'Atletico MG', 'value': 'Atletico MG'},
                                                    {'label': 'Bahia', 'value': 'Bahia'},
                                                    {'label': 'Botafogo', 'value': 'Botafogo'},
                                                    {'label': 'Ceara', 'value': 'Ceara'},
                                                    {'label': 'Corinthians', 'value': 'Corinthians'},
                                                    {'label': 'Cruzeiro', 'value': 'Cruzeiro'},
                                                    {'label': 'Cuiaba', 'value': 'Cuiaba'},
                                                    {'label': 'Flamengo', 'value': 'Flamengo'},
                                                    {'label': 'Fluminense', 'value': 'Fluminense'},
                                                    {'label': 'Fortaleza', 'value': 'Fortaleza'},
                                                    {'label': 'Goias', 'value': 'Goias'},
                                                    {'label': 'Inter', 'value': 'Inter'},
                                                    {'label': 'Palmeiras', 'value': 'Palmeiras'},
                                                    {'label': 'RB Bragantino', 'value': 'RB Bragantino'},
                                                    {'label': 'Santos', 'value': 'Santos'},
                                                    {'label': 'São Paulo', 'value': 'São Paulo'},
                                                    {'label': 'America MG', 'value': 'America MG'}
                                        ],
                                        value="Fluminense",
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-left': '5px'})
                            ]),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Posição (Comparado):", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-posicao-comp',
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
                                        value="AD",
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-right': '5px'}),

                                dbc.Col([
                                    dbc.Label("Jogador (Comparado):", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-comp-jogador-comp',
                                        options=[],
                                        value="Matheus Reis",
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-left': '5px'})
                            ]),
                        ], className="dropdown-container", style={'margin-top': '0px'}),

                        html.Div(style={'height': '150px'}),

                        html.Div([
                            dbc.Button(
                                "Voltar",
                                id="back-btn-elenco",
                                className="circular-button",
                                n_clicks=0
                            )
                        ], className="button-containerele", style={
                            'position': 'relative',
                            'font-size': '14px',
                            'margin': '0px auto'
                        })

                    ], className="sidebar-jogador")

                ], md=3, style={'padding': '0'}),

                # Área de conteúdo
                dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Img(
                                        id="imagem-card-sfera",
                                        src="",
                                        style={
                                            "height": "270px",
                                            "display": "block",
                                            "margin": "0 auto",
                                            "object-fit": "contain"
                                        }
                                    )
                                ], className="analysis-box")
                            ], md=6),

                            dbc.Col([
                                html.Div([
                                    html.Img(
                                        id="imagem-card-comp",
                                        src="",
                                        style={
                                            "height": "270px",
                                            "display": "block",
                                            "margin": "0 auto",
                                            "object-fit": "contain"
                                        }
                                    )
                                ], className="analysis-box")
                            ], md=6),
                        ], className="mb-4"),

                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    dcc.Graph(
                                        id='radar-comparativo',
                                        config={'displayModeBar': False},
                                        style={'height': '270px', 'width': '100%'}
                                    )
                                ], className="analysis-box")
                            ], md=6),

                            dbc.Col([
                                html.Div([
                                    dcc.Graph(
                                        id='grafico-indicadores-comparativo',
                                        config={'displayModeBar': False},
                                        style={'height': '290px', 'width': '100%'}
                                    )
                                ], className="analysis-box")
                            ], md=6),
                        ], style={'margin-top': '8px'})
                    ], className="content-area")
                ], md=9, style={'padding': '0'})
            ], style={'height': 'calc(100vh - 16px)', 'margin': '8px 0'})
        ], fluid=True, style={'padding': '0', 'overflow': 'hidden'})
    ], className="main-container")
