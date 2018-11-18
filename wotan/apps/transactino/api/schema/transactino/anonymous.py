
from util.merge import merge
from util.api import StructureSchema

from apps.subscription.constants import mode_constants
from apps.subscription.models import Account, Challenge

from .constants import transactino_constants
from .common import CommonSchema

class AnonymousSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'Welcome to the Transactino interface '
        'Please refer to the README and the glossary '
        'for more information.'
      ),
      children=merge(
        {
          transactino_constants.SCHEMA: StructureSchema(
            description='The schema accepts data in plaintext JSON',
            children={
              transactino_constants.MODELS: StructureSchema(
                description='Models available to the user',
                children={
                  Account.__name__: Account.objects.schema(mode=mode_constants.ANONYMOUS),
                },
              ),
            },
          ),
        },
      ),
    )
