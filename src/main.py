import uvicorn
from fastapi import FastAPI

from api_v0 import router as router_v0


app = FastAPI(
    title="ScoreSpin"
)

app.include_router(router=router_v0, prefix="/api/v0")


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
