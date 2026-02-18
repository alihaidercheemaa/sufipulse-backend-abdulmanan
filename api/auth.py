from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import psycopg2
from utils.hashing import hash_password,verify_password
from utils.jwt_handler import create_access_token, create_refresh_token,verify_token
from utils.otp import generate_otp, send_otp_email, get_otp_expiry
from utils.conv_to_json import user_to_dict
from utils.google_auth import google_login_or_signup
from sql.combinedQueries import Queries
from db.connection import DBConnection
from typing import Optional


router = APIRouter(prefix="/auth", tags=["Authentication"])


class GoogleAuthRequest(BaseModel):
    token: str
    role: Optional[str] = None  # Optional if user exists, required for signup

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
class ChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str

class SignUpRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str
    country: str
    city: str

class OTPVerifyRequest(BaseModel):
    email: str
    otp: str

class ResendOTPRequest(BaseModel):
    email: str
    
    
class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str
    
@router.post("/signup")
def signup(data: SignUpRequest):
    if data.role == "admin":
        raise HTTPException(status_code=403, detail="Cannot sign up as admin")

    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)

            existing_user = db.get_user_by_email(data.email)
            if existing_user:
                # Check if user is already verified
                if existing_user["is_registered"]:
                    raise HTTPException(status_code=400, detail="User already exists")
                else:
                    # User exists but not verified, allow to continue with verification
                    # Generate new OTP and update user
                    otp = generate_otp()
                    otp_expiry = get_otp_expiry()
                    
                    db.resend_otp(data.email, otp, otp_expiry)
                    
                    # Send new OTP email
                    try:
                        send_otp_email(data.email, otp)
                        return {"message": "User exists but not verified. New OTP sent to your email."}
                    except Exception as email_error:
                        print(f"Email sending failed: {email_error}")
                        return {
                            "message": "User exists but not verified. New OTP generated, but there was an issue sending the email. Please contact support.",
                            "user_exists_unverified": True
                        }

            # If user doesn't exist, create new user
            hashed = hash_password(data.password)
            otp = generate_otp()
            otp_expiry = get_otp_expiry()

            db.create_user_with_otp(
                email=data.email,
                name=data.name,
                password_hash=hashed,
                role=data.role,
                country=data.country,
                city=data.city,
                otp=otp,
                otp_expiry=otp_expiry
            )

            # Send OTP email, but handle errors gracefully
            try:
                send_otp_email(data.email, otp)
                return {"message": "User created. OTP sent to your email."}
            except Exception as email_error:
                print(f"Email sending failed, but user created: {email_error}")
                # Return success even if email fails, but indicate the issue
                return {
                    "message": "User created successfully, but there was an issue sending the OTP email. Please contact support.",
                    "user_created": True
                }
        except HTTPException:
            # Re-raise HTTP exceptions (like 400 for user exists, 403 for admin signup)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in signup: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in signup: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/verify-otp")
def verify_otp(data: OTPVerifyRequest):
    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)

            user, msg = db.verify_otp_and_register(data.email, data.otp)
            if not user:
                raise HTTPException(status_code=400, detail=msg)

            # Decide check based on role
            role = user.get("role")
            if role == "vocalist":
                info_submitted = bool(db.is_vocalist_registered(user["id"]))
            elif role == "blogger":
                info_submitted = bool(db.is_blogger_registered(user["id"]))
            else:
                info_submitted = bool(db.is_writer_registered(user["id"]))

            access_token = create_access_token({
                "sub": str(user["id"]),
                "info_submitted": info_submitted
            })
            refresh_token = create_refresh_token({
                "sub": str(user["id"]),
                "info_submitted": info_submitted
            })

            user_data = {k: v for k, v in user.items() if k not in ("email", "password_hash")}
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "info_submitted": info_submitted,
                "user": user_data
            }
        except HTTPException:
            # Re-raise HTTP exceptions (like 400 for invalid OTP)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in verify_otp: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in verify_otp: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/login")
