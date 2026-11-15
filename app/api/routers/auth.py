from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_auth_service
from app.services.auth import AuthService, EmailAlreadyExistsError, InvalidCredentialsError
from app.schemas.users import TokenSchema
from app.schemas.users import UserCreateSchema, UserLoginSchema

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=TokenSchema)
async def user_register(payload: UserCreateSchema, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return await auth_service.register(payload)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The email is taken.')


@router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenSchema)
async def user_login(payload: UserLoginSchema, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return await auth_service.login(payload)
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid login or password')
    


