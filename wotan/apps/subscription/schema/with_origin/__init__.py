
from util.api.schema import Schema, Response

from .constants import with_origin_constants

class WithOriginResponse(Response):
  def __init__(self, parent_schema):
    self.origin = parent_schema.origin
    super().__init__(parent_schema)

  def render_empty(self, top=False):
    super().render_empty(top=top)

    self.rendered.update({
      with_origin_constants.ORIGIN: self.origin,
    })

    return self.rendered

class WithOrigin(Schema):
  def __init__(self, origin=None, response=WithOriginResponse, **kwargs):
    self.origin = origin
    super().__init__(
      **kwargs,
      response=response,
    )
