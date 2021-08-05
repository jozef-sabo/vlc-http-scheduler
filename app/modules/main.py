import VLC_connector
from VLC_connector import connector


if __name__ == "__main__":
    conn = VLC_connector.connector.connect("localhost", "administrator")

    conn.toggle_fullscreen()
