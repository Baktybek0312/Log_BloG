from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class PostList(UserBase):
    id: int
    title: str
    description: str
    owner_id: str

    class Config:
        orm_mode = True
