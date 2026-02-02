from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from server.api.routes import router as api_router
import os

app = FastAPI(title="AI Employee Design Generator")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routes
app.include_router(api_router, prefix="/api")

# Serve Static Files (Frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
