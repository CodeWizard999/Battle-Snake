import logging
import os
import typing

from flask import Flask
from flask import request
from gevent.pywsgi import WSGIServer
from gevent import monkey


def run_server(handlers: typing.Dict):
    # monkey.patch_all()
    app = Flask("Battlesnake")

    @app.get("/")
    def on_info():
        return handlers["info"]()

    @app.post("/start")
    def on_start():
        game_state = request.get_json()
        handlers["start"](game_state)
        return "ok"

    @app.post("/move")
    def on_move():
        game_state = request.get_json()
        return handlers["move"](game_state)

    @app.post("/end")
    def on_end():
        game_state = request.get_json()
        handlers["end"](game_state)
        return "ok"

    @app.after_request
    def identify_server(response):
        response.headers.set(
            "server", "battlesnake/github/starter-snake-python"
        )
        return response

    app.debug = True
    port = int(os.environ["PORT"]) if "PORT" in os.environ else 8080
    http = WSGIServer(('0.0.0.0', port), app.wsgi_app)
    print(f"Starting Server on Port {port}")
    
    http.serve_forever()
