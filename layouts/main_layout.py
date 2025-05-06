from dash import html
import dash_bootstrap_components as dbc

def main_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                # Sidebar - Esquerda
                dbc.Col([
                    html.Div([
                        # Cabeçalho do Sidebar
                        html.Div([
                            html.Img(
                                src="/assets/logo_sfera.png",
                                style={
                                    'height': '70px',
                                    'display': 'block',
                                    'margin': '25px auto 25px auto'  # Reduzi a margem inferior
                                }
                            ),
                            html.H3(
                                "Tipo de Análise",
                                style={
                                    'color': '#C0C0C0',
                                    'text-align': 'center',
                                    'margin-bottom': '0px',  # Reduzido de 30px
                                    'font-size': '24px',     # Reduzido de 28px
                                    'font-weight': 'bold',
                                    'letter-spacing': '1px'
                                }
                            )
                        ], className="sidebar-header"),

                        # Container dos Botões Circulares
                        html.Div([
                            dbc.Button(
                                "Elenco",
                                id="elenco-btn",
                                className="circular-button",
                                n_clicks=0,
                                style={'font-size': '14px', 'margin': '20px auto'}
                            ),
                            dbc.Button(
                                "Jogador",
                                id="jogador-btn",
                                className="circular-button",
                                n_clicks=0,
                                style={'font-size': '14px', 'margin': '20px auto'}
                            ),
                            dbc.Button(
                                "Comparar",
                                id="comparar-btn",
                                className="circular-button",
                                n_clicks=0,
                                style={'font-size': '14px', 'margin': '20px auto'}
                            )
                        ], className="button-container", style={
                            'margin': '20px 0'  # Adicionado margem controlada
                        }),

                        # Rodapé do Sidebar
                        html.Div(
                            html.Img(
                                src="/assets/beta.png",
                                style={
                                    'height': '20px'
                                }
                            ),
                            className="sidebar-footer",
                            style={
                                'margin-top': 'auto',
                                'padding': '0px 0',
                                'display': 'flex',
                                'justify-content': 'center'
                            }
                        )

                    ], className="sidebar", style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'height': '100vh',
                        'padding': '20px 0'
                    })
                ], md=3, style={'padding': '0'}),
                
                # Área de Conteúdo - Direita
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.H2(
                                "Galeria",
                                style={
                                    'color': '#C0C0C0',
                                    'font-size': '35px',
                                    'font-weight': 'bold',
                                    'margin': '0',
                                    'padding': '0 10px 0 0'
                                }
                            ),
                            html.Img(
                                src="/assets/best_player.png",
                                style={
                                    'height': '65px',
                                    'margin-top': '5px'
                                }
                            )
                        ], style={
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'margin-top': '50px'
                        }),
                        html.H5(
                            "Ano : 2024",
                            style={
                                'color': '#C0C0C0',
                                'text-align': 'center',
                                'margin-top': '5px',
                                'font-size': '14px'
                            }
                        ),
                        html.H5(
                            "Categoria : Sub-17",
                            style={
                                'color': '#C0C0C0',
                                'text-align': 'center',
                                'margin-bottom': '30px',
                                'font-size': '14px'
                            }
                        ),
                        html.Div([
                            html.Img(
                                src="/assets/guilherme2.png",
                                style={
                                    'width': '25%',
                                    'height': 'auto',
                                    'box-shadow': '0 2px 12px rgba(0, 0, 0, 0.4)',
                                    'border-radius': '12px',
                                    'margin': '0 2% 0 0'
                                }
                            ),
                            html.Img(
                                src="/assets/geovanni2.png",
                                style={
                                    'width': '25%',
                                    'height': 'auto',
                                    'box-shadow': '0 2px 12px rgba(0, 0, 0, 0.4)',
                                    'border-radius': '12px',
                                    'margin': '0 2%'
                                }
                            ),
                            html.Img(
                                src="/assets/murilo2.png",
                                style={
                                    'width': '25%',
                                    'height': 'auto',
                                    'box-shadow': '0 2px 12px rgba(0, 0, 0, 0.4)',
                                    'border-radius': '12px',
                                    'margin': '0 0 0 2%'
                                }
                            )
                        ], style={
                            'display': 'flex',
                            'justify-content': 'center',
                            'align-items': 'center',
                            'gap': '20px',
                            'margin-bottom': '30px'
                        }),

                        html.Div(id='main-content')
                    ], className="content-area")
                ], md=9, style={'padding': '0'})
            ], style={
                'height': '100vh',
                'margin': '0',
                'overflow': 'hidden'
            })
        ], fluid=True, style={
            'padding': '0',
            'height': '100vh'
        })
    ], className="main-container")