from typing import List
from dataclasses import dataclass

from spotipy.serialise import SerialisableDataclass, Timestamp
from spotipy.model.album.base import Album
from spotipy.model.member import Copyright
from spotipy.model.track import SimpleTrackPaging
from spotipy.model.paging import OffsetPaging


@dataclass
class FullAlbum(Album):
    """
    Available markets is available when market is not specified.

    The presence of is_playable is undocumented
    and it appears to only be True when it is present.
    """
    copyrights: List[Copyright]
    external_ids: dict
    genres: List[str]
    label: str
    popularity: int
    tracks: SimpleTrackPaging
    available_markets: List[str] = None
    is_playable: True = None

    def __post_init__(self):
        super().__post_init__()
        self.copyrights = [Copyright(**c) for c in self.copyrights]
        self.tracks = SimpleTrackPaging(**self.tracks)


@dataclass
class SavedAlbum(SerialisableDataclass):
    added_at: Timestamp
    album: FullAlbum

    def __post_init__(self):
        self.added_at = Timestamp.from_string(self.added_at)
        self.album = FullAlbum(**self.album)


@dataclass
class SavedAlbumPaging(OffsetPaging):
    items: List[SavedAlbum]

    def __post_init__(self):
        self.items = [SavedAlbum(**a) for a in self.items]
