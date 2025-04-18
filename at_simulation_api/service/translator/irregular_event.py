import os
from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from at_simulation_api.repository.editor.resource.models.models import ResourceTypeDB
from at_simulation_api.repository.editor.template.models.models import IrregularEventDB
from at_simulation_api.service.translator.utils import preprocess_template_code

module_dir = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(module_dir, "templates")
TEMPLATE_NAME = "irregular_event.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_irregular_events(
    irregular_events: List[IrregularEventDB], resource_types: List[ResourceTypeDB]
) -> List[str]:
    def find_resource_type(resource_type_id: int) -> ResourceTypeDB:
        return next((rt for rt in resource_types if rt.id == resource_type_id), None)

    rendered_templates = []

    for irregular_event in irregular_events:
        rel_resources_info = {}
        for rel_resource in irregular_event.meta.rel_resources:
            resource_type = find_resource_type(rel_resource.resource_type_id)
            if resource_type:
                rel_resources_info[rel_resource.id] = resource_type

        rendered_template = template.render(
            to_irregular_event_tr(irregular_event, rel_resources_info)
        )
        rendered_templates.append(rendered_template)

    return rendered_templates


def to_irregular_event_tr(
    irregular_event: IrregularEventDB, rel_resources_info: dict
) -> dict:
    params = [
        {"name": rel_resource.name, "type": rel_resources_info[rel_resource.id].name}
        for rel_resource in irregular_event.meta.rel_resources
        if rel_resource.id in rel_resources_info
    ]

    param_names = [param["name"] for param in params]
    new_body = preprocess_template_code(irregular_event.body.body, param_names)

    return {
        "template_name": irregular_event.meta.name,
        "params": params,
        "generator_type": irregular_event.generator.type,
        "generator_value": irregular_event.generator.value,
        "generator_dispersion": irregular_event.generator.dispersion,
        "body": new_body,
    }
