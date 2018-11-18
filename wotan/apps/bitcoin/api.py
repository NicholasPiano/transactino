
from util.merge import merge
from util.api import Schema, StructureSchema, types, map_type, errors

from apps.base.schema import ModelsSchemaWithExternal
from apps.rowbot.models import (
  Address,
  Block,
)

class api_constants:
  MODELS = 'models'
  SYSTEM = 'system'

api = StructureSchema(
  description='',
  children={
    api_constants.MODELS: ModelsSchemaWithExternal(
      description='',
      children={
        Model.__name__: Model.objects.schema() for Model in [
          Address,
          Block,
        ]
      },
    ),
    api_constants.SYSTEM: StructureSchema(
      description='',
      children={

      },
    ),
    'socket': Schema(),
    'message': Schema(),
  },
)
