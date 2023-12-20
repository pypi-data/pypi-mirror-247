import uuid
from logging import Logger

from rosemary.core.logger import get_logger
from rosemary.db.db import DBConnector


class RosemaryMainWorker:
    def __init__(
            self,
            db_host: str,
            db_port: int | str,
            db_user: str,
            db_password: str,
            db_name_db: str,
            db_schema: str,
            shutdown_event,
            logger: Logger | None = None,
    ):
        self.uuid = uuid.uuid4()
        self.db_connector = None
        self.logger: Logger | None = get_logger(str(f'main_worker -> {self.uuid}')) or logger

        self.db_connector = DBConnector(
            db_host, db_name_db, db_user, db_password, db_port, db_schema
        )
        self.__shutdown_event = shutdown_event
