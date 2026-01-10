from fastapi import FastAPI
from presentation.controllers.article_controller import router

app = FastAPI(title="Cache Research API")
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "cache-research"}