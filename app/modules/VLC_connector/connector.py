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
        """
        Plays an actual item in VLC. If playlist empty or nothing selected, nothing will happen.
        """
        actions.play(self)

    @dispatch(str, str)
    def play(self, access: str, path: str, **kwargs):
        """
        Plays an inserted mrl in VLC. If playlist empty or nothing selected, nothing will happen.
        :param access: Type of media resource e.g. FILE, FTP and more.
        :param path: An actual path of accessed media without protocol (e.g. ftp://).
        :param kwargs:
        ip: IP of server where accessed media comes from (required always if access is not FILE)
        port: Port of server where accessed media comes from (optional)
        username: Username for user authentication to server where accessed media comes from (optional, required if
        password set)
        password: Password for user authentication to server where accessed media comes from (optional, required if
        username set)
        """
        ip = kwargs.get("ip", None)
        port = kwargs.get("port", None)
        username = kwargs.get("username", None)
        password = kwargs.get("password", None)

        mrl = tools.request_processing.mrl.create().from_parameters(
            access, path, ip, port, username, password
        ).stringify()
        actions.play(self, inp=mrl)

    @dispatch(int)
    def play(self, identifier: int):
        """
        Plays item in VLC by id in playlist. If playlist empty or nothing selected, nothing will happen.
        :param identifier: ID of item in current playlist.
        """
        actions.play(self, identifier=identifier)

    def stop(self):
        """
        Stops an actual item in VLC. If playlist empty or nothing selected, nothing will happen.
        """
        actions.stop(self)

    def pause(self):
        actions.pause(self)

    def toggle_pause(self):
        """
        Toggles a pause of an actual item in VLC. If playlist empty or nothing selected, nothing will happen.
        """
        actions.toggle_pause(self)

    def next(self):
        """
        Plays next item in playlist in VLC. If playlist empty or nothing after current item, nothing will happen.
        """
        actions.next_item(self)

    def previous(self):
        """
        Plays next item in playlist in VLC. If playlist empty nothing will happen. Otherwise if nothing before current
        item, the current item will be played.
        """
        actions.previous_item(self)

    def playlist_empty(self):
        """
        Clears the whole playlist in VLC. If something playing, it stops and clears it as well.
        """
        actions.playlist_empty(self)

    def is_paused(self) -> bool:
        return False

    def is_stopped(self) -> bool:
        return False

    def toggle_fullscreen(self):
        """
        Toggles a fullscreen mode in VLC. If playlist empty or nothing selected, nothing will happen.
        """
        actions.toggle_fullscreen(self)
