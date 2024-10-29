from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

# from app.telegram.telegram_auth import router_test
# from app.users.router import router_users
# from app.users.router import router_auth
from api.news.router import router as router_news
from api.graphs.router import router as router_graphs
from api.services.router import router as router_services
from api.crud.router import router as router_crud
from api.models.router import router as router_models

app = FastAPI(title='AntiSMI API')


@app.get("/", tags=["Home"])
async def root() -> dict:
    """
    Главная точка доступа API.
    Возвращает основную информацию о проекте.

    Main API access point.
    Returns basic project information.
    """
    return {
        "project": "antiSMI",
        "url": "http://news.anti-smi.com/",
        "github": "https://github.com/data-silence/antiSMI-Project",
        "author": "enjoy@data-silence.com"
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """
    Возвращает файл favicon.ico для клиента.

    Returns the favicon.ico file for the client.
    """
    return FileResponse(os.path.join(os.path.dirname(__file__), "favicon.ico"))


# Включение маршрутизаторов (routers) для различных частей приложения
# app.include_router(router_auth)
# app.include_router(router_users)
app.include_router(router_news)
app.include_router(router_models)
app.include_router(router_services)
app.include_router(router_graphs)
app.include_router(router_crud)
# app.include_router(router_test)
