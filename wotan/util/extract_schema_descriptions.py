
def extract_schema_descriptions(rendered_schema, null=True):
  paths = []
  if null and '_children' not in rendered_schema:
    return paths

  children = (
    rendered_schema.get('_children')
    if null
    else (
      rendered_schema
      if isinstance(rendered_schema, dict)
      else {}
    )
  )

  for key, value in children.items():
    child_paths = extract_schema_descriptions(value, null=null)
    if child_paths:
      paths.extend([
        [key] + path
        for path
        in child_paths
      ])
    else:
      paths.append([key])

  return paths
