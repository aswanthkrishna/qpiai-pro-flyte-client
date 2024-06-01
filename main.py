from fastapi import FastAPI
from app.routes import executions, tasks
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

app = FastAPI()

# Include the router
app.include_router(executions.router)
app.include_router(tasks.router)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)