def login(data: LoginRequest):
    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)

            user = db.get_user_by_email(data.email)
            if not user:
                raise HTTPException(status_code=400, detail="User not found")

            if not user["is_registered"]:
                raise HTTPException(status_code=400, detail="User not verified. Please verify your email first.")

            if not verify_password(data.password, user["password_hash"]):
                raise HTTPException(status_code=400, detail="Invalid credentials")

            # Decide check based on role
            role = user.get("role")
            if role == "vocalist":
                info_submitted = bool(db.is_vocalist_registered(user["id"]))
            elif role == "blogger":
                info_submitted = bool(db.is_blogger_registered(user["id"]))
            else:
                info_submitted = bool(db.is_writer_registered(user["id"]))

            access_token = create_access_token({
                "sub": str(user["id"]),
                "info_submitted": info_submitted
            })
            refresh_token = create_refresh_token({
                "sub": str(user["id"]),
                "info_submitted": info_submitted
            })

            user_data = {k: v for k, v in user.items() if k not in ("email", "password_hash")}
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "info_submitted": info_submitted,
                "user": user_data
            }
        except HTTPException:
            # Re-raise HTTP exceptions (like 400 for invalid credentials)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in login: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in login: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


   

@router.post("/resend-otp")
def resend_otp(data: ResendOTPRequest):
    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)

            user = db.get_user_by_email(data.email)
            if not user:
                raise HTTPException(status_code=400, detail="User not found")
            if user["is_registered"]:
                raise HTTPException(status_code=400, detail="User already verified")

            otp = generate_otp()
            otp_expiry = get_otp_expiry()
            db.resend_otp(data.email, otp, otp_expiry)
            
            # Send OTP email, but handle errors gracefully
            try:
                send_otp_email(data.email, otp)
                return {"message": "OTP resent successfully."}
            except Exception as email_error:
                print(f"Email sending failed when resending OTP: {email_error}")
                # Return success even if email fails, but indicate the issue
                return {
                    "message": "OTP generated successfully, but there was an issue sending the email. Please contact support.",
                    "otp_sent": False
                }
        except HTTPException:
            # Re-raise HTTP exceptions (like 400 for user not found)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in resend_otp: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in resend_otp: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")




@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)

            user = db.get_user_by_email(data.email)
            if not user:
                raise HTTPException(status_code=400, detail="User not found")

            otp = generate_otp()
            otp_expiry = get_otp_expiry()
            db.resend_otp(data.email, otp, otp_expiry)  # Reuse resend_otp for storing OTP
            
            # Send OTP email, but handle errors gracefully
            try:
                send_otp_email(data.email, otp)
                return {"message": "OTP sent to your email for password reset"}
            except Exception as email_error:
                print(f"Email sending failed for password reset: {email_error}")
                # Return success even if email fails, but indicate the issue
                return {
                    "message": "Password reset initiated, but there was an issue sending the OTP email. Please contact support.",
                    "email_sent": False
                }
        except HTTPException:
            # Re-raise HTTP exceptions (like 400 for user not found)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in forgot_password: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in forgot_password: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

# ---------- Reset Password ----------

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)

            user = db.get_user_by_email(data.email)
            if not user:
                raise HTTPException(status_code=400, detail="User not found")

            verified_user, msg = db.verify_otp_and_register(data.email, data.otp)
            if not verified_user:
                raise HTTPException(status_code=400, detail=msg)

            hashed = hash_password(data.new_password)
            db.update_password(data.email, hashed)  # You need to implement update_password in UserQueries

            return {"message": "Password reset successfully"}
        except HTTPException:
            # Re-raise HTTP exceptions (like 400 for invalid OTP)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in reset_password: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in reset_password: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/refresh-token")
def refresh_token(data: RefreshTokenRequest):
    payload = verify_token(data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)
            user = db.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            new_access_token = create_access_token({"sub": str(user_id)})

            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }
        except HTTPException:
            # Re-raise HTTP exceptions (like 401, 404)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in refresh_token: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in refresh_token: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    
@router.post("/change-password")
def change_password(data: ChangePasswordRequest):
    with DBConnection.get_db_connection() as conn:
        try:
            db = Queries(conn)

            user = db.get_user_by_email(data.email)
            if not user:
                raise HTTPException(status_code=400, detail="User not found")

            if not verify_password(data.old_password, user["password_hash"]):
                raise HTTPException(status_code=400, detail="Old password is incorrect")

            hashed_new = hash_password(data.new_password)
            db.update_password(data.email, hashed_new)

            return {"message": "Password changed successfully"}
        except HTTPException:
            # Re-raise HTTP exceptions (like 400 for invalid credentials)
            raise
        except psycopg2.Error as e:
            # Rollback any failed transaction
            conn.rollback()
            print(f"Database error in change_password: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in change_password: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/google-auth")
def google_auth(data: GoogleAuthRequest):
    try:
        result, error = google_login_or_signup(data.token, data.role)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return result
    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for invalid token)
        raise
    except Exception as e:
        # Handle any other exceptions
        print(f"Error in google_auth: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")