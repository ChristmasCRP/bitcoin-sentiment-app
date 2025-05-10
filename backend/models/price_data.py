from pydantic import BaseModel

class PredictionRequest(BaseModel):
    api_key: str
    prompt: str