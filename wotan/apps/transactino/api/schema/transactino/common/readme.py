
from util.api import Schema

class ReadmeSchema(Schema):
  def __init__(self):
    super().__init__(
      description='Run this method to obtain the README for the system',
    )
