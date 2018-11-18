
from util.merge import merge
from util.api import StructureSchema
from apps.base.schema import ModelsSchemaWithExternal
from apps.subscription.constants import mode_constants
from apps.subscription.models import (
  Account,
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
            children={
              transactino_constants.MODELS: ModelsSchemaWithExternal(
                children={
                  Model.__name__: Model.objects.schema(mode=mode_constants.SUBSCRIBED) for Model in [
                    Account,
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
