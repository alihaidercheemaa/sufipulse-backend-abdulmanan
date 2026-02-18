from pydantic import BaseModel
from typing import Optional,Union
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from db.connection import DBConnection
from utils.jwt_handler import get_current_user
from sql.combinedQueries import Queries

# Studio Visit Request Models
class StudioVisitRequestCreate(BaseModel):
    vocalist_id: int
    kalam_id: int
    name: str
    email: str
    organization: Optional[str] = None
    contact_number: Optional[str] = None
    preferred_date: Optional[date] = None
    preferred_time: Optional[str] = None
    purpose: Optional[str] = None
    number_of_visitors: Optional[Union[str, int]] = None
    additional_details: Optional[str] = None
    special_requests: Optional[str] = None

class StudioVisitRequestResponse(BaseModel):
    id: int
    vocalist_id: int
    kalam_id: int
    name: str
    email: str
    organization: Optional[str]
    contact_number: Optional[str]
    preferred_date: Optional[date]
    preferred_time: Optional[str]
    purpose: Optional[str]
    number_of_visitors: Optional[Union[str, int]] = None
    additional_details: Optional[str]
    special_requests: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

# Remote Recording Request Models
class RemoteRecordingRequestCreate(BaseModel):
    vocalist_id: int
    kalam_id: int
    name: str
    email: str
    city: Optional[str] = None
    country: Optional[str] = None
    time_zone: Optional[str] = None
    role: Optional[str] = None
    project_type: Optional[str] = None
    recording_equipment: Optional[str] = None
    internet_speed: Optional[str] = None
    preferred_software: Optional[str] = None
    availability: Optional[str] = None
    recording_experience: Optional[str] = None
    technical_setup: Optional[str] = None
    additional_details: Optional[str] = None

class RemoteRecordingRequestResponse(BaseModel):
    id: int
    vocalist_id: int
    kalam_id: int
    name: str
    email: str
    city: Optional[str]
    country: Optional[str]
    time_zone: Optional[str]
    role: Optional[str]
    project_type: Optional[str]
    recording_equipment: Optional[str]
    internet_speed: Optional[str]
    preferred_software: Optional[str]
    availability: Optional[str]
    recording_experience: Optional[str]
    technical_setup: Optional[str]
    additional_details: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/studio-visit-request", response_model=StudioVisitRequestResponse)
def create_studio_visit_request(
    data: StudioVisitRequestCreate,
    user_id: int = Depends(get_current_user)
):
    with DBConnection.get_db_connection() as conn:
        db = Queries(conn)

        user = db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.get("role") != "vocalist":
            raise HTTPException(status_code=403, detail="Only vocalists can create studio visit requests")

        if data.vocalist_id != int(user.get("id")):
            raise HTTPException(status_code=403, detail="Vocalist ID must match authenticated user")

        result = db.create_studio_visit_request(data.dict())
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create studio visit request")

        # Send studio visit request confirmation email
        try:
            from utils.otp import send_studio_visit_request_email
            # Use the email from the request data
            send_studio_visit_request_email(data.email)
        except Exception as e:
            print(f"Failed to send studio visit request confirmation email: {e}")
            # Don't fail the request if email fails, just log the error

        return StudioVisitRequestResponse(**result)

@router.get("/studio-visit-requests", response_model=list[StudioVisitRequestResponse])
def get_all_studio_visit_requests(user_id: int = Depends(get_current_user)):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("role") not in ['admin','sub-admin']:
        raise HTTPException(status_code=403, detail="Only admins can view all studio visit requests")

    requests = db.get_all_studio_visit_requests()
    return [StudioVisitRequestResponse(**req) for req in requests]

@router.get("/studio-visit-requests/vocalist", response_model=list[StudioVisitRequestResponse])
def get_studio_visit_requests_by_vocalist(user_id: int = Depends(get_current_user)):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("role") != "vocalist":
        raise HTTPException(status_code=403, detail="Only vocalists can view their studio visit requests")

    requests = db.get_studio_visit_requests_by_vocalist(int(user.get("id")))
    return [StudioVisitRequestResponse(**req) for req in requests]

