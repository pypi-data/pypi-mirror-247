from datetime import datetime
from typing import Tuple
from uuid import UUID

from pydantic import BaseModel, ValidationError, field_validator
from pydantic_core.core_schema import FieldValidationInfo

class BaseUser(BaseModel):
    class Config:
        # from pydantic.config import BaseConfig
        frozen = True

    uuid: UUID
    id: int
    phone: str

    is_active: bool = False
    is_staff: bool = False
    email_active: bool = False
    phone_active: bool = False

    created_at: datetime
    updated_at: datetime
    last_login: datetime

    permissions: Tuple[str, ...] = tuple
    groups: Tuple[str, ...] = tuple

    position: int | None = None
    firstname: str | None = ''
    lastname: str | None = ''
    avatar: str | None = ''
    email: str | None = ''

    @field_validator('position')
    def validate_position(cls, val: int, info: FieldValidationInfo) -> int:
        #  в качестве работающего примера валидации
        if (val and val < 1) or val == 0:
            raise ValueError('position must be greater then 0')
        return val

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @property
    def TestP(self):
        return 'TestP'


class AdminUser(BaseUser):
    is_superuser: bool = False


__all__ = ['AdminUser', 'BaseUser']
