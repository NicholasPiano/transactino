
from apps.base.schema import ModelSchema
from apps.base.schema.constants import schema_constants

from .methods import DiscountModelMethodsSchema

class DiscountModelSchema(ModelSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children.update({
      schema_constants.METHODS: DiscountModelMethodsSchema(Model, mode=mode),
    })