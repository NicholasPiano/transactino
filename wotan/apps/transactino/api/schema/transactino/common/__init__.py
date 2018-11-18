
from constants import application_constants

from util.api import StructureSchema

from .message import MessageSchema
from .readme import ReadmeSchema
from .socket import SocketSchema
from .system import SystemSchema
from .models import ModelsSchemaWithChallenges

class CommonSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      application_constants.SYSTEM: SystemSchema(),
      application_constants.SOCKET: SocketSchema(),
      application_constants.MESSAGE: MessageSchema(),
      application_constants.README: ReadmeSchema(),
    }
