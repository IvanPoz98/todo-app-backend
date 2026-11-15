from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.users import UserRepository
from app.schemas.users import UserCreateSchema, UserLoginSchema, TokenSchema


class EmailAlreadyExistsError(Exception):
    ...


class InvalidCredentialsError(Exception):
    ...


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = UserRepository(session)

    async def register(self, payload: UserCreateSchema) -> TokenSchema:
        existing = await self.repository.get_by_email(payload.email)
        if existing is not None:
            raise EmailAlreadyExistsError()

        user = await self.repository.create(
            email=payload.email,
            hashed_password=hash_password(payload.password)
        )
        await self.session.commit()

        token = create_access_token(subject=user.id)
        return TokenSchema(access_token=token)

    async def login(self, payload: UserLoginSchema) -> TokenSchema:
        user = await self.repository.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise InvalidCredentialsError()

        token = create_access_token(subject=user.id)
        return TokenSchema(access_token=token)