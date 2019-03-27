
from util.api import Error

class DurationNotIncludedError(Error):
  code = '987'
  name = 'duration_not_included'
  description = 'The subscription duration is not included'

class create_errors:
  DURATION_NOT_INCLUDED = DurationNotIncludedError

class SubscriptionIdNotIncludedError(Error):
  code = '989'
  name = 'subscription_id_not_included'
  description = 'Subscription ID must be included'

class SubscriptionDoesNotExistError(Error):
  code = '988'
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
