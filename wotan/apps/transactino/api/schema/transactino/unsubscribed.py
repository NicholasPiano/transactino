
from util.merge import merge
from util.api import StructureSchema
from apps.base.schema import ModelsSchemaWithExternal
from apps.subscription.constants import mode_constants
from apps.subscription.models import (
  Account,
  System,
  Subscription,
  Challenge,
  Payment,
)

from .constants import transactino_constants
from .common import CommonSchema

class UnsubscribedSchema(StructureSchema):
  def __init__(self, context=None, **kwargs):

    models = [
      Account,
      Challenge,
      System,
    ]

    account = context.get_account()
    if account.is_verified:
      models.extend([
        Subscription,
        Payment,
      ])

    super().__init__(
      **kwargs,
      description=(
        'The account does not have an active subscription. '
        'Refer to the Subscription model to create one'
      ),
      children=merge(
        {
          transactino_constants.SCHEMA: StructureSchema(
            description='The schema accepts data in plaintext JSON and interacts with the API',
            children={
              transactino_constants.MODELS: ModelsSchemaWithExternal(
                description='Models available to the user',
                children={
                  Model.__name__: Model.objects.schema(mode=mode_constants.UNSUBSCRIBED)
                  for Model
                  in models
                },
              ),
            },
          ),
        },
      ),
    )
