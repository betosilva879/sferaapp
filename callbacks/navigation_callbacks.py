# No arquivo callbacks/navigation_callbacks.py
from dash import Input, Output, State, callback_context, no_update
import dash
from dash import Input, Output, State, callback_context
from layouts.login_layout import login_layout
from layouts.main_layout import main_layout
from layouts.elenco_layout import elenco_layout
from layouts.jogador_layout import jogador_layout
from layouts.comparar_layout import comparar_layout


def register_navigation_callbacks(app):
    @app.callback(
        [Output('page-content', 'children'),
         Output('url', 'pathname'),
         Output('login-message-store', 'data')],
        [Input('login-button', 'n_clicks'),
         Input('elenco-btn', 'n_clicks'),
         Input('jogador-btn', 'n_clicks'),
         Input('comparar-btn', 'n_clicks'),
         Input('back-btn-elenco', 'n_clicks'),
         Input('back-btn-jogador', 'n_clicks'),
         Input('back-btn-comparar', 'n_clicks'),
         Input('url', 'pathname')],
        [State('email-input', 'value'),
         State('password-input', 'value')],
        prevent_initial_call=True
    )
    def handle_navigation(login_clicks, elenco_clicks, jogador_clicks, comparar_clicks,
                        back_elenco, back_jogador, back_comparar, pathname,
                        email, password):
        ctx = callback_context
        
        if not ctx.triggered:
            return login_layout(), no_update, None
            
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Login handling
        if trigger_id == 'login-button':
            if email == "sfera@com.br" and password == "@0565":
                return main_layout(), '/main', None
            else:
                return no_update, no_update, "Usuário ou senha incorretos."
        
        # Navigation handling
        if trigger_id == 'elenco-btn':
            return elenco_layout(), '/elenco', None
        elif trigger_id == 'jogador-btn':
            return jogador_layout(), '/jogador', None
        elif trigger_id == 'comparar-btn':
            return comparar_layout(), '/comparar', None
        elif 'back-btn' in trigger_id:
            return main_layout(), '/main', None
        
        # Pathname handling
        if pathname == '/main':
            return main_layout(), no_update, None
        elif pathname == '/elenco':
            return elenco_layout(), no_update, None
        elif pathname == '/jogador':
            return jogador_layout(), no_update, None
        elif pathname == '/comparar':
            return comparar_layout(), no_update, None
        
        return login_layout(), no_update, None