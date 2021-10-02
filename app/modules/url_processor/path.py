
class Path:
    def __init__(self, path: str):
        path = path.replace("\\", "/")

        path_split = path.split("/")
        file_split = path_split[-1].split(".")

        path_split.pop(-1)

        self.__path = "/".join(path_split)
        if len(path_split) == 1 and not path_split[0]:
            self.__path = "/"

        self.__file_extension = ""
        if len(file_split) > 1 and not not file_split[0]:  # if files are named with leading dot, e.g. .gitignore
            self.__file_extension = ".{}".format(file_split[-1])
            file_split.pop(-1)

        self.__filename = ".".join(file_split)

        self.__full_filename = ""
        if self.__filename:
            self.__full_filename += self.__filename

        if self.__file_extension:
            self.__full_filename += self.__file_extension

        self.__full_path = "{}/{}".format(self.__path, self.__full_filename)
        if self.__path == "/":
            self.__full_path = "/{}".format(self.__full_filename)
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
