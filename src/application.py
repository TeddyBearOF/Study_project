from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware

from src import healthcheck
from src.users_user_profiles import routers as users_router
from src.resumes_vacancies import routers as resumes_vacancies_router
from src.employers_reviews import routers as employers_reviews_router

def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(router=healthcheck.router)
    app.include_router(router=users_router.router)
    app.include_router(router=resumes_vacancies_router.router)
    app.include_router(router=employers_reviews_router.router)

    # Main routers.py for the API.

    return app
