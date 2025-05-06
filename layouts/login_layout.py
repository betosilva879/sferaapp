from dash import html
import dash_bootstrap_components as dbc

def login_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    # Logo centralizada
                    html.Div([
                        html.Img(
                            src="/assets/logo_sfera.png",
                            style={
                                'height': '102px',
                                'margin-bottom': '20px',
                                'display': 'block',
                                'margin-left': 'auto',
                                'margin-right': 'auto'
                            }
                        )
                    ], className="text-center mb-2"),
                    
                    # Título adicionado
                    html.H2(
                        "Sfera Analytics App",
                        style={
                            'color': '#C0C0C0',
                            'text-align': 'center',
                            'margin-bottom': '30px',
                            'font-weight': 'bold',
                            'letter-spacing': '1px'
                        }
                    ),
                    
                    # Card de login
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Input(
                                    id="email-input",
                                    type="email",
                                    placeholder="E-mail",
                                    className="mb-3 login-input",
                                    style={'width': '100%'}
                                ),
                                dbc.Input(
                                    id="password-input",
                                    type="password",
                                    placeholder="Senha",
                                    className="mb-3 login-input",
                                    style={'width': '100%'}
                                ),
                                # Espaço aumentado acima do botão
                                html.Div(style={'height': '15px'}),  
                                html.Div(
                                    dbc.Button(
                                        "Entrar",
                                        id="login-button",
                                        className="login-button",
                                        n_clicks=0
                                    ),
                                    className="text-center"
                                ),
                                html.Div(
                                    id="login-message-display",
                                    className="mt-3 text-center login-message"
                                ),
                                # Texto "Powered by"
                                html.Div(
                                    "Powered by Beta Sigma Analytics\u00ae",
                                    style={
                                        'color': '#C0C0C0',
                                        'font-size': '12px',
                                        'text-align': 'center',
                                        'margin-top': '25px',  # Aumentado
                                        'letter-spacing': '0.5px'
                                    }
                                )
                            ])
                        ], className="login-card")
                    ], style={
                        'width': '350px',
                        'margin': '0 auto'
                    })
                ], className="d-flex flex-column align-items-center justify-content-center", 
                   style={"height": "100vh"})
            ])
        ], fluid=True, className="login-container")
    ], className="main-container")