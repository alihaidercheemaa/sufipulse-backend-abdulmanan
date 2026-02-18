from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from db.connection import DBConnection
from sql.combinedQueries import Queries
from utils.jwt_handler import get_current_user
from datetime import datetime

router = APIRouter(
    prefix="/cms",
    tags=["CMS Management"]
)

# =========================
# Pydantic Models
# =========================

class CMSPageBase(BaseModel):
    page_name: str
    page_title: str
    page_slug: str
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    hero_quote: Optional[str] = None
    hero_quote_author: Optional[str] = None
    is_active: bool = True

class CMSPageCreate(CMSPageBase):
    pass

class CMSPageUpdate(BaseModel):
    page_title: Optional[str] = None
    page_slug: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    hero_quote: Optional[str] = None
    hero_quote_author: Optional[str] = None
    is_active: Optional[bool] = None

class CMSPageResponse(CMSPageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CMSStatBase(BaseModel):
    stat_number: str
    stat_label: str
    stat_description: Optional[str] = None
    stat_icon: Optional[str] = None
    stat_order: int = 0
    is_active: bool = True

class CMSStatCreate(CMSStatBase):
    page_id: int

class CMSStatUpdate(BaseModel):
    stat_number: Optional[str] = None
    stat_label: Optional[str] = None
    stat_description: Optional[str] = None
    stat_icon: Optional[str] = None
    stat_order: Optional[int] = None
    is_active: Optional[bool] = None

class CMSValueBase(BaseModel):
    value_title: str
    value_description: Optional[str] = None
    value_icon: Optional[str] = None
    value_color: Optional[str] = 'emerald'
    value_order: int = 0
    is_active: bool = True

class CMSValueCreate(CMSValueBase):
    page_id: int

class CMSValueUpdate(BaseModel):
    value_title: Optional[str] = None
    value_description: Optional[str] = None
    value_icon: Optional[str] = None
    value_color: Optional[str] = None
    value_order: Optional[int] = None
    is_active: Optional[bool] = None

class CMSTeamBase(BaseModel):
    member_name: str
    member_role: Optional[str] = None
    member_organization: Optional[str] = None
    member_bio: Optional[str] = None
    member_image_url: Optional[str] = None
    is_featured: bool = False
    member_order: int = 0
    is_active: bool = True

class CMSTeamCreate(CMSTeamBase):
    page_id: int

class CMSTeamUpdate(BaseModel):
    member_name: Optional[str] = None
    member_role: Optional[str] = None
    member_organization: Optional[str] = None
    member_bio: Optional[str] = None
    member_image_url: Optional[str] = None
    is_featured: Optional[bool] = None
    member_order: Optional[int] = None
    is_active: Optional[bool] = None

class CMSTimelineBase(BaseModel):
    timeline_year: str
    timeline_title: str
    timeline_description: Optional[str] = None
    timeline_order: int = 0
    is_active: bool = True

class CMSTimelineCreate(CMSTimelineBase):
    page_id: int

class CMSTimelineUpdate(BaseModel):
    timeline_year: Optional[str] = None
    timeline_title: Optional[str] = None
    timeline_description: Optional[str] = None
    timeline_order: Optional[int] = None
    is_active: Optional[bool] = None

class CMSTestimonialBase(BaseModel):
    testimonial_name: str
    testimonial_location: Optional[str] = None
    testimonial_role: Optional[str] = None
    testimonial_quote: str
    testimonial_image_url: Optional[str] = None
    testimonial_order: int = 0
    is_active: bool = True

class CMSTestimonialCreate(CMSTestimonialBase):
    page_id: int

class CMSTestimonialUpdate(BaseModel):
    testimonial_name: Optional[str] = None
    testimonial_location: Optional[str] = None
    testimonial_role: Optional[str] = None
    testimonial_quote: Optional[str] = None
    testimonial_image_url: Optional[str] = None
    testimonial_order: Optional[int] = None
    is_active: Optional[bool] = None

class CMSSectionBase(BaseModel):
    section_name: str
    section_type: str
    section_title: Optional[str] = None
    section_subtitle: Optional[str] = None
    section_content: Optional[str] = None
    section_order: int = 0
    is_active: bool = True

class CMSSectionCreate(CMSSectionBase):
    page_id: int

class CMSSectionUpdate(BaseModel):
    section_name: Optional[str] = None
    section_type: Optional[str] = None
    section_title: Optional[str] = None
    section_subtitle: Optional[str] = None
    section_content: Optional[str] = None
    section_order: Optional[int] = None
    is_active: Optional[bool] = None

class CMSSectionItemBase(BaseModel):
    item_title: str
    item_subtitle: Optional[str] = None
    item_description: Optional[str] = None
    item_icon: Optional[str] = None
    item_field: Optional[str] = None
    item_order: int = 0
    is_active: bool = True

class CMSSectionItemCreate(CMSSectionItemBase):
    section_id: int

class CMSSectionItemUpdate(BaseModel):
    item_title: Optional[str] = None
    item_subtitle: Optional[str] = None
    item_description: Optional[str] = None
    item_icon: Optional[str] = None
    item_field: Optional[str] = None
    item_order: Optional[int] = None
    is_active: Optional[bool] = None

class CMSHubBase(BaseModel):
    hub_title: str
    hub_details: Optional[str] = None
    hub_description: Optional[str] = None
    hub_icon: Optional[str] = None
    hub_order: int = 0
    is_active: bool = True

class CMSHubCreate(CMSHubBase):
    page_id: int

class CMSHubUpdate(BaseModel):
    hub_title: Optional[str] = None
    hub_details: Optional[str] = None
    hub_description: Optional[str] = None
    hub_icon: Optional[str] = None
    hub_order: Optional[int] = None
    is_active: Optional[bool] = None

# =========================
# Helper Functions
# =========================

def check_admin_permission(current_user_id: int):
    """Check if user has admin or sub-admin permissions"""
    conn = DBConnection.get_connection()
    db = Queries(conn)
    
    user = db.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user["role"] not in ["admin", "sub-admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user

# =========================
# Public Routes - Get Page Data
# =========================

@router.get("/page/{page_slug}")
def get_page_data(page_slug: str):
    """Get complete page data by slug (public endpoint)"""
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM get_cms_page_data(%s)", (page_slug,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Page not found")
        
        # Map column names
        columns = [desc[0] for desc in cursor.description]
        page_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "data": page_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/pages")
def get_all_pages():
    """Get list of all CMS pages (public endpoint)"""
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM get_all_cms_pages()")
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        pages = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# =========================
# Admin Routes - Page Management
# =========================

@router.get("/admin/pages")
def admin_get_all_pages(current_user_id: int = Depends(get_current_user)):
    """Get all pages with full details (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, page_name, page_title, page_slug, meta_description, 
                   meta_keywords, hero_title, hero_subtitle, hero_quote, 
                   hero_quote_author, is_active, created_at, updated_at
            FROM cms_pages
            ORDER BY page_name
        """)
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        pages = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/admin/pages", status_code=status.HTTP_201_CREATED)
def admin_create_page(
    page: CMSPageCreate,
    current_user_id: int = Depends(get_current_user)
):
    """Create a new CMS page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cms_pages (
                page_name, page_title, page_slug, meta_description, 
                meta_keywords, hero_title, hero_subtitle, hero_quote, 
                hero_quote_author, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, page_name, page_title, page_slug, meta_description, 
                      meta_keywords, hero_title, hero_subtitle, hero_quote, 
                      hero_quote_author, is_active, created_at, updated_at
        """, (
            page.page_name, page.page_title, page.page_slug, 
            page.meta_description, page.meta_keywords, page.hero_title, 
            page.hero_subtitle, page.hero_quote, page.hero_quote_author, 
            page.is_active
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        columns = [desc[0] for desc in cursor.description]
        page_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Page created successfully",
            "data": page_data
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/pages/{page_id}")
def admin_update_page(
    page_id: int,
    page: CMSPageUpdate,
    current_user_id: int = Depends(get_current_user)
):
    """Update a CMS page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        # Build dynamic update query
        update_fields = []
        values = []
        
        for field, value in page.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(page_id)
        query = f"""
            UPDATE cms_pages 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, page_name, page_title, page_slug, meta_description, 
                      meta_keywords, hero_title, hero_subtitle, hero_quote, 
                      hero_quote_author, is_active, created_at, updated_at
        """
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Page not found")
        
        columns = [desc[0] for desc in cursor.description]
        page_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Page updated successfully",
            "data": page_data
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/pages/{page_id}")
def admin_delete_page(
    page_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Delete a CMS page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cms_pages WHERE id = %s RETURNING id", (page_id,))
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Page not found")
        
        return {
            "success": True,
            "message": "Page deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# =========================
# Admin Routes - Stats Management
# =========================

@router.get("/admin/stats/{stat_id}")
def admin_get_stat(
    stat_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Get a single stat by ID (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM cms_page_stats 
            WHERE id = %s
        """, (stat_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Stat not found")
        
        columns = [desc[0] for desc in cursor.description]
        stat = dict(zip(columns, result))
        
        return {
            "success": True,
            "data": stat
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/admin/pages/{page_id}/stats")
def admin_get_page_stats(
    page_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Get all stats for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM cms_page_stats 
            WHERE page_id = %s 
            ORDER BY stat_order
        """, (page_id,))
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        stats = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/admin/pages/{page_id}/stats", status_code=status.HTTP_201_CREATED)
def admin_create_stat(
    page_id: int,
    stat: CMSStatBase,
    current_user_id: int = Depends(get_current_user)
):
    """Create a new stat for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cms_page_stats (
                page_id, stat_number, stat_label, stat_description, 
                stat_icon, stat_order, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            page_id, stat.stat_number, stat.stat_label, 
            stat.stat_description, stat.stat_icon, stat.stat_order, stat.is_active
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        columns = [desc[0] for desc in cursor.description]
        stat_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Stat created successfully",
            "data": stat_data
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/stats/{stat_id}")
def admin_update_stat(
    stat_id: int,
    stat: CMSStatUpdate,
    current_user_id: int = Depends(get_current_user)
):
    """Update a page stat (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        update_fields = []
        values = []
        
        for field, value in stat.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(value)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(stat_id)
        query = f"""
            UPDATE cms_page_stats 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Stat not found")
        
        columns = [desc[0] for desc in cursor.description]
        stat_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Stat updated successfully",
            "data": stat_data
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/stats/{stat_id}")
def admin_delete_stat(
    stat_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Delete a page stat (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cms_page_stats WHERE id = %s RETURNING id", (stat_id,))
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Stat not found")
        
        return {
            "success": True,
            "message": "Stat deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# =========================
# Admin Routes - Values Management
# =========================

@router.get("/admin/pages/{page_id}/values")
def admin_get_page_values(
    page_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Get all values for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM cms_page_values 
            WHERE page_id = %s 
            ORDER BY value_order
        """, (page_id,))
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        values = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": values
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/admin/pages/{page_id}/values", status_code=status.HTTP_201_CREATED)
def admin_create_value(
    page_id: int,
    value: CMSValueBase,
    current_user_id: int = Depends(get_current_user)
):
    """Create a new value for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cms_page_values (
                page_id, value_title, value_description, value_icon, 
                value_color, value_order, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            page_id, value.value_title, value.value_description, 
            value.value_icon, value.value_color, value.value_order, value.is_active
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        columns = [desc[0] for desc in cursor.description]
        value_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Value created successfully",
            "data": value_data
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/values/{value_id}")
def admin_update_value(
    value_id: int,
    value: CMSValueUpdate,
    current_user_id: int = Depends(get_current_user)
):
    """Update a page value (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        update_fields = []
        values = []
        
        for field, val in value.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(val)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(value_id)
        query = f"""
            UPDATE cms_page_values 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Value not found")
        
        columns = [desc[0] for desc in cursor.description]
        value_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Value updated successfully",
            "data": value_data
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/values/{value_id}")
def admin_delete_value(
    value_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Delete a page value (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cms_page_values WHERE id = %s RETURNING id", (value_id,))
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Value not found")
        
        return {
            "success": True,
            "message": "Value deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# =========================
# Admin Routes - Team Management
# =========================

@router.get("/admin/pages/{page_id}/team")
def admin_get_page_team(
    page_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Get all team members for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM cms_page_team 
            WHERE page_id = %s 
            ORDER BY member_order
        """, (page_id,))
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        team = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": team
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/admin/pages/{page_id}/team", status_code=status.HTTP_201_CREATED)
def admin_create_team_member(
    page_id: int,
    member: CMSTeamBase,
    current_user_id: int = Depends(get_current_user)
):
    """Create a new team member for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cms_page_team (
                page_id, member_name, member_role, member_organization, 
                member_bio, member_image_url, is_featured, member_order, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            page_id, member.member_name, member.member_role, 
            member.member_organization, member.member_bio, 
            member.member_image_url, member.is_featured, 
            member.member_order, member.is_active
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        columns = [desc[0] for desc in cursor.description]
        member_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Team member created successfully",
            "data": member_data
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/team/{member_id}")
def admin_update_team_member(
    member_id: int,
    member: CMSTeamUpdate,
    current_user_id: int = Depends(get_current_user)
):
    """Update a team member (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        update_fields = []
        values = []
        
        for field, val in member.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(val)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(member_id)
        query = f"""
            UPDATE cms_page_team 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        columns = [desc[0] for desc in cursor.description]
        member_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Team member updated successfully",
            "data": member_data
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/team/{member_id}")
def admin_delete_team_member(
    member_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Delete a team member (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cms_page_team WHERE id = %s RETURNING id", (member_id,))
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        return {
            "success": True,
            "message": "Team member deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# =========================
# Admin Routes - Timeline Management
# =========================

@router.get("/admin/pages/{page_id}/timeline")
def admin_get_page_timeline(
    page_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Get all timeline items for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM cms_page_timeline 
            WHERE page_id = %s 
            ORDER BY timeline_order
        """, (page_id,))
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        timeline = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": timeline
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/admin/pages/{page_id}/timeline", status_code=status.HTTP_201_CREATED)
def admin_create_timeline_item(
    page_id: int,
    timeline: CMSTimelineBase,
    current_user_id: int = Depends(get_current_user)
):
    """Create a new timeline item for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cms_page_timeline (
                page_id, timeline_year, timeline_title, timeline_description, 
                timeline_order, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            page_id, timeline.timeline_year, timeline.timeline_title, 
            timeline.timeline_description, timeline.timeline_order, timeline.is_active
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        columns = [desc[0] for desc in cursor.description]
        timeline_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Timeline item created successfully",
            "data": timeline_data
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/timeline/{timeline_id}")
def admin_update_timeline_item(
    timeline_id: int,
    timeline: CMSTimelineUpdate,
    current_user_id: int = Depends(get_current_user)
):
    """Update a timeline item (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        update_fields = []
        values = []
        
        for field, val in timeline.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(val)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(timeline_id)
        query = f"""
            UPDATE cms_page_timeline 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Timeline item not found")
        
        columns = [desc[0] for desc in cursor.description]
        timeline_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Timeline item updated successfully",
            "data": timeline_data
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/timeline/{timeline_id}")
def admin_delete_timeline_item(
    timeline_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Delete a timeline item (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cms_page_timeline WHERE id = %s RETURNING id", (timeline_id,))
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Timeline item not found")
        
        return {
            "success": True,
            "message": "Timeline item deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# =========================
# Admin Routes - Testimonials Management
# =========================

@router.get("/admin/pages/{page_id}/testimonials")
def admin_get_page_testimonials(
    page_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Get all testimonials for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM cms_page_testimonials 
            WHERE page_id = %s 
            ORDER BY testimonial_order
        """, (page_id,))
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        testimonials = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": testimonials
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/admin/pages/{page_id}/testimonials", status_code=status.HTTP_201_CREATED)
def admin_create_testimonial(
    page_id: int,
    testimonial: CMSTestimonialBase,
    current_user_id: int = Depends(get_current_user)
):
    """Create a new testimonial for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cms_page_testimonials (
                page_id, testimonial_name, testimonial_location, testimonial_role, 
                testimonial_quote, testimonial_image_url, testimonial_order, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            page_id, testimonial.testimonial_name, testimonial.testimonial_location, 
            testimonial.testimonial_role, testimonial.testimonial_quote, 
            testimonial.testimonial_image_url, testimonial.testimonial_order, 
            testimonial.is_active
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        columns = [desc[0] for desc in cursor.description]
        testimonial_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Testimonial created successfully",
            "data": testimonial_data
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/testimonials/{testimonial_id}")
def admin_update_testimonial(
    testimonial_id: int,
    testimonial: CMSTestimonialUpdate,
    current_user_id: int = Depends(get_current_user)
):
    """Update a testimonial (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        update_fields = []
        values = []
        
        for field, val in testimonial.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(val)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(testimonial_id)
        query = f"""
            UPDATE cms_page_testimonials 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        columns = [desc[0] for desc in cursor.description]
        testimonial_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Testimonial updated successfully",
            "data": testimonial_data
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/testimonials/{testimonial_id}")
def admin_delete_testimonial(
    testimonial_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Delete a testimonial (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cms_page_testimonials WHERE id = %s RETURNING id", (testimonial_id,))
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        return {
            "success": True,
            "message": "Testimonial deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# =========================
# Admin Routes - Hubs Management (for Contact page)
# =========================

@router.get("/admin/pages/{page_id}/hubs")
def admin_get_page_hubs(
    page_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Get all hubs for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM cms_page_hubs 
            WHERE page_id = %s 
            ORDER BY hub_order
        """, (page_id,))
        results = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        hubs = [dict(zip(columns, row)) for row in results]
        
        return {
            "success": True,
            "data": hubs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/admin/pages/{page_id}/hubs", status_code=status.HTTP_201_CREATED)
def admin_create_hub(
    page_id: int,
    hub: CMSHubBase,
    current_user_id: int = Depends(get_current_user)
):
    """Create a new hub for a page (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cms_page_hubs (
                page_id, hub_title, hub_details, hub_description, 
                hub_icon, hub_order, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            page_id, hub.hub_title, hub.hub_details, 
            hub.hub_description, hub.hub_icon, hub.hub_order, hub.is_active
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        columns = [desc[0] for desc in cursor.description]
        hub_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Hub created successfully",
            "data": hub_data
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/hubs/{hub_id}")
def admin_update_hub(
    hub_id: int,
    hub: CMSHubUpdate,
    current_user_id: int = Depends(get_current_user)
):
    """Update a hub (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        update_fields = []
        values = []
        
        for field, val in hub.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(val)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(hub_id)
        query = f"""
            UPDATE cms_page_hubs 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *
        """
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Hub not found")
        
        columns = [desc[0] for desc in cursor.description]
        hub_data = dict(zip(columns, result))
        
        return {
            "success": True,
            "message": "Hub updated successfully",
            "data": hub_data
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/hubs/{hub_id}")
def admin_delete_hub(
    hub_id: int,
    current_user_id: int = Depends(get_current_user)
):
    """Delete a hub (admin only)"""
    check_admin_permission(current_user_id)
    
    conn = DBConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM cms_page_hubs WHERE id = %s RETURNING id", (hub_id,))
        result = cursor.fetchone()
        conn.commit()
        
        if not result:
            raise HTTPException(status_code=404, detail="Hub not found")
        
        return {
            "success": True,
            "message": "Hub deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
