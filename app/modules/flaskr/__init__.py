import os
from flask import Flask
from flask import redirect
import app.modules.vlc_connector.connector as connector
import queue


def create_app(queue_to_main: queue.LifoQueue = None, queue_to_flask: queue.LifoQueue = None):
    app = Flask(__name__)
    app.static_folder = "./static/"

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    conn = connector.connect("localhost", "administrator", check_conn=True)

    @app.route('/')
    def index():
        return app.send_static_file("index.html")

    @app.route('/css/<path:path>', methods=["GET"])
    def css(path):
        return app.send_static_file("css/" + path)

    @app.route('/js/<path:path>', methods=["GET"])
    def js(path):
        return app.send_static_file("js/" + path)

    @app.route("/api/play")
    def play():

        conn.play()
        return redirect("/", 302)

    @app.route("/api/pause")
    def pause():
        conn.toggle_pause()
        return redirect("/", 302)

    @app.route("/api/stop")
    def stop():
        conn.stop()
        return redirect("/", 302)

    @app.route("/api/fullscreen")
    def fullscreen():
        conn.toggle_fullscreen()
        return redirect("/", 302)

    return app
