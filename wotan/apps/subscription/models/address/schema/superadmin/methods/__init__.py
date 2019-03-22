
from util.api import StructureSchema

from apps.base.schema.methods.constants import method_constants
from apps.base.schema.methods.filter import FilterSchema
from apps.base.schema.methods.get import GetSchema

from ......schema.methods.set import SetSchemaWithChallenge
from ......schema.methods.create import CreateSchemaWithChallenge
from .constants import set_constants, create_constants

class AddressSuperadminModelMethodsSchema(StructureSchema):
  def __init__(self, mode=None, **kwargs):
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
        method_constants.CREATE: CreateSchemaWithChallenge(
          Model,
          mode=mode,
          origin=create_constants.ORIGIN,
        )
      },
    )
