
from contextlib import asynccontextmanager
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from config import settings 
from api.routes import auth, todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print(f"Starting {settings.APP_NAME}")
    yield

    #Shutdown logic
    print("Shutting down")

app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",         # Swagger UI
        redoc_url="/redoc",     # Redoc
        )

# CORS - adjust origins for production
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Lock this down in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],

        )


app.include_router(auth.router, prefix="/api")
app.include_router(todos.router, prefix="/api")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}



