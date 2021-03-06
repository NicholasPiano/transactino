
from util.api import Error

class DurationNotIncludedError(Error):
  code = 'db5048287e854d2ab0a283d74782d18b'
  name = 'duration_not_included'
  description = 'The subscription duration is not included'

class create_errors:
  DURATION_NOT_INCLUDED = DurationNotIncludedError

class SubscriptionIdNotIncludedError(Error):
  code = 'cf0c47ab721244b690e481a5ba835ef0'
  name = 'subscription_id_not_included'
  description = 'Subscription ID must be included'

class SubscriptionDoesNotExistError(Error):
  code = 'cc80ae53afd24407aad55b52604ab2e9'
  name = 'subscription_does_not_exist'
  description = 'The subscription does not exist'
  description_with_arguments = 'The subscription with id [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class activate_errors:
  SUBSCRIPTION_DOES_NOT_EXIST = SubscriptionDoesNotExistError
  SUBSCRIPTION_ID_NOT_INCLUDED = SubscriptionIdNotIncludedError

class get_errors:
  SUBSCRIPTION_DOES_NOT_EXIST = SubscriptionDoesNotExistError
