"""
Определение объекта приложения
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from PIL import UnidentifiedImageError
from app import api

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

app.include_router(api.router)


@app.get("/")
def home() -> dict[str, str]:
    return {"app status": "OK"}


@app.exception_handler(FileNotFoundError)
def file_not_found_handler(request: Request,
                           exc: FileNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"detail": exc.__str__(),
                                  "method": request.method,
                                  "exception": str(type(exc))})
    )


@app.exception_handler(UnidentifiedImageError)
def pil_image_open_error(request: Request,
                         exc: UnidentifiedImageError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.__str__(),
                                  "method": request.method,
                                  "exception": str(type(exc))})
    )


@app.exception_handler(ValueError)
def bad_file_error(request: Request,
                   exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.__str__(),
                                  "method": request.method,
                                  "exception": str(type(exc))})
    )
