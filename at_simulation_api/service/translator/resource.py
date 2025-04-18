import os
from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from at_simulation_api.repository.editor.resource.models.models import (
    ResourceAttributeDB,
    ResourceDB,
    ResourceTypeDB,
)

module_dir = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(module_dir, "templates")
TEMPLATE_NAME = "resource.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_resources(
    resources: List[ResourceDB], resource_types: List[ResourceTypeDB]
) -> List[str]:
    def find_resource_type(resource_type_id: int) -> ResourceTypeDB:
        return next((rt for rt in resource_types if rt.id == resource_type_id), None)

    rendered_templates = []

    for resource in resources:
        resource_type = find_resource_type(resource.resource_type_id)

        rendered_template = template.render(to_resource_tr(resource, resource_type))
        rendered_templates.append(rendered_template)

    return rendered_templates


def to_resource_tr(resource: ResourceDB, resource_type: ResourceTypeDB) -> dict:
    def _process_value(ra: ResourceAttributeDB, attr_name: str):
        if ra is None:
            return None
        if isinstance(ra.value, bool):
            return str(ra.value).lower()
        if isinstance(ra.value, str):
            _enum_prefix = f"{resource_type.name.upper()}{attr_name.upper()}"
            return f"{_enum_prefix} + {ra.value.upper()}"
        return ra.value

    attrs = [
        {
            "name": attr.name,
            "value": _process_value(
                next((ra for ra in resource.attributes if ra.rta_id == attr.id), None),
                attr.name,
            ),
        }
        for attr in resource_type.attributes
    ]

    return {
        "resource_name": resource.name,
        "resource_type_name": resource_type.name,
        "to_be_traced": str(resource.to_be_traced).lower(),
        "attributes": attrs,
    }
