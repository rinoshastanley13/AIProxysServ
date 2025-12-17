from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import customer_router, user_router, demo_router, email_router, ollama_router
from app.configs import migration
import json

from app.auth.auth import auth_middleware_call

from app.configs.settings import settings

app = FastAPI(
    title = settings.server.api_name,
    description = settings.server.api_name, # or description if added to settings
    version = settings.server.version
)
app.include_router(user_router.userRoutes)
app.include_router(customer_router.customerRoutes)
app.include_router(demo_router.demoRoutes)
app.include_router(email_router.emailRoutes)
app.include_router(ollama_router.aiAgentsRoutes)

origins = settings.server.cors_urls
print("CORS Allowed Origins:", origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_origin_regex=r"https://.*\.ricagoapi\.com",
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    #allow_origins = ["*"]  # allow all origins
)

# @app.on_event("startup")
# async def startup_event():
    # app.state.api_keys = load_api_keys() 
    # Logic moved to settings.security.api_keys usage

# Middleware to check API key for all requests
app.middleware("http")(auth_middleware_call)

@app.get("/")
def root():
    return {"message": f"Welcome to {app.title} {app.version}. It's an {app.description}"}

# ----------------- Create Database and Tables if not exists --------------
migration.migrate()