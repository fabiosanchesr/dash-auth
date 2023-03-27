import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from utils.login_handler import restricted_page
from models import Users, db

load_dotenv()

# Exposing the Flask Server to enable configuring it for logging in
server = Flask(__name__)


# @server.route('/login', methods=['POST'])
# def login_button_click():
#     if request.form:
#         username = request.form['username']
#         password = request.form['password']
#         if VALID_USERNAME_PASSWORD.get(username) is None:
#             return """invalid username and/or password <a href='/login'>login here</a>"""
#         if VALID_USERNAME_PASSWORD.get(username) == password:
#             login_user(Users(username))
#             if 'url' in session:
#                 if session['url']:
#                     url = session['url']
#                     session['url'] = None
#                     return redirect(url) ## redirect to target url
#             return redirect('/') ## redirect to home
#         return """invalid username and/or password <a href='/login'>login here</a>"""


app = dash.Dash(
    __name__, server=server, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SIMPLEX]
)

# Keep this out of source code repository - save in a file or a database
#  passwords should be encrypted
VALID_USERNAME_PASSWORD = {"test": "test", "hello": "world"}


# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server.config.update(SECRET_KEY=os.urandom(33))

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"



@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return Users(username)


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        html.Div(id="user-status-header"),
        html.Hr(),
        dash.page_container,
    ]
)


@app.callback(
    Output("user-status-header", "children"),
    Output('url','pathname'),
    Input("url", "pathname"),
    Input({'index': ALL, 'type':'redirect'}, 'n_intervals')
)
def update_authentication_status(path, n):
    ### logout redirect
    if n:
        if not n[0]:
            return '', dash.no_update
        else:
            return '', '/login'

    ### test if user is logged in
    if current_user.is_authenticated:
        if path == '/login':
            return dcc.Link("logout", href="/logout"), '/'
        return dcc.Link("logout", href="/logout"), dash.no_update
    else:
        ### if page is restricted, redirect to login and save path
        if path in restricted_page:
            session['url'] = path
            return dcc.Link("login", href="/login"), '/login'

    ### if path not login and logout display login link
    if current_user and path not in ['/login', '/logout']:
        return dcc.Link("login", href="/login"), dash.no_update

    ### if path login and logout hide links
    if path in ['/login', '/logout']:
        return '', dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)