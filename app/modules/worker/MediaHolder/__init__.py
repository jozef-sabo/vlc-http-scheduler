from app.modules.VLC_connector.tools.request_processing import mrl
from . import types
import hashlib
from typing import List, Optional
import os
import datetime

NOT_INITIALIZED_ERROR: RuntimeError = RuntimeError("Media not initialized yet")


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

    def add(self, media_resource_locator: mrl.MRL):
        new_media = Media(media_resource_locator)
        new_media.ingest()

        common_name = [media for media in self.media if new_media.display_name == media.display_name]
        if common_name:
            raise ValueError("Display name must be unique")
        self.media.append(new_media)
        return new_media

    def rename_media(self, renamed_media: "Media", new_display_name: str) -> None:
        if renamed_media not in self.media:
            renamed_media.latest_display_name, renamed_media.display_name = renamed_media.display_name, new_display_name
            return

        common_name = [media for media in self.media if renamed_media.display_name == media.display_name]
        if common_name:
            raise ValueError("Display name must be unique")
        renamed_media.latest_display_name, renamed_media.display_name = renamed_media.display_name, new_display_name

    def get_media(self, display_name: str = None):
        if not display_name:
            return self.media[:]

        searched_media = [media for media in self.media if media.display_name == display_name][0]

        return searched_media

    def check_integrity(self, with_deletion: bool = False) -> List["Media"]:
        not_capable_media = []

        for media_order in range(len(self.media)):
            media = self.media[media_order]

            media_integrity = media.check_integrity()

            if not media_integrity:
                not_capable_media.append(media_order)

        if with_deletion:
            for media_order in not_capable_media[::-1]:
                self.media.pop(media_order)

        not_capable_media = [self.media[media_order] for media_order in not_capable_media]

        return not_capable_media


class Media(object):
    def __init__(self, media_resource_locator: mrl.MRL, display_name: str = None) -> None:
        self.mrl: mrl.MRL = media_resource_locator

        #  keeps only filename without path and extension
        self.display_name = self.mrl.path.file_name
        if display_name:
            self.display_name = display_name

        # keeps track of last used display_name
        self.latest_display_name = self.display_name

        self.type: Optional[str] = None
        self.SHA_256: Optional[str] = None
        self.size: Optional[int] = None
        self.creation_date: Optional[datetime.datetime] = None

        self.__ingested: bool = False

    def ingest(self, offline_accessible: bool = False):
        if self.__ingested:
            return

        if self.mrl.access == mrl.uri.FILE:  # path refers to file
            self.SHA_256 = SHA_256(self.mrl.path.full)
            self.size = os.path.getsize(self.mrl.path.full)
        else:
            if offline_accessible:
                # TODO: download file
                pass
        self.creation_date = datetime.datetime.now()

        self.__ingested = True

    def media_of_type(self, media_type: str):
        media_type_normalized = types.together.get(media_type)
        if media_type_normalized is None:
            raise ValueError("Media type is not correct")

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
        if self.mrl.access == mrl.uri.FILE:  # path refers to file
            if not os.path.isfile(self.mrl.path.full):
                return False

            if self.size != os.path.getsize(self.mrl.path.full):
                return False

            if self.SHA_256 != SHA_256(self.mrl.path.full):
                return False
        else:
            pass

        if self.creation_date != datetime.datetime.now():
            return False

        if not self.__ingested:
            return False

        return True


def create() -> MediaHolder:
    """Creates MediaHolder instance"""
    return MediaHolder()
