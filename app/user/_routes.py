from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.auth.providers import user_provider
from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.templating.provider import templating_provider
from app.user.dto.user import UserDTO, GetUserDTO
from app.user.entities import UserEntity
from app.user.value_objects import UserID

router = APIRouter()


@router.get("/user/{user_id}", name="get-user-by-id")
async def get_user_by_id(
	user_id: str,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> UserDTO:
	return await ioc.user_service().get_user(
		GetUserDTO(
			user_id=UserID.from_uuid(UUID(user_id)),
		)
	)


@router.get("/account", name="get-account", response_class=HTMLResponse)
async def get_account(
	request: Request,
	user: Annotated[UserEntity, Depends(user_provider)],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
	return templates.TemplateResponse("users/account.html", {'request': request, 'user': user})
