from pydantic import BaseModel, Field
from datetime import datetime


class GeneralResponseItem(BaseModel):
    date: datetime = Field(..., description="Date")
    logins: int = Field(..., description="Number of logins")
    logouts: int = Field(..., description="Number of logouts")
    actions: int = Field(..., description="Number of actions in user's blogs")


class GeneralResponse(BaseModel):
    data: list[GeneralResponseItem] = Field(..., description="General user data")


class CommentsResponseItem(BaseModel):
    login: str = Field(..., description="User's login")
    header: str = Field(..., description="Header of the post")
    author: str = Field(..., description="Author of the post")
    comments_num: int = Field(..., description="Number of comments")


class CommentsResponse(BaseModel):
    data: list[CommentsResponseItem] = Field(..., description="Comments data")