from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware

from src import healthcheck
from src.users.router import router as user_router
from src.orders_items.router import router as orders_items_router
from src.customer_orders.router import router as customer_orders_router

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
    app.include_router(router = user_router)
    app.include_router(router=customer_orders_router)
    app.include_router(router=orders_items_router)

    # Main router.py for the API.

    return app
