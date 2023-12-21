from typing import Any

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(alias="userIdHash")
    nickname: str
    profile_image_url: str = Field(alias="profileImageUrl")
    has_profile: bool = Field(alias="hasProfile")
    verified: bool = Field(alias="verifiedMark")
    logged_in: bool = Field(alias="loggedIn")
    penalties: list[Any]


class Channel(BaseModel):
    id: str = Field(alias="channelId")
    name: str = Field(alias="channelName")
    image_url: str = Field(alias="channelImageUrl")
    verified: bool = Field(alias="verifiedMark")
    type: str = Field(alias="channelType")
    description: str = Field(alias="channelDescription")
    follower_count: int = Field(alias="followerCount")
    live: bool = Field(alias="openLive")
