
from util.merge import merge
from util.api import StructureSchema
from apps.base.schema import ModelsSchemaWithExternal
from apps.subscription.constants import mode_constants
from apps.subscription.models import (
  Account,
  Announcement,
  System,
  Challenge,
  IP,
  Payment,
  Subscription,
)

from ....models import (
  FeeReport,
  TransactionReport,
  TransactionMatch,
)
from ...constants import api_constants
from .control import TransactinoControlSchema
from .common import CommonSchema

class SubscribedSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'This account has an active subscription.'
        ' Please refer to the README and review the available models.'
      ),
      children={
        api_constants.SCHEMA: TransactinoControlSchema(
          description='The schema accepts data in plaintext JSON and interacts with the API',
          children=merge(
            CommonSchema().children,
            {
              api_constants.MODELS: ModelsSchemaWithExternal(
                description='Models available to the user',
                children={
                  Model.__name__: Model.objects.schema(mode=mode_constants.SUBSCRIBED) for Model in [
                    Account,
                    Announcement,
                    System,
                    Challenge,
                    IP,
                    Payment,
                    Subscription,
                    FeeReport,
                    TransactionReport,
                    TransactionMatch,
                  ]
                },
              ),
            },
          ),
        ),
      },
    )
