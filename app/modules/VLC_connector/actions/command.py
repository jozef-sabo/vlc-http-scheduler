import requests
from app.modules.VLC_connector import tools
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import connector


def command(connect: "connector.Connector", cmd: str, value: str = None):
    tools.check_conn_vlc.check(connect)

    url = "http://{}:{}/requests/status.xml?command={}".format(connect.ip, connect.port, cmd)

    if value:
        url = "http://{}:{}/requests/status.xml?command={}&{}".format(connect.ip, connect.port, cmd, value)

    request = requests.get(url, auth=(connect.username, connect.password))
    print(request.text)
