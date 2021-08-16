import app.modules.VLC_connector.constants.uri as uri
from .. import validate_ip
from typing import Optional


class MRL(object):
    def __init__(self):
        self.__access: Optional[str] = None  # Way to obtain media e.g. FILE, FTP
        self.__path: Optional[str] = None  # Path to file when yet in access
        self.__host: Optional[str] = None  # Host or IP of the resource
        self.__port: Optional[int] = None  # Port of host of the resource
        self.__username: Optional[str] = None  # Username used for authentication of accessing the media
        self.__password: Optional[str] = None  # Password used for authentication of accessing the media

    def __str__(self):
        return self.stringify()

    def from_url(self, url: str):
        """
        Sets parameters from user's inserted URL.
        :param url: URL which refers to media. For path division is used a slash "/"
        :return:
        """
        # ftp://ftp.com/File.mp4
        # ftp://admin@ftp.com/File.mp4
        # ftp://admin@ftp.com:5678/File.mp4
        # ftp://admin:administrator@ftp.com/File.mp4
        # ftp://admin:administrator@ftp.com:5678/File.mp4

        # "access://username:password@host:port/path"
        url_split = url.split("//")  # ["access:", "username:password@host:port/path"]

        self.__access = "http://"  # default value
        if len(url_split) == 2:  # got prefix / access
            self.__access = url_split[0]
            if url_split[1].startswith("/"):  # "file:///path" -> ["file:", "/path"]
                self.__access = uri.FILE
                url_split[1] = url_split[1].removeprefix("/")  # -> ["file:", "path"]

            url_split.pop(0)  # ["access:", "username:password@host:port/path"] -> ["username:password@host:port/path"]

        url_split = url_split[0].split("@")  # ["username:password", "host:port/path"]
        if len(url_split) == 2:  # got authentication
            if url_split[0].startswith(":"):
                raise ResourceWarning("Password or username set, but not both.")

            self.__username = url_split[0]  # default value if has not a second value
            auth_data = url_split[0].split(":")  # ["username", "password"]

            if len(auth_data) == 2:
                self.__username, self.__password = auth_data

            url_split.pop(0)  # ["username:password", "host:port/path"] -> ["host:port/path"]

        url_split = url_split[0].split("/")  # ["host:port", "path/path"]
        if len(url_split) >= 2:  # got authentication
            if ("." in url_split[0]) or url_split[0].lower().startswith("localhost"):  # first part is IP or host
                if url_split[0].startswith(":"):
                    raise ResourceWarning("IP of external file is not set.")

                self.__host = url_split[0]  # default value if has not a second value
                auth_data = url_split[0].split(":")  # ["host", "port"]

                if len(auth_data) == 2:
                    self.__host, self.__port = auth_data

                url_split.pop(0)

        self.__path = "/".join(url_split)

        return self

    def from_parameters(
            self,
            access: str,
            path: str,
            host: str = None,
            port: int = None,
            username: str = None,
            password: str = None
    ):
        """
        Sets parameters from user's parameters specification.
        :param access: Way to obtain media e.g. FILE, FTP
        :param path: Path to file when yet in access
        :param host: Host or IP of the resource
        :param port: Port of host of the resource
        :param username: Username used for authentication of accessing the media
        :param password: Password used for authentication of accessing the media
        :return: The invoked mrl instance
        """
        if access != uri.FILE and not host:
            raise ResourceWarning("IP of external file is not set.")

        if bool(username) ^ bool(password):
            raise ResourceWarning("Password or username set, but not both.")

        self.__access = access
        self.__path = path
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password

        return self

    def using_ip(self):
        """Checks if IP is correct. If not, throws ValueError."""
        self.__host = validate_ip(self.__host)
        return self

    def stringify(self) -> str:
        """Returns prepared string of MRL."""
        mrl = self.__access

        if self.__username:
            mrl = "{}{}".format(mrl, self.__username)

        if self.__password:
            mrl = "{}:{}".format(mrl, self.__password)

        if self.__username or self.__password:
            mrl = "{}@".format(mrl)

        if self.__host:
            mrl = "{}{}".format(mrl, self.__host)

        if self.__port:
            mrl = "{}:{}".format(mrl, self.__port)

        if self.__host:
            mrl = "{}/".format(mrl)

        mrl = "{}{}".format(mrl, self.__path)

        return mrl

    @property
    def access(self) -> str:
        return self.__access

    @property
    def path(self) -> str:
        return self.__path

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password


def create() -> MRL:
    """Creates an object of MRL"""
    return MRL()
