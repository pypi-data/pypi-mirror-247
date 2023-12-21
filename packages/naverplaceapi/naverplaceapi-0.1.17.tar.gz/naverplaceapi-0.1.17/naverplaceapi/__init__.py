import logging

from .mixin.announce import AnnouncementMixin
from .mixin.booking import BookingMixin
from .mixin.broadcast import BroadcastMixin
from .mixin.category import CategoryMixin
from .mixin.menu import MenuMixin
from .mixin.place import PlaceMixin
from .mixin.promotions import PromotionsMixin
from .mixin.review import ReviewMixin

__VERSION__ = "0.1.12"

DEFAULT_LOGGER = logging.getLogger("naverplaceapi")


class Client(
    PlaceMixin,
    ReviewMixin,
    BroadcastMixin,
    PromotionsMixin,
    AnnouncementMixin,
    BookingMixin,
    MenuMixin,
    CategoryMixin
):
    pass
