
from util.api import Error

class OpenChallengeExistsWithOriginError(Error):
  code = '629'
  name = 'open_challenge_exists_with_origin'
  description = 'Open challenge exists with the given origin'
  description_with_arguments = 'Open challenge {} exists with origin {}'

  def __init__(self, id=None, origin=None):
    self.description = (
      self.description_with_arguments.format(id, origin)
      if (
        id is not None
        and origin is not None
      )
      else self.description
    )

class with_challenge_errors:
  OPEN_CHALLENGE_EXISTS_WITH_ORIGIN = OpenChallengeExistsWithOriginError
