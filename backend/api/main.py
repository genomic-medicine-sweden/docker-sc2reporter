from db import *

from authentication import *
from models import *

from api.config import settings

from api.endpoints import (
    samples,
    users,
    login,
    variants,
    dashboard,
    phylogeny,
    consensus,
    depth,
    significant_variants,
)

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version="development",
    root_path=settings.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 500:
        return JSONResponse(
            status_code=500,
            content={
                "message": "You encountered an internal server error. Please contact the administrator."
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
def root():
    return {
        "message": "Hello and welcome to the SarsCov 2 API",
        "root_path": app.root_path,
    }


app.include_router(
    samples.router,
    prefix="/samples",
    tags=["Samples"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    consensus.router,
    prefix="/consensus",
    tags=["Consensus"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    depth.router,
    prefix="/depth",
    tags=["Depth"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    login.router,
    prefix="/login",
    tags=["Login"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
app.include_router(
    significant_variants.router,
    prefix="/significant_variants",
    tags=["Significant Variants"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    variants.router,
    prefix="/variants",
    tags=["Variants"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    phylogeny.router,
    prefix="/phylogeny",
    tags=["Phylogeny"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@app.on_event("startup")
async def startup_event():
    await startup_db()
