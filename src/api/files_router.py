import os

import aiofiles
from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import FileResponse

from api.auth_router import get_current_user
from db.db import add_file, get_all_user_file, get_file
from models.users_model import Users

router_files = APIRouter()


@router_files.get("/")
async def get_files(
    request: Request, current_user: Users = Depends(get_current_user)
):
    files = await get_all_user_file(current_user)
    return files


@router_files.get("/download")
async def download_file(
    s_path: str, current_user: Users = Depends(get_current_user)
):
    file = await get_file(s_path)
    if not file:
        return "File not found"
    print(file)
    media_type = file.path.split(".")[-1]
    return FileResponse(
        path=file.path, filename=file.name, media_type=media_type
    )


@router_files.post("/upload")
async def upload_file(
    file: UploadFile,
    path: str,
    current_user: Users = Depends(get_current_user),
):
    full_path = os.path.join("data", path)
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path))
    if path.endswith("/"):
        full_path = os.path.join(full_path, file.filename)
    file_size = 0
    async with aiofiles.open(full_path, "wb") as out_file:
        content = await file.read()
        file_size = len(content)
        await out_file.write(content)
    await add_file(file.filename, full_path, file_size, current_user)
    file_info = await get_all_user_file(current_user)
    if file_info:
        last_file_name = file_info[-1].name
        return last_file_name
    else:
        return "No files found"
