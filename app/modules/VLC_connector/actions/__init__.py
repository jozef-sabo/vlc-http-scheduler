from . import command
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import connector


def play(connect: "connector.Connector", inp: str = None, identifier: int = None):
    """
    Plays an actual item or playlist in VLC. If playlist empty or nothing selected, nothing will happen.
    :param identifier:
    :param inp:
    :param connect: VLC Connector class
    """

    if inp:
        command.command(connect, "in_play", "input={}".format(inp))
        return

    if identifier:
        command.command(connect, "pl_play", "id={}".format(identifier))
        return

    command.command(connect, "pl_play")


def stop(connect: "connector.Connector"):
    """
    Stops an actual item in VLC. If playlist empty or nothing selected, nothing will happen.
    :param connect: VLC Connector class
    """
    command.command(connect, "pl_stop")
