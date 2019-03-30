
from util.api import (
  StructureSchema,
)

from apps.base.schema.methods.constants import method_constants

from ......constants import mode_constants
from .constants import challenge_method_constants
from .respond import ChallengeRespondSchema
from .get import ChallengeGetSchema

class ChallengeModelMethodsSchema(StructureSchema):
  def __init__(self, Model):
    super().__init__(
      description=(
        'Methods for the Challenge model'
      ),
      children={
        challenge_method_constants.RESPOND: ChallengeRespondSchema(),
        method_constants.GET: ChallengeGetSchema(),
      },
    )
