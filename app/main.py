from fastapi import FastAPI
from typing import Union
import uvicorn
from .routers import generate_router

app = FastAPI(title="Text-to-Speech API")

# Register API routes
app.include_router(generate_router.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)