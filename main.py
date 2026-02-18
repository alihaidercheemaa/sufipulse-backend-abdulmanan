from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import auth_router,user_router,admin_router,vocalist_router,kalam_router,studio_router,notification_router,public_router,writer_router,blogger_router,youtube_router,recording_requests_router,cms_router
import os

app = FastAPI(title="My App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://sufipulse.com", "http://127.0.0.1", "http://localhost:8000", "http://127.0.0.1:8000"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_credentials=True,
    allow_methods=["*"],            # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],            # Allow all headers
    expose_headers=["*"],           # Expose all headers
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads/blog-images", exist_ok=True)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(vocalist_router)
app.include_router(kalam_router)
app.include_router(studio_router)
app.include_router(notification_router)
app.include_router(public_router)
app.include_router(writer_router)
app.include_router(blogger_router)
app.include_router(youtube_router)
app.include_router(recording_requests_router)
app.include_router(cms_router)
