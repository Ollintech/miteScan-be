from fastapi import APIRouter, UploadFile, File
import shutil
from app.ai.predict import predict_image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_image(path)

    return result