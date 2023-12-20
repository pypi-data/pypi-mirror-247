import asyncio
import uuid
from abc import abstractmethod
from logging import Logger
from typing import Type

from rosemary.core.custom_semaphore import CustomSemaphore
from rosemary.core.logger import get_logger
from rosemary.db.db import DBConnector
from rosemary.db.models import RosemaryWorkerModel
from rosemary.task.task_interface import InterfaceRosemaryTask


class RosemaryWorkerInterface:
    def __init__(
            self,
            db_host: str,
            db_port: int | str,
            db_user: str,
            db_password: str,
            db_name_db: str,
            db_schema: str,
            tasks: dict[str, Type[InterfaceRosemaryTask]],
            shutdown_event,
            logger: Logger | None = None,
            max_task_semaphore: int = 30,
    ):
        self.uuid = uuid.uuid4()
        self.worker_db: RosemaryWorkerModel | None = None
        self.db_connector = None
        self.logger: Logger | None = get_logger(str(self.uuid)) or logger

        self.db_connector = DBConnector(
            db_host, db_name_db, db_user, db_password, db_port, db_schema
        )
        self._max_task_semaphore = max_task_semaphore
        self._registered_tasks = tasks
        self.__shutdown_event = shutdown_event

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._looping())
        loop.close()

    @abstractmethod
    async def _looping(self):
        ...

    async def __cycle_looping(self):
        async with self.db_connector.get_session() as session:
            while not self.__shutdown_event.is_set():

            await self.register_in_db(session)
            self.logger.info(f'Start looping by worker {self.uuid}')
            semaphore = CustomSemaphore(self._max_task_semaphore)
            while not self.__shutdown_event.is_set():
                await self.__ping(session)
                if semaphore.tasks_remaining() > 0:
                    ids_tasks = await self._get_new_tasks(session, semaphore.tasks_remaining())
                    for id_task in ids_tasks:
                        await semaphore.acquire()
                        asyncio.create_task(self._run_task(id_task, semaphore))
                else:
                    await asyncio.sleep(2)
                await asyncio.sleep(1)

                step += 1

                if step >= 60 * 1:
                    step = 0
                    await self.__check_stuck_tasks(session)
                    await self.__check_stuck_tasks_by_other_workers(session)
                    await self._check_deaths_workers(session)

            self.logger.info(f'Rosemary worker {self.uuid} is shutdowning warm...')
            while semaphore.tasks_remaining() != self._max_task_semaphore:
                await asyncio.sleep(1)
            await self.__suicide(session)
            self.logger.info(f'Rosemary worker {self.uuid} is shutdown warm!')