from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel, Field


app = FastAPI()


class SigninRequest(BaseModel):
    email: str
    password: str
    name: str = Field(default=None)


class SigninResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str


class GetPostsResponse(BaseModel):
    id: int
    title: str
    detail: str


class ErrorResponse(BaseModel):
    message: str


TEST_REQUESTER = {
    "email": "example@example.co.jp",
    "password": "1234",
}

TEST_ACCESS_TOKEN = "access_token"


@app.post("/signin")
async def signin(body: SigninRequest) -> SigninResponse | ErrorResponse:
    if body.email != TEST_REQUESTER["email"] or body.password != TEST_REQUESTER["password"]:
        return {
            "message": "Invalid email or password",
        }
    return {
        "access_token": TEST_ACCESS_TOKEN,
        "refresh_token": "refresh_token",
        "id_token": "id_token",
    }


@app.get("/posts")
async def list_posts(authorization: Annotated[str | None, Header()] = None) -> list[GetPostsResponse] | ErrorResponse:
    if authorization != TEST_ACCESS_TOKEN:
        return {
            "message": "Unauthorized",
        }
    return [
        {
            "id": 1,
            "title": "Hello1",
            "detail": "World1",
        },
        {
            "id": 2,
            "title": "Hello2",
            "detail": "World2",
        },
    ]
