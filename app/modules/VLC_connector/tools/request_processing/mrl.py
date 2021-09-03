import app.modules.VLC_connector.constants.uri as uri
from .. import validate_ip
from typing import Optional
import re


class MRL(object):
    def __init__(self):
        self.__access: Optional[str] = None  # Way to obtain media e.g. FILE, FTP
        self.__path: Optional["MRL.Path"] = None  # Path to file when yet in access
        self.host: Optional[str] = None  # Host or IP of the resource
        self.port: Optional[int] = None  # Port of host of the resource
        self.username: Optional[str] = None  # Username used for authentication of accessing the media
        self.password: Optional[str] = None  # Password used for authentication of accessing the media

    def __str__(self):
        return self.stringify()

    class Path:
        def __init__(self, path: str):
            path_split = path.split("/")
            file_split = path_split[-1].split(".")

            path_split.pop(-1)

            self.__path = "/".join(path_split)

            self.__file_extension = ""
            if len(file_split) > 1 and not not file_split[0]:  # if files are named for example .gitignore
                self.__file_extension = ".{}".format(file_split[-1])
                file_split.pop(-1)

            self.__filename = ".".join(file_split)

            self.__full_filename = ""
            if self.__filename:
                self.__full_filename += self.__filename

            if self.__file_extension:
                self.__full_filename += self.__file_extension

            self.__full_path = "{}/{}".format(self.__path, self.__full_filename)
            if not self.__path:
                self.__full_path = self.__full_filename
                if self.__path == "" and path != self.__full_filename:
                    self.__full_path = "/{}".format(self.__full_filename)

            if self.__full_path != path:
                raise RuntimeError("Something went wrong")

        @property
        def full(self):
            """Returns full path"""
            return self.__full_path

        @property
        def path(self):
            """Returns path without file"""
            return self.__path

        @property
        def file_extension(self):
            """Returns file extension with trailing dot"""
            return self.__file_extension

        @property
        def file_name(self):
            """Returns filename without extension"""
            return self.__filename

        @property
        def full_filename(self):
            """Returns filename with extension"""
            return self.__full_filename

    def from_url(self, url: str, **kwargs):
        """
        Sets parameters from user's inserted URL.
        :param url: URL which refers to media. For path division is used a slash "/"
        :return: MRL object
        """
        # /folder1/folder2/file
        # folder1/folder2/file
        # file:///folder1/folder2/file
        # file:///C:/folder1/folder2/file
        # ftp://ftp.com/File.mp4
        # ftp://admin@ftp.com/File.mp4
        # ftp://admin@ftp.com:5678/File.mp4
        # ftp://admin:administrator@ftp.com/File.mp4
        # ftp://admin:administrator@ftp.com:5678/File.mp4

        # "access://username:password@host:port/path"
        url_normalized = url.replace("\\", "/")
        url_split = url_normalized.split("//")  # ["access:", "username:password@host:port/path"]

        self.__access = uri.FILE  # default value

        if not len(url_split) == 1:
            self.__access = url_split[0].lower() + "//"
            if kwargs.get("check_access", False):
                if uri.uri_dict.get(self.__access) is None:
                    raise ValueError('Given access "{}" is not supported.'.format(self.__access))

        # ["access:", "username:password@host:port/path"] -> ["username:password@host:port/path"]
        url_split = [url_split[-1]]

        win_path_regex = "^/[A-Z]:/"
        # check if WIN like or UNIX like path, if WIN ["file:", "/path"] -> ["file:", "path"]
        if re.search(win_path_regex, url_split[0]):
            url_split[0] = url_split[0][1:]  # -> ["file:", "path"]

        url_split = url_split[0].split("@")  # ["username:password", "host:port/path"]
        if len(url_split) == 2:  # got authentication
            if url_split[0].startswith(":"):
                raise ResourceWarning("Password or username set, but not both.")

            self.username = url_split[0]  # default value if has not a second value
            auth_data = url_split[0].split(":")  # ["username", "password"]

            if len(auth_data) == 2:
                self.username, self.password = auth_data

            url_split.pop(0)  # ["username:password", "host:port/path"] -> ["host:port/path"]

        url_split = url_split[0].split("/")  # ["host:port", "path/path"]
        if len(url_split) >= 2:  # got authentication
            if ("." in url_split[0]) or url_split[0].lower().startswith("localhost"):  # first part is IP or host
                if url_split[0].startswith(":"):
                    raise ResourceWarning("IP of external file is not set.")

                self.host = url_split[0]  # default value if has not a second value
                auth_data = url_split[0].split(":")  # ["host", "port"]

                if len(auth_data) == 2:
                    self.host, self.port = auth_data[0], int(auth_data[1])

                url_split.pop(0)

        # self.__path = "/".join(url_split)
        self.__path = self.Path("/".join(url_split))

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
        self.__path = self.Path(path)
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        return self

    def using_ip(self):
        """Checks if IP is correct. If not, throws ValueError."""
        self.host = validate_ip(self.host)
        return self

    def stringify(self) -> str:
        """Returns prepared string of MRL."""
        mrl = self.__access

        if self.username:
            mrl = "{}{}".format(mrl, self.username)

        if self.password:
            mrl = "{}:{}".format(mrl, self.password)

        if self.username or self.password:
            mrl = "{}@".format(mrl)

        if self.host:
            mrl = "{}{}".format(mrl, self.host)

        if self.port:
            mrl = "{}:{}".format(mrl, self.port)

        if self.host:
            mrl = "{}/".format(mrl)

        if self.__access == "file://" and not self.path.full.startswith("/"):
            mrl = "{}/{}".format(mrl, self.__path.full)
        else:
            mrl = "{}{}".format(mrl, self.__path.full)

        return mrl

    @property
    def access(self) -> str:
        return self.__access

    @property
    def path(self) -> "MRL.Path":
        return self.__path


def create() -> MRL:
    """Creates an object of MRL"""
    return MRL()
