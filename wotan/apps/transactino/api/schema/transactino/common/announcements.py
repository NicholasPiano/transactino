
from util.api import (
  Schema, ClosedSchema,
  Response,
)

class AnnouncementsResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(
      parent_schema,
      value=(
        'There are active announcements. Please refer'
        ' to the Announcement model for more details.'
      ),
    )

class AnnouncementsClientSchema(Schema):
  def __init__(self):
    super().__init__(response=AnnouncementsResponse)

class AnnouncementsSchema(ClosedSchema):
  def __init__(self):
    super().__init__(
      description=(
        'This schema takes no input, but will display a message when'
        ' there are active announcements.'
      ),
      client=AnnouncementsClientSchema(),
    )
