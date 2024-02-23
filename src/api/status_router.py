from fastapi import APIRouter, Request

from db.db import ping_database

router_get_ping = APIRouter()


@router_get_ping.get("/")
async def get_ping(request: Request):
    """
    Returns data about the response time of the linked servers
    """
    response = {"db": await ping_database()}
    print(response)
    return response
