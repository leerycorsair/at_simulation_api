from fastapi import Depends
from sqlalchemy.orm import Session

from at_simulation_api.providers.visio import get_visio_service
from at_simulation_api.repository.editor.template.repository import TemplateRepository
from at_simulation_api.service.editor.template.service import TemplateService
from at_simulation_api.storage.postgres.storage import get_db


def get_template_repository(session: Session = Depends(get_db)) -> TemplateRepository:
    return TemplateRepository(session)


def get_template_service(
    template_rep=Depends(get_template_repository),
    visio_service=Depends(get_visio_service),
) -> TemplateService:
    return TemplateService(template_rep, visio_service)
