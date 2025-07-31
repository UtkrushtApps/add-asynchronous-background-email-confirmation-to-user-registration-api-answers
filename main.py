from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict
import asyncio

app = FastAPI()

# Simulated User DB
users_db: Dict[str, dict] = {}

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

async def send_confirmation_email(email: str, full_name: str):
    # Simulate the process of sending an email asynchronously
    await asyncio.sleep(2)  # Simulate a delay for email sending
    print(f"Confirmation email sent to {email} for user {full_name}")

@app.post("/register")
async def register_user(
    user_req: UserRegisterRequest,
    background_tasks: BackgroundTasks
):
    # Check for existing user
    if user_req.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Simulate saving user to DB
    users_db[user_req.email] = {
        "email": user_req.email,
        "full_name": user_req.full_name,
        "password": user_req.password,  # Don't store plaintext in real apps.
    }
    
    # Schedule email confirmation in the background
    background_tasks.add_task(
        asyncio.create_task, send_confirmation_email(user_req.email, user_req.full_name)
    )

    return {"message": "User registered successfully. Please check your email for confirmation."}
