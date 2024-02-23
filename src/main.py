import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer

from api.auth_router import router_auth
from api.files_router import router_files
from api.status_router import router_get_ping
from core import config
from db.db import create_model


app = FastAPI(
    title=config.app_settings.app_title,
    default_response_class=ORJSONResponse,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(router_get_ping, prefix="/ping")
app.include_router(router_auth, prefix="")
app.include_router(router_files, prefix="/files")


@app.on_event("startup")
async def startup_event():
    await create_model()


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=config.app_settings.redis_host,
        port=config.app_settings.redis_port,
        reload=True,
        log_config=config.LOGGING,
    )
