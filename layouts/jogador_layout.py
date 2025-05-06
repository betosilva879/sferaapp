from dash import html, dcc
import dash_bootstrap_components as dbc

def jogador_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                # Sidebar
                dbc.Col([
                    html.Div([
                        # Logo (com caminho atualizado)
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
                        
                        # Título
                        html.H3(
                            "Análise Individual",
                            style={
                                'color': '#C0C0C0',
                                'text-align': 'center',
                                'margin-bottom': '1px',
                                'font-size': '24px',
                                'font-weight': 'bold',
                                'letter-spacing': '1px'
                            }
                        ),

                        # Dropdowns
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Categoria:", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-categoria',
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
                                        id='dropdown-ano',
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
                                    dbc.Label("Posição:", className="dropdown-label", style={'margin-bottom': '2px'}),
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
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-right': '5px'}),

                                dbc.Col([
                                    dbc.Label("Jogador:", className="dropdown-label", style={'margin-bottom': '2px'}),
                                    dcc.Dropdown(
                                        id='dropdown-jogador', value=None,
                                        options=[],
                                        placeholder="Jogador",
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-left': '5px'}),
                            ]),

                            dbc.Label("Habilidade:", className="dropdown-label", style={'margin-bottom': '2px'}),
                            dcc.Dropdown(
                                id='dropdown-habilidade-principal',
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
                            ),

                            dbc.Label("Indicadores para Scatterplot:", className="dropdown-label", style={'margin-bottom': '2px'}),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='dropdown-scatter-x',
                                        options=[
                                            {'label': var, 'value': var} for var in [
                                                'xA', 'xG', 'Assistências', 'Gols', 'ChutesNoGol', 'AssistênciasChute',
                                                'Interceptações', 'RecuperaçãoPosse', 'DisputasVencidas', 'Faltas',
                                                'Passes', 'PassesTerçoFinal', 'CruzamentosCorretos', 'Dribles'
                                            ]
                                        ],
                                        placeholder="Eixo X",
                                        value='Gols',
                                        clearable=False,
                                        className="dropdown-style",
                                        style={'margin-bottom': '1px'}
                                    )
                                ], width=6, style={'padding-right': '5px'}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='dropdown-scatter-y',
                                        options=[
                                            {'label': var, 'value': var} for var in [
                                                'xA', 'xG', 'Assistências', 'Gols', 'ChutesNoGol', 'AssistênciasChute',
                                                'Interceptações', 'RecuperaçãoPosse', 'DisputasVencidas', 'Faltas',
                                                'Passes', 'PassesTerçoFinal', 'CruzamentosCorretos', 'Dribles'
                                            ]
                                        ],
                                        placeholder="Eixo Y",
                                        clearable=False,
                                        className="dropdown-style",
                                        value='Assistências',
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
                            'font-size': '14px', 'margin': '0px auto'
                        }),
                    ], className="sidebar-jogador")
                ], md=3, style={'padding': '0'}),

                dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Img(
                                        id="imagem-card",
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
                                    dcc.Graph(
                                        id='radar-jogador',
                                        config={'displayModeBar': False},
                                        style={'height': '270px'} 
                                    )
                                ], className="analysis-box")
                            ], md=6),                      
                        ], className="mb-4"),
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    dcc.Graph(
                                        id='grafico-indicadores-habilidade',
                                        config={'displayModeBar': False},
                                        style={'height': '290px', 'width': '95%'}
                                    )
                                ], className="analysis-box")
                            ], md=6),
                            dbc.Col([
                                html.Div([  
                                    dcc.Graph(
                                        id='scatterplot-indicadores',
                                        config={'displayModeBar': False},
                                        style={'height': '270px', 'width': '100%'}
                                    )
                                ], className="analysis-box")
                            ], md=6),
                        ], style={'margin-top': '8px'})
                    ], className="content-area")
                ], md=9, style={'padding': '0'})
            ], style={'height': 'calc(100vh - 16px)', 'margin': '8px 0'})
        ], fluid=True, style={'padding': '0', 'overflow': 'hidden'})
    ], className="main-container")
