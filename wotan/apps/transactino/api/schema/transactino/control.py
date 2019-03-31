
from util.api import StructureSchema

from apps.subscription.models import Announcement

from ...constants import api_constants
from .constants import transactino_constants

class TransactinoControlSchema(StructureSchema):
  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    models_response = self.active_response.get_child(api_constants.MODELS)
    announcements_response = None
    if models_response is not None:
      announcements_response = models_response.get_child(Announcement.__name__)

    if announcements_response is None and Announcement.objects.active():
      self.active_response.force_get_child(transactino_constants.ANNOUNCEMENTS)
