from dash import Input, Output
import dash_bootstrap_components as dbc

def register_login_message_callbacks(app):
    @app.callback(
        Output('login-message-display', 'children'),
        Input('login-message-store', 'data')
    )
    def show_login_message(message):
        if message:
            return dbc.Alert(message, color="danger", dismissable=True)
        return None