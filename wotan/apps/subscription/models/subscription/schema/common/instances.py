
from apps.base.schema.constants import schema_constants
from apps.base.schema.instances import (
  InstancesClosedSchema,
  InstancesSchema,
  InstanceSchema,
)
from apps.base.schema.instances.attributes import InstanceAttributeSchema

class SubscriptionInstanceSchema(InstanceSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.children = {
      schema_constants.ATTRIBUTES: InstanceAttributeSchema(Model, mode=mode),
    }

  def response_from_model_instance(self, instance, attributes=None, relationships=None):
    return self.respond(
      payload=self.model.objects.serialize(
        instance,
        attributes=attributes,
        mode=self.mode,
      ),
    )

class SubscriptionInstancesSchema(InstancesSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.template = SubscriptionInstanceSchema(Model, mode=mode)

class SubscriptionInstancesClosedSchema(InstancesClosedSchema):
  def __init__(self, Model, mode=None, **kwargs):
    super().__init__(Model, mode=mode, **kwargs)
    self.client = SubscriptionInstancesSchema(Model, mode=mode)
