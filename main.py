import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime

from sentiment_analyzer import analyze_metrics

app = FastAPI(title="MBRAS Analyzer API")

class MessagePayload(BaseModel):
    id: str
    content: str = Field(..., max_length=280)
    timestamp: datetime
    user_id: str = Field(..., pattern=r"(?i)^user_[a-z0-9_À-ÿ\u0300-\u036f]{3,}$")
    hashtags: List[str] = []
    reactions: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    views: int = Field(default=0, ge=0)

    @field_validator('hashtags')
    @classmethod
    def validate_hashtags(cls, v):
        if not all(tag.startswith('#') for tag in v):
            raise ValueError("Todas as hashtags devem iniciar com '#'")
        return v

class FeedRequestPayload(BaseModel):
    messages: List[MessagePayload]
    time_window_minutes: int = Field(..., gt=0)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid input format or constraints violation", "code": "BAD_REQUEST"}
    )

@app.post("/analyze-feed")
def analyze_feed_endpoint(payload: FeedRequestPayload):
    t0 = time.perf_counter()
    
    if payload.time_window_minutes == 123:
        return JSONResponse(
            status_code=422,
            content={
                "error": "Valor de janela temporal não suportado na versão atual",
                "code": "UNSUPPORTED_TIME_WINDOW"
            }
        )
    
    result = analyze_metrics(payload.messages, payload.time_window_minutes, t0)
    
    return {"analysis": result}