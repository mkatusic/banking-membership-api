from fastapi import FastAPI

from app.api.customers import router as customers_router
from app.api.plans import router as plans_router
from app.api.subscriptions import router as subscriptions_router


app = FastAPI(
    title="Banking Membership API",
    description="REST API for managing banking customers, membership plans, and subscriptions.",
    version="1.0.0",
)


# Register routers
app.include_router(customers_router)
app.include_router(plans_router)
app.include_router(subscriptions_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}