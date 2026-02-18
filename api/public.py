from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from db.connection import DBConnection
from datetime import datetime
from sql.combinedQueries import Queries
from utils.otp import send_template_email

router = APIRouter(prefix="/public", tags=["Public"])

class PartnershipProposalCreate(BaseModel):
    full_name: str
    email: str
    organization_name: str
    role_title: str
    organization_type: Optional[str]
    partnership_type: Optional[str]
    website: Optional[str]
    proposal_text: str
    proposed_timeline: Optional[str]
    resources: Optional[str]
    goals: Optional[str]
    sacred_alignment: Optional[bool] = True

class PartnershipProposalResponse(BaseModel):
    id: int
    full_name: str
    email: str
    organization_name: str
    role_title: str
    organization_type: Optional[str]
    partnership_type: Optional[str]
    website: Optional[str]
    proposal_text: str
    proposed_timeline: Optional[str]
    resources: Optional[str]
    goals: Optional[str]
    sacred_alignment: bool
    created_at: str

@router.post("/", response_model=PartnershipProposalResponse)
def create_partnership_proposal(
    data: PartnershipProposalCreate,

):
    with DBConnection.get_db_connection() as conn:
        db = Queries(conn)

        query = """
        INSERT INTO partnership_proposals (
            full_name, email, organization_name, role_title, organization_type,
            partnership_type, website, proposal_text, proposed_timeline,
            resources, goals, sacred_alignment
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        with conn.cursor() as cur:
            cur.execute(query, (
                data.full_name,
                data.email,
                data.organization_name,
                data.role_title,
                data.organization_type,
                data.partnership_type,
                data.website,
                data.proposal_text,
                data.proposed_timeline,
                data.resources,
                data.goals,
                data.sacred_alignment
            ))
            proposal = cur.fetchone()
            conn.commit()

        # Send collaboration proposal received email
        try:
            from utils.otp import send_collaboration_proposal_email
            send_collaboration_proposal_email(data.email)
        except Exception as e:
            print(f"Failed to send collaboration proposal email: {e}")
            # Don't fail the request if email fails, just log the error

        return PartnershipProposalResponse(
            id=proposal[0],
            full_name=proposal[1],
            email=proposal[2],
            organization_name=proposal[3],
            role_title=proposal[4],
            organization_type=proposal[5],
            partnership_type=proposal[6],
            website=proposal[7],
            proposal_text=proposal[8],
            proposed_timeline=proposal[9],
            resources=proposal[10],
            goals=proposal[11],
            sacred_alignment=proposal[12],
            created_at=str(proposal[13])
        )





@router.get("/postedkalams", response_model=List[dict])
def get_posted_kalams(
    skip: int = Query(0, ge=0),  # how many to skip
    limit: int = Query(4, ge=1),  # how many to fetch
):
    conn = DBConnection.get_connection()
    db = Queries(conn)
   
    return db.fetch_posted_kalams(skip, limit)




@router.get("/vocalists", response_model=List[dict])
def get_vocalists(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    conn = DBConnection.get_connection()
    db = Queries(conn)
    return db.fetch_vocalists(skip, limit)





@router.get("/posts", response_model=List[dict])
def get_guest_posts_paginated(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    conn = DBConnection.get_connection()
    db = Queries(conn)
    
    try:
        return db.fetch_paginated_guest_posts(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







@router.get("/writers", response_model=List[dict])
def get_writers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    conn = DBConnection.get_connection()
    db = Queries(conn)
    return db.fetch_writers(skip, limit)





@router.get("/special-recognitions/all", response_model=List[dict])
def get_all_special_recognitions():
    conn = DBConnection.get_connection()
    db = Queries(conn)

    try:
        return db.fetch_all_special_recognitions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blogs", response_model=List[dict])
def get_approved_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(6, ge=1),
    category: Optional[str] = None,
    search: Optional[str] = None
):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    try:
        # Fetch only approved and posted blogs
        blogs = db.fetch_approved_blogs(skip, limit, category, search)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blogs/{blog_id}")
def get_blog_by_id(blog_id: int):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    try:
        blog = db.fetch_blog_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog post not found")
        return blog
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ContactFormSubmit(BaseModel):
    name: str
    email: str
    subject: str
    message: str


@router.post("/contact")
def submit_contact_form(data: ContactFormSubmit):
    """
    Submit contact form and send confirmation email using Resend template
    """
    try:
        # Validate input
        if not data.name or not data.email or not data.subject or not data.message:
            raise HTTPException(status_code=400, detail="All fields are required")
        
        # Send confirmation email to user using template
        try:
            send_template_email(
                to_email=data.email,
                template_id="contact-form-notification",
                subject="Thank You for Contacting SufiPulse",
                variables={
                    "name": data.name,
                    "email": data.email,
                    "subject": data.subject,
                    "message": data.message
                }
            )
        except Exception as email_error:
            print(f"Failed to send confirmation email: {email_error}")
            # Don't fail the request if email fails, just log the error
        
        # Send notification email to admin
        try:
            send_template_email(
                to_email="contact@sufipulse.com",
                template_id="contact-form-notification",
                subject=f"New Contact Form: {data.subject}",
                variables={
                    "name": data.name,
                    "email": data.email,
                    "subject": data.subject,
                    "message": data.message
                }
            )
        except Exception as admin_email_error:
            print(f"Failed to send admin notification: {admin_email_error}")
        
        return {
            "message": "Message sent successfully! We will get back to you soon.",
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in contact form: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))