from fastapi import FastAPI
from presentation.controllers.article_controller import router

app = FastAPI()
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}