
from util.merge import merge
from util.api import StructureSchema
from apps.base.schema import ModelsSchemaWithExternal
from apps.subscription.constants import mode_constants
from apps.subscription.models import (
  Account,
  Address,
  Challenge,
  Discount,
  IP,
  Payment,
  Subscription,
)

from .....models import FeeReport
from ..constants import transactino_constants
from ..common import CommonSchema
from .constants import superadmin_constants

class SuperadminTopLevelSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      children=merge(
        {
          transactino_constants.SCHEMA: StructureSchema(
            children={
              transactino_constants.MODELS: ModelsSchemaWithExternal(
                children={
                  Model.__name__: Model.objects.schema(mode=mode_constants.SUPERADMIN) for Model in [
                    Account,
                    Address,
                    Challenge,
                    Discount,
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
