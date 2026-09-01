from fastapi import FastAPI

from app.api.router import api_router


app = FastAPI(
    title="StudyPilot API",
    version="0.1.0",
    description="AI-Powered Study Planner API",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)