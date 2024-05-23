from pydantic import BaseModel


class Invitation(BaseModel):
    campaign_id: str
    campaign_name: str
    dungeon_master: str
