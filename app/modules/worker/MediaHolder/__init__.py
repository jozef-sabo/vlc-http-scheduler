from app.modules.VLC_connector.tools.request_processing import mrl
from . import types
import hashlib
from typing import List, Optional
import os
import datetime


def SHA_256(path: str) -> str:
    sha256_hash = hashlib.sha256()

    with open(path, "rb") as media_file:
        for byte_block in iter(lambda: media_file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


class MediaHolder:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __init__(self) -> None:
        self.media: List[Media] = []

    def add(self, media_resource_locator: mrl.MRL) -> "Media":
        """
        Adds and ingests media by MRL.
        :param media_resource_locator: MRL object of inserted media.
        :return: instance of Media class
        """
        new_media = Media(media_resource_locator)
        new_media.ingest()

        common_name = [selected_media for selected_media in self.media if
                       new_media.display_name == selected_media.display_name]
        if common_name:
            raise ValueError("Display name must be unique")
        self.media.append(new_media)
        return new_media

    def add_using_name(self, media_resource_locator: mrl.MRL, name: str) -> "Media":
        """
        Adds and ingests media by MRL using given name.
        :param name: Display name of Media
        :param media_resource_locator: MRL object of inserted media.
        :return: instance of Media class
        """

        common_name = [selected_media for selected_media in self.media if
                       name == selected_media.display_name]

        if common_name:
            raise ValueError("Display name must be unique")

        new_media = Media(media_resource_locator)
        new_media.ingest()
        self.rename_media(new_media, name)

        self.media.append(new_media)
        return new_media

    def rename_media(self, renamed_media: "Media", new_display_name: str) -> None:
        """
        Renames any media of Media class. If renaming causes duplicate name in MediaHolder, raises error.
        :param renamed_media: Media to be renamed
        :param new_display_name: New display name of renamed_media
        :return: None
        """
        if renamed_media not in self.media:
            renamed_media.latest_display_name, renamed_media.display_name = renamed_media.display_name, new_display_name
            return

        common_name = [selected_media for selected_media in self.media
                       if new_display_name == selected_media.display_name]
        if common_name:
            raise ValueError("Display name must be unique")
        renamed_media.latest_display_name, renamed_media.display_name = renamed_media.display_name, new_display_name

    def get_media(self, display_name: str = None):
        """
        Returns all Media unless display_name is set; then returns only Media with that name
        :param display_name: [Optional] Name of media
        :return: Media or list of Media
        """
        if display_name is None:
            return self.media[:]

        searched_media = [selected_media for selected_media in self.media
                          if selected_media.display_name == display_name]

        return searched_media[0] if len(searched_media) != 0 else None

    def check_integrity(self, with_deletion: bool = False) -> List["Media"]:
        """
        Checks an integrity of all Media in MediaHolder. If some is violated, returns it in list.
        :param with_deletion: [Optional] If True, removes the media from MediaHolder when integrity is violated.
        :return: List of integrity violated media.
        """
        not_capable_media_order = []

        for media_order in range(len(self.media)):
            selected_media = self.media[media_order]

            media_integrity = selected_media.check_integrity()

            if not media_integrity:
                not_capable_media_order.append(media_order)

        not_capable_media = [self.media[media_order] for media_order in not_capable_media_order]

        if with_deletion:
            for media_order in not_capable_media_order[::-1]:
                self.media.pop(media_order)

        return not_capable_media

    def remove_media(self, display_name: str = None) -> None:
        """
        Removes all Media unless display_name is set; then removes only Media with that name
        :param display_name: [Optional] Name of media
        :return: Media or list of Media
        """
        if not display_name:
            self.media = []
            return

        [self.media.remove(selected_media) for selected_media in self.media if selected_media.display_name == display_name]


class Media(object):
    def __init__(self, media_resource_locator: mrl.MRL, display_name: str = None) -> None:
        self.mrl: mrl.MRL = media_resource_locator

        #  keeps only filename without path and extension
        self.display_name = self.mrl.path.file_name
        if display_name:
            self.display_name = display_name

        # keeps track of last used display_name
        self.latest_display_name = self.display_name

        # if none type set
        self.type: str = types.FEATURE

        self.SHA_256: Optional[str] = None
        self.size: Optional[int] = None
        self.creation_date: Optional[datetime.datetime] = None

        self.__ingested: bool = False

    def ingest(self, offline_accessible: bool = False) -> None:
        if self.__ingested:
            return

        # TODO: check If playable in VLC

        if self.mrl.access == mrl.uri.FILE:  # path refers to file
            self.SHA_256 = SHA_256(self.mrl.path.full)
            self.size = os.path.getsize(self.mrl.path.full)
        else:
            if offline_accessible:
                # TODO: download file
                pass
        self.creation_date = datetime.datetime.now()

        self.__ingested = True

    def media_of_type(self, media_type: str) -> "Media":
        """
        Sets type of media being added. Valid one is only constant in types.together or names of types.
        :param media_type: String or constant which represents type of media
        :return: instance of Media class
        """
        media_type_normalized = types.together.get(media_type)
        if media_type_normalized is None:
            if media_type not in types.together.values():
                raise ValueError("Media type is not correct")
            media_type_normalized = media_type

        self.type = media_type_normalized
        return self

    @property
    def feature(self):
        self.type = types.FEATURE
        return self

    @property
    def trailer(self):
        self.type = types.TRAILER
        return self

    @property
    def teaser(self):
        self.type = types.TEASER
        return self

    @property
    def test(self):
        self.type = types.TEST
        return self

    @property
    def rating(self):
        self.type = types.RATING
        return self

    @property
    def advertisement(self):
        self.type = types.ADVERTISEMENT
        return self

    @property
    def short(self):
        self.type = types.SHORT
        return self

    @property
    def transitional(self):
        self.type = types.TRANSITIONAL
        return self

    @property
    def psa(self):
        self.type = types.PSA
        return self

    def check_integrity(self) -> bool:
        if self.mrl.access == mrl.uri.FILE:  # path refers to file, not FTP and others
            if not os.path.isfile(self.mrl.path.full):
                return False

            if self.size != os.path.getsize(self.mrl.path.full):
                return False

            if self.SHA_256 != SHA_256(self.mrl.path.full):
                return False
        else:
            pass

        if not self.__ingested:
            return False

        return True


default_media_holder = MediaHolder()

media = default_media_holder.media


def add(media_resource_locator: mrl.MRL) -> "Media":
    """Calls :meth:`add <MediaHolder.add>` on the
    :data:`default MediaHolder instance <default_media_holder>`.
    """
    return default_media_holder.add(media_resource_locator)


def add_using_name(media_resource_locator: mrl.MRL, name: str) -> "Media":
    """Calls :meth:`add <MediaHolder.add_sung_name>` on the
    :data:`default MediaHolder instance <default_media_holder>`.
    """
    return default_media_holder.add_using_name(media_resource_locator, name)


def rename_media(renamed_media: "Media", new_display_name: str) -> None:
    """Calls :meth:`rename_media <MediaHolder.rename_media>` on the
    :data:`default MediaHolder instance <default_media_holder>`.
    """
    return default_media_holder.rename_media(renamed_media, new_display_name)


def get_media(display_name: str = None):
    """Calls :meth:`get_media <MediaHolder.get_media>` on the
    :data:`default MediaHolder instance <default_media_holder>`.
    """
    return default_media_holder.get_media(display_name)


def remove_media(display_name: str = None):
    """Calls :meth:`get_media <MediaHolder.remove_media>` on the
    :data:`default MediaHolder instance <default_media_holder>`.
    """
    return default_media_holder.remove_media(display_name)


def check_integrity(with_deletion: bool = False) -> List["Media"]:
    """Calls :meth:`get_media <MediaHolder.check_integrity>` on the
    :data:`default MediaHolder instance <default_media_holder>`.
    """
    return default_media_holder.check_integrity(with_deletion)
