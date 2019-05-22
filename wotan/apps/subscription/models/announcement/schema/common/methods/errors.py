
from util.api import Error

class AnnouncementGetTakesNoArgumentsError(Error):
  code = 'a02100aef7ee4082b8b7dc7155992d23'
  name = 'announcement_get_takes_no_arguments'
  description = 'Announcement get takes no arguments'

class get_errors:
  ANNOUNCEMENT_GET_TAKES_NO_ARGUMENTS = AnnouncementGetTakesNoArgumentsError
