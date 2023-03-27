import dash
import dash_bootstrap_components as dbc
import database as db
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from models import Users
from sqlalchemy import func


dash.register_page(__name__)


username_input = html.Div(
    [
        dbc.Label("Username", html_for="username"),
        dbc.Input(type="text", id="username", placeholder="Enter your username"),
    ],
    className="mb-3",
)


passwor_input = html.Div(
    [
        dbc.Label("Password", html_for="password"),
        dbc.Input(type="password", id="password", placeholder="Enter password"),
    ],
    className="mb-3",
)


logged = html.Div('')


button = dbc.Button("Submit", color="primary", id='login_btn', n_clicks=0)


form = dbc.Form([username_input, passwor_input, button])


# Login screen
layout = html.Div(
    [
        html.Div(form),
        html.Div(children='', id='output-state')
    ],
    className="d-flex justify-content-center"
)


@callback(
    Output('url_login', 'pathname'),
    Input('login_btn', 'n_clicks'),
    [
        State('username', 'value'),
        State('password', 'value'),
    ]
)
def successful(n_clicks, input1, input2):
    user = db.session.query(Users).filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user('/success')
        else:
            pass
    else:
        pass
@callback(
    Output('output-state', 'children'),
    Input('login_btn', 'n_clicks'),
    [
        State('username', 'value'),
        State('password', 'value'),
    ]
)
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = db.session.query(Users).filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Invalid userane or password'
        else:
            return 'Invalid userane or password'
    else:
        return '/heatmap'


# html.Form(
#     [
#         html.H2("Please log in to continue:", id="h1"),
#         dbc.Col(
#             [
#                 dbc.Row(
#                     dcc.Input(placeholder="Enter your username", type="text", id="uname-box", name='username'),
#                     class_name="mb-3",
#                     justify="center",
#                 ),
#                 dbc.Row(
#                     dcc.Input(placeholder="Enter your password", type="password", id="pwd-box", name='password'),
#                     class_name="mb-3",
#                 ),
#                 dbc.Row(
#                     html.Button(children="Login", n_clicks=0, type="submit", id="login-button"),
#                     class_name="mb-3",
#                 ),    
#             ],
#             align="center",
#             width={"size": 3, "offset": 3},
#             class_name="mb-3",
#         ),
#         html.Div(children="", id="output-state")
#     ], method='POST'
# )