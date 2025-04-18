from typing import List

from at_queue.core.at_component import ATComponent
from at_queue.utils.decorators import authorized_method

from at_simulation_api.worker.dependencies import (
    IAuthClient,
    IModelService,
    IProcessorService,
    ITranslatorService,
)
from at_simulation_api.worker.models.conversions import (
    TranslatedFileDict,
    to_ProcessDict,
    to_ProcessDicts,
    to_TickDict,
    to_TranslatedFileDicts,
)
from at_simulation_api.worker.models.models import ProcessDict, TickDict


class ATSimulationWorker(ATComponent):
    def __init__(
        self,
        connection_parameters,
        auth_client: IAuthClient,
        model_service: IModelService,
        translator_service: ITranslatorService,
        processor_service: IProcessorService,
    ):
        super().__init__(connection_parameters=connection_parameters)
        self._auth_client = auth_client
        self._model_service = model_service
        self._translator_service = translator_service
        self._processor_service = processor_service

    @authorized_method
    async def get_translated_files(self, auth_token: str) -> List[TranslatedFileDict]:
        user_id = await self._auth_client.verify_token(auth_token)
        models = self._model_service.get_models(user_id)
        files = self._translator_service.get_translated_files(user_id)
        return to_TranslatedFileDicts(files, models)

    @authorized_method
    async def create_process(
        self, auth_token: str, file_id: str, process_name: str
    ) -> ProcessDict:
        user_id = await self._auth_client.verify_token(auth_token)
        return to_ProcessDict(
            self._processor_service.create_process(user_id, file_id, process_name)
        )

    @authorized_method
    async def run_tick(self, auth_token: str, process_id: str) -> TickDict:
        user_id = await self._auth_client.verify_token(auth_token)
        return to_TickDict(await self._processor_service.run_tick(user_id, process_id))

    @authorized_method
    async def kill_process(self, auth_token: str, process_id: str) -> ProcessDict:
        user_id = await self._auth_client.verify_token(auth_token)
        return to_ProcessDict(self._processor_service.kill_process(user_id, process_id))

    @authorized_method
    async def get_processes(self, auth_token: str) -> List[ProcessDict]:
        user_id = await self._auth_client.verify_token(auth_token)
        return to_ProcessDicts(self._processor_service.get_processes(user_id))
