from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from app.core.redis_client import redis_client
from app.routers import routes
from app.core.config import settings

app = FastAPI(
    title="HireKarle API",
    description="AI-Powered Job Matcher",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router, prefix="/api")

@app.get("/", summary="Health check endpoint", description="Check API health and Redis connectivity.")
async def health_check():
    """
    Simple health check endpoint.

    Returns:
    - {"status": "ok"} if Redis is connected.
    - {"status": "Redis not working."} if Redis is unavailable.
    """
    ping = await redis_client.check_redis_connection()
    if not ping:
        return {"status": "Redis not working."}
    return {"status": "ok"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    """
    Return the Scalar API reference.

    This endpoint is hidden from OpenAPI/Swagger docs (`include_in_schema=False`).
    """
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar"
    )
