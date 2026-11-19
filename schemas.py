from pydantic import BaseModel, Field, ConfigDict


class DocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    content: str = Field(min_length=1)
    priority: int = Field(default=1, ge=1, le=5)
    description: str | None = Field(default=None, max_length=250)


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    priority: int
    description: str | None = None
    ai_summary: str | None = None


class AIAnalysisResponse(BaseModel):
    summary: str
    key_points: list[str]
    category: str
    suggested_priority: int


class AgentAskRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class AgentAskResponse(BaseModel):
    answer: str
