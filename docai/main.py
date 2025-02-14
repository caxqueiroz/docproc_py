from fastapi import FastAPI
from .api.router import router
from .config.settings import settings

app = FastAPI(title="Document AI API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
