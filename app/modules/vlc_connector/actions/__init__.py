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


def pause(connect: "connector.Connector"):
    pass
    # TODO: pause an item without toggling when paused


def toggle_pause(connect: "connector.Connector"):
    """
    Toggles a pause of an actual item in VLC. If playlist empty or nothing selected, nothing will happen.
    :param connect: VLC Connector class
    """
    command.command(connect, "pl_pause")


def next_item(connect: "connector.Connector"):
    """
    Plays next item in playlist in VLC. If playlist empty or nothing after current item, nothing will happen.
    :param connect: VLC Connector class
    """
    command.command(connect, "pl_next")


def previous_item(connect: "connector.Connector"):
    """
    Plays next item in playlist in VLC. If playlist empty nothing will happen. Otherwise if nothing before current item,
    the current item will be played
    :param connect: VLC Connector class
    """
    command.command(connect, "pl_previous")


def playlist_empty(connect: "connector.Connector"):
    """
    Clears the whole playlist in VLC. If something playing, it stops and clears it as well.
    :param connect: VLC Connector class
    """
    command.command(connect, "pl_empty")


def toggle_fullscreen(connect: "connector.Connector"):
    """
    Toggles a fullscreen mode in VLC. If playlist empty or nothing selected, nothing will happen.
    :param connect: VLC Connector class
    """
    command.command(connect, "fullscreen")
