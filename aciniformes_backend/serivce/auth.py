from .base import AuthServiceInterface

import aciniformes_backend.serivce.exceptions as exc
from aciniformes_backend.settings import get_settings
from .. import models as db_models

settings = get_settings()


class PgAuthService(AuthServiceInterface):
    async def get_all(self) -> list[db_models.BaseModel]:
        pass

    async def create(self, item: dict) -> int:
        pass

    async def registrate_user(self, username, password):
        db_user = self.repository.get_user_by_username(username)
        if db_user:
            raise exc.AlreadyRegistered(username)
        else:
            self.repository.add(Auth(username=username, password=password))

    async def authenticate_user(self, username, password) -> db_models.Auth | None:
        db_user: Auth | None = self.repository.get_user_by_username(username)
        if not db_user:
            raise exc.NotRegistered(username)
        if not await self._validate_password(db_user.password, password):
            raise exc.WrongPassword()
        return db_user

    async def get_user(self, username):
        return self.repository.get_user_by_username(username)

    @staticmethod
    async def _validate_password(db_password, inp_password):
        return settings.PWD_CONTEXT.verify(inp_password, db_password)
