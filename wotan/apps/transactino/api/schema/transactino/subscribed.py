
from util.merge import merge
from util.api import StructureSchema
from apps.base.schema import ModelsSchemaWithExternal
from apps.subscription.constants import mode_constants
from apps.subscription.models import (
  Account,
  System,
  Challenge,
  IP,
  Payment,
  Subscription,
)

from ....models import FeeReport
from .constants import transactino_constants
from .common import CommonSchema

class SubscribedSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'This account has an active subscription. '
        'Please refer to the README and review the available models'
      ),
      children=merge(
        {
          transactino_constants.SCHEMA: StructureSchema(
            description='The schema accepts data in plaintext JSON and interacts with the API',
            children={
              transactino_constants.MODELS: ModelsSchemaWithExternal(
                description='Models available to the user',
                children={
                  Model.__name__: Model.objects.schema(mode=mode_constants.SUBSCRIBED) for Model in [
                    Account,
                    System,
                    Challenge,
                    IP,
                    Payment,
                    Subscription,
                    FeeReport,
                  ]
                },
              ),
            },
          ),
        },
      ),
    )
