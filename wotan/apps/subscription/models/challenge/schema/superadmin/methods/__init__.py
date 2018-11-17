
from util.api import StructureSchema

from apps.base.schema.methods.constants import method_constants
from apps.base.schema.methods.filter import FilterSchema
from apps.base.schema.methods.get import GetSchema

from ......schema.methods.set import SetSchemaWithChallenge
from .constants import set_constants

class ChallengeSuperadminModelMethodsSchema(StructureSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(
      **kwargs,
      description='',
      children={
        method_constants.FILTER: FilterSchema(Model),
        method_constants.GET: GetSchema(Model),
        method_constants.SET: SetSchemaWithChallenge(
          Model,
          mode=mode,
          origin=set_constants.ORIGIN,
        ),
      },
    )
