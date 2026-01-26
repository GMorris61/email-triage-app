from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import email_routes

# Create the FastAPI application instance
app = FastAPI()

# Allow the frontend (running in the browser) to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you would restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the email routes (search, actions, etc.)
app.include_router(email_routes.router)

# Root endpoint for testing
@app.get("/")
def root():
    return {"message": "Email Triage Backend is running"}
