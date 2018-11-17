
from util.merge import merge

from .constants import constants

class Response():
  def __init__(self, parent_schema):
    self.parent_schema = parent_schema
    self.description = parent_schema.description
    self.types = parent_schema.types
    self.client_schema = parent_schema.client
    self.active_type = None
    self.errors = {}
    self.is_empty = False
    self.value = None
    self.rendered = None
    self.has_child_errors = False

  def should_render(self):
    return True

  def has_errors(self):
    return bool(self.errors) or self.has_child_errors

  def add_error(self, error):
    self.errors.update({
      error.code: error,
    })

  def add_value(self, value):
    self.value = value

  def render(self, top=True):
    if self.is_empty:
      self.render_empty(top=top)
      return self.rendered

    if self.errors:
      self.render_errors()
      return self.rendered

    self.render_value()
    return self.rendered

  def render_empty(self, top=False):
    self.rendered = {
      constants.DESCRIPTION: self.description,
      constants.TYPES: {
        type.code: type.render()
        for type in self.types
      },
      constants.ERRORS: [
        error.code
        for error in self.parent_schema.available_errors
      ],
    }

    type_errors = []
    for type in self.types:
      if type.schema is not None:
        type_errors.extend(
          list(type.schema.available_errors)
          + list(type.schema.respond().errors.values())
        )

    self.errors.update({
      error.code: error
      for error in type_errors
    })

    if self.client_schema is not None:
      self.rendered.update({
        constants.CLIENT: self.client_schema.respond().render(top=False),
      })

    return self.rendered

  def render_errors(self):
    self.rendered = {
      constants.ERRORS: {
        error_code: error.render()
        for error_code, error in self.errors.items()
      },
    }

    return self.rendered

  def render_value(self):
    self.rendered = self.value
    return self.rendered

class StructureResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.children = {}

  def should_render(self):
    return bool(self.children) or self.has_errors()

  def add_child(self, child_key, child_response):
    self.children.update({child_key: child_response})
    if child_response.has_errors():
      self.has_child_errors = True

  def has_child(self, child_key):
    return child_key in self.children

  def get_child(self, child_key):
    return self.children.get(child_key)

  def force_get_child(self, child_key):
    if child_key not in self.children and child_key in self.parent_schema.children:
      self.add_child(child_key, self.parent_schema.children.get(child_key).get_response())

    return self.get_child(child_key)

  def render_empty(self, top=False):
    super().render_empty(top=top)

    if self.children:
      children = {}
      for child_key, child_response in self.children.items():
        children.update({
          child_key: child_response.render(top=False),
        })
        self.errors.update({
          error.code: error
          for error in (
            list(child_response.parent_schema.available_errors)
            + list(child_response.errors.values())
          )
        })

      self.rendered.update({
        constants.CHILDREN: children,
      })

      if top:
        self.rendered.update({
          constants.ERRORS: {
            error.code: error.render()
            for error in (
              list(self.parent_schema.available_errors)
              + list(self.errors.values())
            )
          },
        })

  def render_value(self):
    self.rendered = {
      child_key: child_response.render()
      for child_key, child_response in self.children.items()
      if child_response.should_render()
    }

class ArrayResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.template_schema = parent_schema.template
    self.children = []

  def should_render(self):
    return bool(self.children) or self.has_errors()

  def add_child(self, child_response):
    self.children.append(child_response)
    if child_response.has_errors():
      self.has_child_errors = True

  def render_empty(self, top=False):
    super().render_empty()
    template_response = self.template_schema.respond()
    self.rendered.update({
      constants.TEMPLATE: template_response.render(top=False),
    })
    self.errors.update({
      error.code: error
      for error in (
        list(self.template_schema.available_errors)
        + list(template_response.errors.values())
      )
    })

  def render_value(self):
    self.rendered = [
      child_response.render()
      for child_response in self.children
    ]

class IndexedResponse(Response):
  def __init__(self, parent_schema):
    super().__init__(parent_schema)
    self.template_schema = parent_schema.template
    self.children = {}

  def should_render(self):
    return bool(self.children) or self.has_errors()

  def add_child(self, child_index, child_response):
    self.children.update({
      child_index: child_response,
    })
    if child_response.has_errors():
      self.has_child_errors = True

  def render_empty(self, top=False):
    super().render_empty()
    template_response = self.template_schema.respond()
    self.rendered.update({
      constants.TEMPLATE: template_response.render(top=False),
    })
    self.errors.update({
      error.code: error
      for error in (
        list(self.template_schema.available_errors)
        + list(template_response.errors.values())
      )
    })

    if top:
      self.rendered.update({
        constants.ERRORS: {
          error.code: error.render()
          for error in (
            list(self.parent_schema.available_errors)
            + list(self.errors.values())
          )
        },
      })

  def render_value(self):
    self.rendered = {
      child_index: child_response.render()
      for child_index, child_response in self.children.items()
    }
