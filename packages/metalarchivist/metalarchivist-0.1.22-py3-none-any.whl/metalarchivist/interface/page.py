

from .base import Page, Pages
from .genre import BandGenre
from .album import AlbumReleases



class GenrePage(Page, data_type=BandGenre):
    ...


class GenrePages(Pages, data_type=GenrePage):
    ...


class ReleasePage(Page, data_type=AlbumReleases):    
    ...


class ReleasePages(Pages, data_type=ReleasePage):
    ...
