import shutil

from fastapi import APIRouter, UploadFile
from fastapi_versioning import version

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"],
)


@router.post("/hotels")
@version(1)
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)