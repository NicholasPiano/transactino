
from util.api import StructureSchema

from apps.base.schema.methods.constants import method_constants

from .get import PaymentGetSchema

class PaymentModelMethodsSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(Model, **kwargs)
    self.children = {
      method_constants.GET: PaymentGetSchema(),
    }
