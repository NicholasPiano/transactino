
from util.api import Error

class ChallengeIDNotIncludedError(Error):
  code = '749072d97e7a4d7c82b840e106f85255'
  name = 'challenge_id_not_included'
  description = 'The challenge ID is not included'

class ChallengeDoesNotExistError(Error):
  code = 'b67071706ef04eeeb85af1f1c77798e9'
  name = 'challenge_does_not_exist'
  description = 'The challenge does not exist'
  description_with_arguments = 'The challenge with ID [{}] does not exist'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class ClosedChallengeHasBeenUsedError(Error):
  code = 'ef4bb57cee2647259251ef8f923f7b5b'
  name = 'closed_challenge_has_been_used'
  description = 'Closed challenge has been used'
  description_with_arguments = 'The challenge with ID [{}] has been used'

  def __init__(self, id=None):
    self.description = (
      self.description_with_arguments.format(id)
      if id is not None
      else self.description
    )

class ContentNotIncludedError(Error):
  code = '994ca615ff8745f3a1a3e8dc6cd2b60c'
  name = 'content_not_included'
  description = 'Content not included'

class respond_errors:
  CHALLENGE_ID_NOT_INCLUDED = ChallengeIDNotIncludedError
  CHALLENGE_DOES_NOT_EXIST = ChallengeDoesNotExistError
  CLOSED_CHALLENGE_HAS_BEEN_USED = ClosedChallengeHasBeenUsedError
  CONTENT_NOT_INCLUDED = ContentNotIncludedError

class get_errors:
  CHALLENGE_DOES_NOT_EXIST = ChallengeDoesNotExistError

class delete_errors:
  CHALLENGE_ID_NOT_INCLUDED = ChallengeIDNotIncludedError
  CHALLENGE_DOES_NOT_EXIST = ChallengeDoesNotExistError
