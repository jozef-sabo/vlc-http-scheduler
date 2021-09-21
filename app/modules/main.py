import vlc_connector
from vlc_connector import connector
import flaskr


if __name__ == "__main__":
    flask_app = flaskr.create_app()

    flask_app.run(host="localhost", debug=True, port=80)
    print("aa")

    # conn = VLC_connector.connector.connect("localhost", "administrator")
    # conn.toggle_fullscreen()
