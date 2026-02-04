from pydantic import BaseModel, HttpUrl

class FetchRequest(BaseModel):
    url: HttpUrl

class FetchResponse(BaseModel):
    url: str
    status: int
    content: str
