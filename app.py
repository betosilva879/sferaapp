import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask import Flask

# Inicialização
server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    assets_folder="static/assets"
)

# Layout base completo
app.layout = html.Div([
    # Componentes de roteamento e estado
    dcc.Location(id='url', refresh=True),
    dcc.Store(id='login-state', storage_type='session'),
    dcc.Store(id='login-message-store'),  # Armazena mensagens de login
    
    # Container principal de conteúdo
    html.Div(id='page-content'),
    
    # Componentes ocultos para callbacks
    html.Div([
        # Botões de navegação
        dbc.Button(id='login-button', style={'display': 'none'}),
        dbc.Button(id='elenco-btn', style={'display': 'none'}),
        dbc.Button(id='jogador-btn', style={'display': 'none'}),
        dbc.Button(id='comparar-btn', style={'display': 'none'}),
        
        # Botões de voltar
        dbc.Button(id='back-btn-elenco', style={'display': 'none'}),
        dbc.Button(id='back-btn-jogador', style={'display': 'none'}),
        dbc.Button(id='back-btn-comparar', style={'display': 'none'}),
        
        # Inputs de login
        dbc.Input(id='email-input', style={'display': 'none'}),
        dbc.Input(id='password-input', type='password', style={'display': 'none'})
    ], style={'display': 'none'})
])

# Importações de layouts e callbacks
from layouts.login_layout import login_layout
from layouts.main_layout import main_layout
from layouts.elenco_layout import elenco_layout
from layouts.jogador_layout import jogador_layout
from layouts.comparar_layout import comparar_layout

from callbacks.navigation_callbacks import register_navigation_callbacks
register_navigation_callbacks(app)
from callbacks.elenco_callbacks import register_elenco_callbacks
register_elenco_callbacks(app)
from callbacks.jogador_callbacks import register_jogador_callbacks
register_jogador_callbacks(app)
from callbacks.comparar_callbacks import register_comparar_callbacks
register_comparar_callbacks(app)




if __name__ == '__main__':
    app.run(debug=True)