
from util.api import StructureSchema

from apps.subscription.constants import mode_constants

from ..constants import transactino_constants
from .system import SystemSchema
from .announcements import AnnouncementsSchema
from .readme import ReadmeSchema
from .socket import SocketSchema

class CommonSchema(StructureSchema):
  def __init__(self, mode=None, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      transactino_constants.README: ReadmeSchema(),
      transactino_constants.SOCKET: SocketSchema(),
    }

    if mode != mode_constants.ANONYMOUS:
      self.children.update({
        transactino_constants.SYSTEM: SystemSchema(),
        transactino_constants.ANNOUNCEMENTS: AnnouncementsSchema(),
      })
