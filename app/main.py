from fastapi import FastAPI
from api.routes import courses, instructors
import yaml
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response

app = FastAPI(
    title="Courses",
    version="1.0.0",
    docs_url="/docs/",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Custom OpenAPI Server URL
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://irisyen115.synology.me/course_api"},
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    openapi_dict = app.openapi()
    openapi_yaml = yaml.dump(openapi_dict, allow_unicode=True, sort_keys=False)
    return Response(content=openapi_yaml, media_type="application/x-yaml")

# Include routers
app.include_router(courses.router)
app.include_router(instructors.router)
