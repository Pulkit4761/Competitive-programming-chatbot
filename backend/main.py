import os
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class SolveRequest(BaseModel):
    problem: str = Field(..., description="The competitive programming problem statement or prompt.")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt to steer the model.")
    temperature: Optional[float] = Field(0.2, ge=0.0, le=2.0, description="Sampling temperature for generation.")
    max_tokens: Optional[int] = Field(512, ge=1, le=8192, description="Max new tokens to generate.")


class SolveResponse(BaseModel):
    output: str
    raw: Optional[dict] = None


COLAB_ENDPOINT = os.getenv("COLAB_ENDPOINT", "").strip()
COLAB_API_KEY = os.getenv("COLAB_API_KEY", "").strip()

app = FastAPI(title="Minor Project Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "colab_configured": bool(COLAB_ENDPOINT)}


@app.post("/solve", response_model=SolveResponse)
async def solve(req: SolveRequest) -> SolveResponse:
    if not COLAB_ENDPOINT:
        raise HTTPException(status_code=500, detail="COLAB_ENDPOINT not configured")

    payload = {
        "problem": req.problem,
        "system_prompt": req.system_prompt,
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
    }

    headers = {}
    if COLAB_API_KEY:
        headers["Authorization"] = f"Bearer {COLAB_API_KEY}"

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(COLAB_ENDPOINT, json=payload, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Error contacting Colab endpoint: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    try:
        data = resp.json()
    except ValueError:
        # If Colab returns plain text
        data = {"output": resp.text}

    # Normalize expected output field
    output_text = (
        data.get("output")
        or data.get("response")
        or data.get("answer")
        or data.get("text")
        or ""
    )

    if not isinstance(output_text, str):
        output_text = str(output_text)

    return SolveResponse(output=output_text, raw=data if isinstance(data, dict) else None)


# For local runs via: uvx uvicorn backend.main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)


