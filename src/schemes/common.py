from pydantic import BaseModel, Field, ConfigDict

class IDSchema(BaseModel):
    id: int = Field(
        ...,
        ge=0,
        description="Уникальный номер.",
        examples=[0, 10, ]
    )

    model_config = ConfigDict(from_attributes=True)
