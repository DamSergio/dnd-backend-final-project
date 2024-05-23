from pydantic import BaseModel


class CreateCampaign(BaseModel):
    name: str
    description: str
    notes: str = ""
