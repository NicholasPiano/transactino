
from util.api import Error

class AnnouncementGetTakesNoArgumentsError(Error):
  code = '725213'
  name = 'announcement_get_takes_no_arguments'
  description = 'Announcement get takes no arguments'

class get_errors:
  ANNOUNCEMENT_GET_TAKES_NO_ARGUMENTS = AnnouncementGetTakesNoArgumentsError
