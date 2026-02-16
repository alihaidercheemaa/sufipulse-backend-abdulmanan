from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from psycopg2.extras import RealDictCursor
from db import DBConnection  # adjust your import
from utils.jwt_handler import get_current_user
from sql.combinedQueries import Queries
from datetime import datetime
import uuid
import os

router = APIRouter(prefix="/bloggers", tags=["Bloggers"])

class SubmitBloggerProfile(BaseModel):
    author_name: Optional[str] = None
    author_image_url: Optional[str] = None
    short_bio: Optional[str] = None
    location: Optional[str] = None
    website_url: Optional[str] = None
    social_links: Optional[dict] = {}
    publish_pseudonym: Optional[bool] = False
    original_work_confirmation: Optional[bool] = False
    publishing_rights_granted: Optional[bool] = False
    discourse_policy_agreed: Optional[bool] = False

class SubmitBlogPost(BaseModel):
    title: str
    excerpt: str
    featured_image_url: Optional[str] = None
    content: str
    category: str
    tags: List[str] = []
    language: str
    editor_notes: Optional[str] = None
    scheduled_publish_date: Optional[datetime] = None
    seo_meta_title: Optional[str] = None
    seo_meta_description: Optional[str] = None

class BlogApprovalRequest(BaseModel):
    status: str  # 'approved', 'rejected', 'changes_requested', etc.
    admin_comments: Optional[str] = None

# ---------------- Routes ---------------- #

@router.post("/submit-profile")
def submit_blogger_profile(data: SubmitBloggerProfile, user_id: int = Depends(get_current_user)):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    existing = db.get_blogger_by_user_id(user_id)
    if existing:
        db.update_blogger_profile(
            user_id=user_id,
            author_name=data.author_name,
            author_image_url=data.author_image_url,
            short_bio=data.short_bio,
            location=data.location,
            website_url=data.website_url,
            social_links=data.social_links,
            publish_pseudonym=data.publish_pseudonym,
            original_work_confirmation=data.original_work_confirmation,
            publishing_rights_granted=data.publishing_rights_granted,
            discourse_policy_agreed=data.discourse_policy_agreed
        )
        return {"message": "Blogger profile updated successfully"}
    else:
        db.create_blogger_profile(
            user_id=user_id,
            author_name=data.author_name,
            author_image_url=data.author_image_url,
            short_bio=data.short_bio,
            location=data.location,
            website_url=data.website_url,
            social_links=data.social_links,
            publish_pseudonym=data.publish_pseudonym,
            original_work_confirmation=data.original_work_confirmation,
            publishing_rights_granted=data.publishing_rights_granted,
            discourse_policy_agreed=data.discourse_policy_agreed
        )
        return {"message": "Blogger profile submitted successfully"}


@router.get("/get/{blogger_id}")
def get_blogger_profile(
    blogger_id: int,
    current_user_id: int = Depends(get_current_user)
):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["role"] == "blogger":
        profile = db.get_blogger_by_user_id(user["id"])
    elif user["role"] in ['admin', 'sub-admin']:
        profile = db.get_blogger_by_user_id(blogger_id)
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view blogger profiles")

    if not profile:
        raise HTTPException(status_code=404, detail="Blogger profile not found")

    profile.pop("id", None)
    return profile


@router.get("/is-registered")
def check_blogger_registration(user_id: int = Depends(get_current_user)):
    conn = DBConnection.get_connection()
    db = Queries(conn)
    blogger = db.is_blogger_registered(user_id)

    if not blogger:
        return {"is_registered": False}
    return {"is_registered": True}


