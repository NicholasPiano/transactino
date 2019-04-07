
from util.api import Schema

class SocketSchema(Schema):
  def __init__(self):
    super().__init__(
      description=(
        'Run this method to obtain the information'
        ' about the active socket if it exists.'
      ),
    )
