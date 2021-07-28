import app.modules.VLC_connector.connector as Connector
import requests
import app.modules.VLC_connector.constants as constants


def check(connect: Connector):
    try:
        test_request = requests.get("http://{}:{}/requests/status.xml".format(connect.ip, connect.port),
                                    auth=(connect.username, connect.password), timeout=3)

    except ConnectionRefusedError as e:
        connect.status = constants.status_codes.WRONG_PORT_ERROR
        raise ConnectionRefusedError("Port is incorrect.", e)
    except TimeoutError as e:
        connect.status = constants.status_codes.CONNECTION_ERROR
        raise ConnectionRefusedError("The IP refers to offline host.", e)

    # TODO: Handle all possible incoming errors

    if test_request.status_code == 401:
        connect.status = constants.status_codes.AUTH_ERROR
        raise ValueError("Username or password to VLC is incorrect. Can't connect to VLC.")

    if not test_request.ok:
        connect.status = constants.status_codes.CONNECTION_ERROR
        raise ConnectionError("Can't connect to VLC. Check if VLC runs and if enabled 'Web' in Settings -> "
                              "All -> Interface -> Main Interfaces.")
    connect.status = constants.status_codes.OK
