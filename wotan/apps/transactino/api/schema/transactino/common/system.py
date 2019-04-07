
from util.api import StructureSchema

class SystemSchema(StructureSchema):
  def __init__(self):
    super().__init__(
      description=(
        'This schema takes no input, but will display a message'
        ' indicating that changes have been made to the system.'
      ),
    )
