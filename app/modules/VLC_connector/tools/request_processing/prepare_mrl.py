import app.modules.VLC_connector.constants.uri as uri


def mrl_prepare(access: str, path: str, ip: str = None, port: int = None, username: str = None, password: str = None) \
        -> str:
    if ((port or username or password) and not ip) or (access != uri.FILE and not ip):
        raise ResourceWarning("IP of external file is not set.")

    if (username and not password) or (password and not username):
        raise ResourceWarning("Password or username set, but not both.")

    mrl = access

    if username:
        mrl = "{}{}".format(mrl, username)

    if password:
        mrl = "{}:{}".format(mrl, password)

    if username or password:
        mrl = "{}@".format(mrl)

    if ip:
        mrl = "{}{}".format(mrl, ip)

    if port:
        mrl = "{}:{}".format(mrl, port)

    if ip:
        mrl = "{}/".format(mrl)

    mrl = "{}{}".format(mrl, path)

    return mrl
