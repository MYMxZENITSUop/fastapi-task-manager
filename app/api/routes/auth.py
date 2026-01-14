from fastapi import APIRouter, Depends, HTTPException, Header
from firebase_admin import auth as firebase_auth
from app.core.firebase import firebase_admin
from app.core.security import create_access_token

router = APIRouter()

@router.post("/auth/google")
def google_login(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        decoded_token = firebase_auth.verify_id_token(token)

        email = decoded_token.get("email")
        name = decoded_token.get("name")
        uid = decoded_token.get("uid")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found")

        # TODO: create or fetch user from DB here

        access_token = create_access_token({"sub": email})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": email,
                "name": name
            }
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")