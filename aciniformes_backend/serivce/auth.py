from .base import AuthServiceInterface
import sqlalchemy as sa
import aciniformes_backend.serivce.exceptions as exc
from aciniformes_backend.settings import get_settings
import aciniformes_backend.models as db_models

settings = get_settings()


class PgAuthService(AuthServiceInterface):
    async def registrate_user(self, username, password) -> db_models.Auth | None:
        q = sa.insert(db_models.Auth).values(username=username, password=password).returning(db_models.Auth)
        if await self.get_user(username):
            raise exc.AlreadyRegistered(username)
        else:
            return self.session.scalar(q)

    async def authenticate_user(self, username, password) -> db_models.Auth | None:
        db_user = await self.get_user(username)
        if not db_user:
            raise exc.NotRegistered(username)
        if not await self._validate_password(db_user.password, password):
            raise exc.WrongPassword()
        return db_user

    async def get_user(self, username) -> db_models.Auth | None:
        return self.session.scalar(sa.select(db_models.Auth).where(db_models.Auth.username == username))

    @staticmethod
    async def _validate_password(db_password, inp_password):
        return settings.PWD_CONTEXT.verify(inp_password, db_password)
