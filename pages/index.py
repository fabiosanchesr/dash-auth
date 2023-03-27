import dash
from dash import html, Dash, dcc, Input, Output, callback
from utils.login_handler import require_login


dash.register_page(__name__, path='/')
require_login(__name__)

layout = html.Div([
    html.H1("INDEX")
])