from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import UUID
from ..constants import Role
from pydantic import (
    BaseModel,
)

class Advertiser(BaseModel):
    class Config:
        # pydantic.config.BaseConfig
        frozen = True

    uuid: UUID
    id: int
    profile_id: int
    profile_uuid: UUID


    moderate: int
    premoderate_booking: bool

    created_at: datetime
    updated_at: datetime

    company_name: str = '' or None
    name: str = '' or None
    email: str = '' or None
    phone: str = '' or None
    whatsapp: str = '' or None
    telegram: str = '' or None
    note: str = '' or None
    weblink: str = '' or None
    instagram: str = '' or None

    balance_reach: int = None
    balance_reach_all: int = None
    description: str = '' or None
    group_payer_id: int = None


class Category(BaseModel):
    class Config:
        frozen = True

    id: int
    type: int
    name: str
    parent_id: int = None



class Instagram(BaseModel):
    class Config:
        frozen = True

    uuid: UUID
    id: int
    profile_id: int
    profile_uuid: UUID

    created_at: datetime
    updated_at: datetime

    is_private: bool = False
    is_verified: bool = False
    checked_at: datetime = None


    reach: int = None
    post_reach: int = None
    booking_limit: int = None
    picture: str = '' or None
    pkid: str = '' or None
    categories: list[Category] = []

    count_media: int = 0 or None
    full_name: str = '' or None
    external_url: str = '' or None


class TestM(BaseModel):
    class Config:
        frozen = True

    id: int
    categories: list[Category] = []

class AnonymousProfile(BaseModel):
    class Config:
        frozen = True

    uuid: UUID = None
    user_id: int = None
    role: int = Role.ANONYMOUS
    advertiser: Advertiser = None
    instagram: Instagram = None

    def __str__(self):
        return "AnonymousProfile"

class Profile(BaseModel):
    class Config:
        frozen = True

    uuid: UUID
    user_id: int

    role: int

    advertiser: Advertiser = None
    instagram: Instagram = None

    def __post_init__(self):
        if self.role == Role.ADVERTISER and not self.advertiser:
            raise ValueError('Advertiser must be set')
        elif self.role == Role.INSTAGRAM and not self.instagram:
            raise ValueError('Instagram must be set')


__all__ = [
    'Profile', 'AnonymousProfile',
]