@router.post("/submit-blog")
def submit_blog_post(data: SubmitBlogPost, user_id: int = Depends(get_current_user)):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    # Check if user is a blogger
    blogger = db.get_blogger_by_user_id(user_id)
    if not blogger:
        raise HTTPException(status_code=403, detail="Only registered bloggers can submit blog posts")

    # Insert the blog submission with new fields
    result = db.create_blog_submission(
        title=data.title,
        excerpt=data.excerpt,
        featured_image_url=data.featured_image_url,
        content=data.content,
        category=data.category,
        tags=data.tags,
        language=data.language,
        user_id=user_id,
        editor_notes=data.editor_notes,
        scheduled_publish_date=data.scheduled_publish_date,
        seo_meta_title=data.seo_meta_title,
        seo_meta_description=data.seo_meta_description
    )

    return {"message": "Blog post submitted successfully", "submission_id": result}


@router.get("/my-blogs")
def get_my_blog_submissions(current_user_id: int = Depends(get_current_user)):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(current_user_id)
    if not user or user["role"] != "blogger":
        raise HTTPException(status_code=403, detail="Only bloggers can access their blog submissions")

    blogs = db.get_blog_submissions_by_user_id(current_user_id)
    return {"user_id": current_user_id, "blogs": blogs}


@router.get("/blog/{blog_id}")
def get_blog_submission(blog_id: int, current_user_id: int = Depends(get_current_user)):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(current_user_id)
    if not user or user["role"] not in ["blogger", "admin", "sub-admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view blog submissions")

    blog = db.get_blog_submission_by_id(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog submission not found")

    return blog


@router.put("/blog/{blog_id}")
def update_blog_post(
    blog_id: int,
    data: SubmitBlogPost,
    current_user_id: int = Depends(get_current_user)
):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    # Check if user is the owner of the blog
    blog = db.get_blog_submission_by_id(blog_id)
    if not blog or blog["user_id"] != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this blog post")

    # Update the blog submission with new fields
    result = db.update_blog_submission(
        blog_id=blog_id,
        title=data.title,
        excerpt=data.excerpt,
        featured_image_url=data.featured_image_url,
        content=data.content,
        category=data.category,
        tags=data.tags,
        language=data.language,
        editor_notes=data.editor_notes,
        scheduled_publish_date=data.scheduled_publish_date,
        seo_meta_title=data.seo_meta_title,
        seo_meta_description=data.seo_meta_description
    )

    if not result:
        raise HTTPException(status_code=404, detail="Blog submission not found")

    return {"message": "Blog post updated successfully", "blog_submission": result}


@router.post("/blog/{blog_id}/approval")
def approve_or_reject_blog(
    blog_id: int,
    data: BlogApprovalRequest,
    current_user_id: int = Depends(get_current_user)
):
    conn = DBConnection.get_connection()
    db = Queries(conn)

    user = db.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["role"] not in ["admin", "sub-admin"]:
        raise HTTPException(status_code=403, detail="Only admins can approve/reject blog submissions")

    # Get the blog to find the owner
    blog = db.get_blog_submission_by_id(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog submission not found")

    # Update the blog submission status
    result = db.update_blog_submission_status(
        blog_id=blog_id,
        status=data.status,
        admin_comments=data.admin_comments
    )

    if not result:
        raise HTTPException(status_code=404, detail="Blog submission not found")

    # Create a notification for the blogger
    try:
        status_messages = {
            'pending': 'Your blog is now pending review',
            'review': 'Your blog is under review',
            'approved': 'Congratulations! Your blog has been approved',
            'revision': 'Your blog needs some revisions',
            'rejected': 'Your blog has been rejected',
            'posted': 'Your blog has been posted!'
        }
        
        notification_title = "Blog Status Update"
        notification_message = f"{status_messages.get(data.status, 'Blog status updated')}: {blog['title']}"
        if data.admin_comments:
            notification_message += f" - Admin comment: {data.admin_comments}"
        
        # Create notification for the blog owner
        db.create_notification(
            title=notification_title,
            message=notification_message,
            target_type='specific',
            target_user_ids=[blog['user_id']]
        )
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Failed to create notification: {str(e)}")

    return {"message": f"Blog submission status updated to {data.status} successfully", "blog_submission": result}
