
from ..account.constants import account_fields

class challenge_constants:
  ACCOUNT_RELATED_MODEL = 'subscription.Account'
  ACCOUNT_RELATED_NAME = 'challenges'

class challenge_fields:
  ACCOUNT = 'account'
  ORIGIN = 'origin'
  CONTENT = 'content'
  ENCRYPTED_CONTENT = 'encrypted_content'
  IS_OPEN = 'is_open'
  HAS_BEEN_USED = 'has_been_used'

account_fields.CHALLENGES = challenge_constants.ACCOUNT_RELATED_NAME

class challenge_method_constants:
  OPEN_CHALLENGE_ID = 'open_challenge_id'
  VERIFICATION_COMPLETE = 'verification_complete'
