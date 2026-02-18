import json
from psycopg2.extras import RealDictCursor
from typing import List, Optional


class BloggerQueries:
    def __init__(self, conn):
        self.conn = conn

    def get_blogger_by_user_id(self, user_id: int):
        query = """
            SELECT
                b.*,
                u.country,
                u.city
            FROM bloggers b
            JOIN users u ON b.user_id = u.id
            WHERE b.user_id = %s;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (user_id,))
            return cur.fetchone()

    def create_blogger_profile(self, user_id, author_name, author_image_url, short_bio,
                               location, website_url, social_links, publish_pseudonym,
                               original_work_confirmation, publishing_rights_granted,
                               discourse_policy_agreed):
        query = """
        INSERT INTO bloggers (
            user_id, author_name, author_image_url, short_bio,
            location, website_url, social_links, publish_pseudonym,
            original_work_confirmation, publishing_rights_granted, discourse_policy_agreed
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING *;
        """
        # Convert social_links to JSON string if it's a dict
        social_links_json = json.dumps(social_links) if isinstance(social_links, dict) else json.dumps({})
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (
                user_id, author_name, author_image_url, short_bio,
                location, website_url, social_links_json, publish_pseudonym,
                original_work_confirmation, publishing_rights_granted, discourse_policy_agreed
            ))
            self.conn.commit()
            return cur.fetchone()

    def update_blogger_profile(self, user_id, author_name=None, author_image_url=None,
                               short_bio=None, location=None, website_url=None,
                               social_links=None, publish_pseudonym=None,
                               original_work_confirmation=None, publishing_rights_granted=None,
                               discourse_policy_agreed=None):
        fields = {
            "author_name": author_name,
            "author_image_url": author_image_url,
            "short_bio": short_bio,
            "location": location,
            "website_url": website_url,
            "social_links": social_links,
            "publish_pseudonym": publish_pseudonym,
            "original_work_confirmation": original_work_confirmation,
            "publishing_rights_granted": publishing_rights_granted,
            "discourse_policy_agreed": discourse_policy_agreed
        }

        set_clauses = []
        values = []

        for key, value in fields.items():
            if value is not None:
                set_clauses.append(f"{key} = %s")
                # Handle social_links which is a dict - convert to JSON string
                if key == "social_links" and isinstance(value, dict):
                    values.append(json.dumps(value))
                else:
                    values.append(value)

        if not set_clauses:
            return None  # Nothing to update

        set_clause_str = ", ".join(set_clauses) + ", updated_at = CURRENT_TIMESTAMP"
        values.append(user_id)

        query = f"""
            UPDATE bloggers
            SET {set_clause_str}
            WHERE user_id = %s
            RETURNING *;
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            self.conn.commit()
            return cur.fetchone()

    def is_blogger_registered(self, user_id: int):
        query = """
        SELECT b.id
        FROM bloggers b
        JOIN users u ON u.id = b.user_id
        WHERE b.user_id = %s AND u.role = 'blogger';
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (user_id,))
            return cur.fetchone()

    def create_blog_submission(self, title: str, excerpt: str, featured_image_url: str, content: str,
                               category: str, tags: List[str], language: str,
                               user_id: int, editor_notes: str = None, scheduled_publish_date = None,
                               seo_meta_title: str = None, seo_meta_description: str = None):
        query = """
        INSERT INTO blog_submissions (
            title, excerpt, featured_image_url, content, category, tags, language, user_id, status,
            editor_notes, scheduled_publish_date, seo_meta_title, seo_meta_description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, %s, %s, %s)
        RETURNING id;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (
                title, excerpt, featured_image_url, content, category, tags, language, user_id,
                editor_notes, scheduled_publish_date, seo_meta_title, seo_meta_description
            ))
            self.conn.commit()
            result = cur.fetchone()
            return result['id'] if result else None

    def get_blog_submissions_by_user_id(self, user_id: int):
        query = """
            SELECT *
            FROM blog_submissions
            WHERE user_id = %s
            ORDER BY created_at DESC;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (user_id,))
            return cur.fetchall()

    def get_blog_submission_by_id(self, blog_id: int):
        query = """
            SELECT *
            FROM blog_submissions
            WHERE id = %s;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (blog_id,))
            return cur.fetchone()

    def update_blog_submission_status(self, blog_id: int, status: str, admin_comments: str = None):
        query = """
            UPDATE blog_submissions
            SET status = %s, admin_comments = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (status, admin_comments, blog_id))
            self.conn.commit()
            return cur.fetchone()

    def update_blog_submission(self, blog_id: int, title: str = None, excerpt: str = None,
                              featured_image_url: str = None, content: str = None,
                              category: str = None, tags: List[str] = None, language: str = None,
                              editor_notes: str = None, scheduled_publish_date = None,
                              seo_meta_title: str = None, seo_meta_description: str = None):
        fields = {
            "title": title,
            "excerpt": excerpt,
            "featured_image_url": featured_image_url,
            "content": content,
            "category": category,
            "tags": tags,
            "language": language,
            "editor_notes": editor_notes,
            "scheduled_publish_date": scheduled_publish_date,
            "seo_meta_title": seo_meta_title,
            "seo_meta_description": seo_meta_description
        }

        set_clauses = []
        values = []

        for key, value in fields.items():
            if value is not None:
                set_clauses.append(f"{key} = %s")
                values.append(value)

        if not set_clauses:
            return None  # Nothing to update

        set_clause_str = ", ".join(set_clauses) + ", updated_at = CURRENT_TIMESTAMP"
        values.append(blog_id)

        query = f"""
            UPDATE blog_submissions
            SET {set_clause_str}
            WHERE id = %s
            RETURNING *;
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            self.conn.commit()
            return cur.fetchone()

    def fetch_blog_submissions(self, skip: int, limit: int) -> List[dict]:
        query = """
            SELECT
                bs.*,
                u.name AS user_name,
                u.email AS user_email
            FROM blog_submissions bs
            JOIN users u ON bs.user_id = u.id
            ORDER BY bs.created_at DESC
            OFFSET %s
            LIMIT %s;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (skip, limit))
            blogs = cur.fetchall()
            return blogs

    def get_blog_submissions_count(self) -> int:
        query = """
            SELECT COUNT(*) as count
            FROM blog_submissions;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            result = cur.fetchone()
            return result['count'] if result else 0

    def fetch_approved_blogs(self, skip: int = 0, limit: int = 6, category: str = None, search: str = None) -> List[dict]:
        query = """
            SELECT 
                bs.*,
                u.name AS author_name,
                u.email AS author_email,
                b.author_name AS blogger_name,
                b.author_image_url,
                b.short_bio
            FROM blog_submissions bs
            JOIN users u ON bs.user_id = u.id
            LEFT JOIN bloggers b ON bs.user_id = b.user_id
            WHERE bs.status IN ('approved', 'posted')
        """
        
        params = []
        
        if category:
            query += " AND LOWER(bs.category) = LOWER(%s)"
            params.append(category)
        
        if search:
            query += " AND (bs.title ILIKE %s OR bs.excerpt ILIKE %s OR bs.content ILIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        query += " ORDER BY bs.created_at DESC OFFSET %s LIMIT %s"
        params.extend([skip, limit])
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()