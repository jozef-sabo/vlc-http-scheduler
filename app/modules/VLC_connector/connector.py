from . import tools
from . import actions
import app.modules.VLC_connector.constants as constants
import app.modules.VLC_connector.constants.uri as uri
from multipledispatch import dispatch


def connect(ip: str, password: str, port=8080, username="", **kwargs):
    """
    Creates a connection object, which is used to control VLC.
    :param ip: IPv4 address of VLC web server
    :param password: Password for auth on VLC web server set in VLC settings
    :param port: (Optional) Port used to connect to VLC web server. Default is "8080".
    :param username: (Optional) Username for auth on VLC web server set in VLC settings. Default is blank.
    :param args:
    :param kwargs: (Optional) check_conn: bool - defines, if needed to try connection when Connector is created.
    Default is True.
    :return: Connection object
    :rtype: Connector
    """
    init_check = kwargs.get("check_conn", True)
    ip = tools.validate_ip(ip)
    return Connector(ip, password, port, username, init_check)


class Connector(object):
    def __init__(self, ip: str, password: str, port: int, username: str, init_check: bool):
        self.ip = tools.validate_ip(ip)
        self.password = password
        self.port = port
        self.username = username
        self.__init_check = init_check
        self.status = constants.status_codes.OK_WITHOUT_TEST

        if self.__init_check:
            tools.check_conn_vlc.check(self)

    @dispatch()
    def play(self):
        actions.play(self)

    @dispatch(str, str)
    def play(self, access: str, path: str, **kwargs):
        ip = kwargs.get("ip", None)
        port = kwargs.get("port", None)
        username = kwargs.get("username", None)
        password = kwargs.get("password", None)

        mrl = tools.request_processing.mrl_prepare(access, path, ip, port, username, password)
        actions.play(self, inp=mrl)

    @dispatch(int)
    def play(self, identifier: int):
        actions.play(self, identifier=identifier)

    def stop(self):
        pass

    def pause(self):
        pass

    def toggle_pause(self):
        pass

    def next(self):
        pass

    def previous(self):
        pass

    def playlist_empty(self):
        pass

    def is_paused(self) -> bool:
        return False

    def is_stopped(self) -> bool:
        return False