@router.post("/remote-recording-request", response_model=RemoteRecordingRequestResponse)
def create_remote_recording_request(
    data: RemoteRecordingRequestCreate,
    user_id: int = Depends(get_current_user)
):
    with DBConnection.get_db_connection() as conn:
        db = Queries(conn)

        user = db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.get("role") != "vocalist":
            raise HTTPException(status_code=403, detail="Only vocalists can create remote recording requests")

        if data.vocalist_id != int(user.get("id")):
            raise HTTPException(status_code=403, detail="Vocalist ID must match authenticated user")

        result = db.create_remote_recording_request(data.dict())
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create remote recording request")

        # Send recording session confirmation email
        try:
            from utils.otp import send_recording_session_confirmation_email
            # Use the email from the request data
            send_recording_session_confirmation_email(data.email)
        except Exception as e:
            print(f"Failed to send recording session confirmation email: {e}")
            # Don't fail the request if email fails, just log the error

        return RemoteRecordingRequestResponse(**result)

@router.get("/remote-recording-requests", response_model=list[RemoteRecordingRequestResponse])
def get_all_remote_recording_requests(user_id: int = Depends(get_current_user)):
    with DBConnection.get_db_connection() as conn:
        db = Queries(conn)

        user = db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.get("role") not in ['admin','sub-admin']:
            raise HTTPException(status_code=403, detail="Only admins can view all remote recording requests")

        requests = db.get_all_remote_recording_requests()
        return [RemoteRecordingRequestResponse(**req) for req in requests]

@router.get("/remote-recording-requests/vocalist", response_model=list[RemoteRecordingRequestResponse])
def get_remote_recording_requests_by_vocalist(user_id: int = Depends(get_current_user)):
    with DBConnection.get_db_connection() as conn:
        db = Queries(conn)

        user = db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.get("role") != "vocalist":
            raise HTTPException(status_code=403, detail="Only vocalists can view their remote recording requests")

        requests = db.get_remote_recording_requests_by_vocalist(int(user.get("id")))
        return [RemoteRecordingRequestResponse(**req) for req in requests]




@router.get("/check-request-exists/{vocalist_id}/{kalam_id}")
def check_request_exists(vocalist_id: int, kalam_id: int, user_id: int = Depends(get_current_user)):
    with DBConnection.get_db_connection() as conn:
        db = Queries(conn)

        studio_conflict = db.studio_request_exists(vocalist_id, kalam_id)
        remote_conflict = db.remote_request_exists(vocalist_id, kalam_id)

        return {"is_booked": studio_conflict or remote_conflict}


class StatusUpdateRequest(BaseModel):
    status: str
    admin_comments: Optional[str] = None

@router.put("/studio-visit-requests/{request_id}/status")
def update_studio_visit_request_status(
    request_id: int,
    data: StatusUpdateRequest,
    user_id: int = Depends(get_current_user)
):
    """Update studio visit request status (Admin only)"""
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("role") not in ["admin", "sub-admin"]:
        raise HTTPException(status_code=403, detail="Only admins can update request status")

    # Get the request
    get_query = """
        SELECT * FROM studio_visit_requests
        WHERE id = %s
    """
    with conn.cursor() as cur:
        cur.execute(get_query, (request_id,))
        request = cur.fetchone()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Update status
    update_query = """
        UPDATE studio_visit_requests
        SET status = %s, admin_comments = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *;
    """
    with conn.cursor() as cur:
        cur.execute(update_query, (data.status, data.admin_comments, request_id))
        result = cur.fetchone()
        conn.commit()

    if not result:
        raise HTTPException(status_code=500, detail="Failed to update request status")

    return {"message": f"Studio visit request {data.status}", "request": result}


@router.put("/remote-recording-requests/{request_id}/status")
def update_remote_recording_request_status(
    request_id: int,
    data: StatusUpdateRequest,
    user_id: int = Depends(get_current_user)
):
    """Update remote recording request status (Admin only)"""
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("role") not in ["admin", "sub-admin"]:
        raise HTTPException(status_code=403, detail="Only admins can update request status")

    # Get the request
    get_query = """
        SELECT * FROM remote_recording_requests
        WHERE id = %s
    """
    with conn.cursor() as cur:
        cur.execute(get_query, (request_id,))
        request = cur.fetchone()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Update status
    update_query = """
        UPDATE remote_recording_requests
        SET status = %s, admin_comments = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING *;
    """
    with conn.cursor() as cur:
        cur.execute(update_query, (data.status, data.admin_comments, request_id))
        result = cur.fetchone()
        conn.commit()

    if not result:
        raise HTTPException(status_code=500, detail="Failed to update request status")

    return {"message": f"Remote recording request {data.status}", "request": result}
