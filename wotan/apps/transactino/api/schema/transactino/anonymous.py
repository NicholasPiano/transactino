
from util.merge import merge
from util.api import StructureSchema

from apps.subscription.constants import mode_constants
from apps.subscription.models import Account, System

from ...constants import api_constants
from .common import CommonSchema

class AnonymousSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'Welcome to the Transactino interface'
        ' Please refer to the README and the glossary'
        ' for more information.'
      ),
      children={
        api_constants.SCHEMA: StructureSchema(
          description='The schema accepts data in plaintext JSON and interacts with the API',
          children=merge(
            CommonSchema(mode=mode_constants.ANONYMOUS).children,
            {
              api_constants.MODELS: StructureSchema(
                description='Models available to the user',
                children={
                  Model.__name__: Model.objects.schema(mode=mode_constants.ANONYMOUS)
                  for Model
                  in [
                    Account,
                    System,
                  ]
                },
              ),
            },
          ),
        ),
      },
    )
