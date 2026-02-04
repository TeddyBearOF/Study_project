from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware

from src import healthcheck
from src.users_user_profiles import routers as users_router
from src.resumes_vacancies import routers as resumes_vacancies_router
from src.employers_reviews import routers as employers_reviews_router

from src.exceptions import AppException


def get_app() -> FastAPI:
    app = FastAPI(
        title="Энвелоуп",
        description="Раскрывается тема энвелоупов",
        version="0.1.0",
        docs_url='/api/v1/docs',
        openapi_url='/api/v1/openapi.json',
        contact={
            "name": "Rudik-Prudik",
            "email": "rudislamswmiass2004@gmail.com"
        },
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return UJSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "status_code": exc.status_code,
                "path": request.url.path,
                "details": exc.details,
            },
        )


    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return UJSONResponse(
            status_code=500,
            content={
                "error": "Внутренняя ошибка сервера",
                "status_code": 500,
                "path": request.url.path,
                "details": {
                    "type": type(exc).__name__,
                    "message": str(exc)
                }
            },
        )


    app.include_router(router=healthcheck.router, prefix="/api/v1")
    app.include_router(router=users_router.router, prefix="/api/v1")
    app.include_router(router=resumes_vacancies_router.router, prefix="/api/v1")
    app.include_router(router=employers_reviews_router.router, prefix="/api/v1")


    return app