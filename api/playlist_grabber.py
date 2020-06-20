import tekore as tk
import os
from flask import Flask, Response, session, jsonify
from functools import wraps

spotify_conf = tk.config_from_environment()
spotfy_cred = tk.Credentials(*spotify_conf)
spotify = tk.Spotify()

user_to_token = {}
app = Flask(__name__)

# Decorate to ensure user is logged in to spotify
def spotify_user_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user = session.get('spotify_user', None)
        if user is None:
            # There is no logged in user --> Send to login page
            return jsonify({'redirect': spotfy_cred.user_authorisation_url(scope=tk.scope.playlist_read_private)})
        else:
            user_token: tk.Token = user_to_token.get(user, None)
            if user_token.is_expiring:
                user_token = user_token.refresh_token(user_token)
                user_to_token[user] = user_token
            return f(*args, **kwargs)
    return wrap


@app.route('/')
def show_playlist(path):
    return jsonify({'Hello': 'World :-)'})


