# Database Setup & Migration Guide

## Overview
This guide explains how to set up and migrate the SufiPulse backend database when changing to a new database environment.

---

## Prerequisites

1. **PostgreSQL Installation**
   - Ensure PostgreSQL is installed on your system
   - PostgreSQL client tools (`psql`, `pg_restore`) must be in your system PATH
   - Recommended: PostgreSQL 12 or higher

2. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Update the `DATABASE_URL` with your new database credentials

---

## Database Setup Options

### Option 1: Fresh Setup (Recommended for New Databases)

This creates a new database with schema from `schema.sql`.

```bash
python setup_complete_db.py
```

**What this does:**
1. Creates the database if it doesn't exist
2. Applies the complete schema from `schema.sql`
3. Attempts to import data from `sufipulse.dump` (optional)

---

### Option 2: Using Dump File (If Available)

If you have a compatible database dump file:

```bash
python setup_db.py
```

**What this does:**
1. Creates the database if it doesn't exist
2. Restores from `sufipulse.dump` using `pg_restore`
3. Falls back to `psql` if `pg_restore` fails

---

### Option 3: Manual Schema Application

For applying schema updates to an existing database:

```bash
python apply_schema_updates.py
```

**What this does:**
1. Connects to your existing database
2. Applies schema from `schema.sql`
3. Skips tables/columns that already exist

---

## Database Schema

### Core Tables

#### 1. **users**
User accounts and authentication
```sql
- id (SERIAL PRIMARY KEY)
- email (VARCHAR UNIQUE)
- name (VARCHAR)
- password_hash (TEXT)
- role (writer|vocalist|blogger|admin)
- country, city (VARCHAR)
- is_registered (BOOLEAN)
- permissions (JSONB)
- otp, otp_expiry (for verification)
- created_at, updated_at (TIMESTAMP)
```

#### 2. **vocalists**
Vocalist profiles
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INT, FK → users.id)
- vocal_range, languages, sample_title
- audio_sample_url, sample_description
- experience_background, portfolio, availability
- status (pending|approved|rejected)
- created_at, updated_at
```

#### 3. **writers**
Writer profiles
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INT, FK → users.id)
- writing_styles, languages, sample_title
- experience_background, portfolio, availability
- created_at, updated_at
```

#### 4. **bloggers**
Blogger profiles
```sql
- id (SERIAL PRIMARY KEY)
- user_id (INT, FK → users.id)
- author_name, author_image_url, short_bio
- location, website_url, social_links (JSONB)
- publish_pseudonym, original_work_confirmation
- publishing_rights_granted, discourse_policy_agreed
- created_at, updated_at
```

#### 5. **kalams**
Kalam (poetry/song) content
```sql
- id (SERIAL PRIMARY KEY)
- title, language, theme, kalam_text, description
- sufi_influence, musical_preference
- youtube_link
- writer_id (FK → users.id)
- vocalist_id (FK → vocalists.id)
- published_at, created_at, updated_at
```

#### 6. **kalam_submissions**
Kalam submission workflow
```sql
- id (SERIAL PRIMARY KEY)
- kalam_id (FK → kalams.id)
- status (draft|submitted|changes_requested|admin_approved|admin_rejected|final_approved|complete_approved|posted)
- user_approval_status, vocalist_approval_status
- admin_comments, writer_comments
- created_at, updated_at
```

#### 7. **blog_submissions**
Blog post submissions
```sql
- id (SERIAL PRIMARY KEY)
- title, excerpt, featured_image_url, content
- user_id (FK → users.id)
- status (pending|review|approved|revision|rejected|posted)
- category, tags, language
- admin_comments, editor_notes
- scheduled_publish_date
- seo_meta_title, seo_meta_description
- created_at, updated_at
```

#### 8. **studio_visit_requests**
Studio visit booking
```sql
- id (SERIAL PRIMARY KEY)
- vocalist_id (FK → vocalists.id)
- kalam_id (FK → kalams.id)
- name, email, organization, contact_number
- preferred_date, preferred_time, purpose
- number_of_visitors, additional_details, special_requests
- status (pending|approved|rejected|completed)
- created_at, updated_at
```

#### 9. **remote_recording_requests**
Remote recording sessions
```sql
- id (SERIAL PRIMARY KEY)
- vocalist_id (FK → vocalists.id)
- kalam_id (FK → kalams.id)
- name, email, city, country, time_zone
- role, project_type, recording_equipment
- internet_speed, preferred_software, availability
- recording_experience, technical_setup
- status (pending|approved|rejected|completed)
- created_at, updated_at
```

#### 10. **notifications**
System notifications
```sql
- id (SERIAL PRIMARY KEY)
- title, message
- target_type (all|writers|vocalists|bloggers|specific)
- target_user_ids (INT[])
- created_at
```

#### 11. **notification_reads**
Notification read tracking
```sql
- id (SERIAL PRIMARY KEY)
- notification_id (FK → notifications.id)
- user_id (FK → users.id)
- read_at
- UNIQUE(notification_id, user_id)
```

#### 12. **partnership_proposals**
Partnership inquiries
```sql
- id (SERIAL PRIMARY KEY)
- full_name, email, organization_name, role_title
- organization_type, partnership_type
- website, proposal_text
- proposed_timeline, resources, goals
- sacred_alignment (BOOLEAN)
- created_at
```

#### 13. **guest_posts**
Guest post management
```sql
- id (SERIAL PRIMARY KEY)
- user_id, date, role, city, country
- status, category, excerpt, content, tags
- title
```

#### 14. **videos**
Video content cache
```sql
- id (TEXT PRIMARY KEY)
- title, writer, vocalist, thumbnail
- views, duration
```

#### 15. **special_recognitions**
Special achievements
```sql
- id (SERIAL PRIMARY KEY)
- title, subtitle, description, achievement
```

---

## Step-by-Step Migration Process

### Step 1: Configure Environment

Create/update your `.env` file:

```env
DATABASE_URL=postgresql://username:password@host:port/database_name
JWT_SECRET=your_jwt_secret_here
GOOGLE_CLIENT_ID=your_google_client_id
RESEND_API_KEY=your_resend_api_key
FROM_EMAIL=your_from_email
YOUTUBE_API_KEY=your_youtube_api_key
```

### Step 2: Create Database

If your database doesn't exist yet, the setup scripts will create it automatically. Alternatively, create manually:

```bash
psql -h host -p port -U postgres
CREATE DATABASE database_name OWNER username;
\q
```

### Step 3: Apply Schema

Choose one of the setup methods from "Database Setup Options" above.

### Step 4: Verify Tables

```bash
psql -h host -p port -U username -d database_name
\dt
```

You should see all 15 tables listed.

### Step 5: Create Admin User (Optional)

Run the admin setup script:

```bash
python fix_admin_password.py
```

Default admin credentials:
- **Email:** admin@sufipulse.com
- **Password:** (set by script)

---

## Troubleshooting

### Connection Issues

**Error:** `could not connect to server`
- Ensure PostgreSQL is running
- Check host and port in `DATABASE_URL`
- Verify firewall settings

**Error:** `password authentication failed`
- Verify username and password in `DATABASE_URL`
- Check database user permissions

### Dump Restore Issues

**Error:** `pg_restore: error: version mismatch`
- PostgreSQL version incompatibility
- Use `setup_complete_db.py` instead (uses `schema.sql`)
- Or try: `python restore_with_compat.py`

**Error:** `command not found: pg_restore`
- Install PostgreSQL client tools
- Windows: Add PostgreSQL `bin` directory to PATH
- Linux: `sudo apt-get install postgresql-client`
- macOS: `brew install libpq`

### Schema Application Issues

**Error:** `relation already exists`
- Tables already exist in database
- Use `apply_schema_updates.py` which handles existing tables
- Or drop existing tables first (⚠️ destroys data)

---

## Database Indexes

The following indexes are created automatically for performance:

| Table | Index | Columns |
|-------|-------|---------|
| users | idx_users_email | email |
| users | idx_users_role | role |
| users | idx_users_country_city | country, city |
| users | idx_users_created_at | created_at |
| vocalists | idx_vocalists_user_id | user_id |
| vocalists | idx_vocalists_status | status |
| vocalists | idx_vocalists_created_at | created_at |
| writers | idx_writer_user_id | user_id |
| bloggers | idx_bloggers_user_id | user_id |
| bloggers | idx_bloggers_created_at | created_at |
| blog_submissions | idx_blog_submissions_user_id | user_id |
| blog_submissions | idx_blog_submissions_status | status |
| blog_submissions | idx_blog_submissions_category | category |
| blog_submissions | idx_blog_submissions_language | language |
| blog_submissions | idx_blog_submissions_created_at | created_at |
| studio_visit_requests | idx_studio_visit_vocalist_id | vocalist_id |
| studio_visit_requests | idx_studio_visit_kalam_id | kalam_id |
| studio_visit_requests | idx_studio_visit_status | status |
| studio_visit_requests | idx_studio_visit_created_at | created_at |
| remote_recording_requests | idx_remote_recording_vocalist_id | vocalist_id |
| remote_recording_requests | idx_remote_recording_kalam_id | kalam_id |
| remote_recording_requests | idx_remote_recording_status | status |
| remote_recording_requests | idx_remote_recording_created_at | created_at |

---

## Quick Reference Commands

### Test Database Connection
```bash
python -c "from db.connection import DBConnection; conn = DBConnection.get_db_connection(); print('Connected!')"
```

### View All Tables
```sql
\dt
```

### Describe Table Structure
```sql
\d users
\d vocalists
\d kalams
```

### Count Records in All Tables
```sql
SELECT 'users' as table_name, COUNT(*) FROM users
UNION ALL SELECT 'vocalists', COUNT(*) FROM vocalists
UNION ALL SELECT 'writers', COUNT(*) FROM writers
UNION ALL SELECT 'bloggers', COUNT(*) FROM bloggers
UNION ALL SELECT 'kalams', COUNT(*) FROM kalams
UNION ALL SELECT 'kalam_submissions', COUNT(*) FROM kalam_submissions
UNION ALL SELECT 'blog_submissions', COUNT(*) FROM blog_submissions
UNION ALL SELECT 'studio_visit_requests', COUNT(*) FROM studio_visit_requests
UNION ALL SELECT 'remote_recording_requests', COUNT(*) FROM remote_recording_requests
UNION ALL SELECT 'notifications', COUNT(*) FROM notifications
UNION ALL SELECT 'partnership_proposals', COUNT(*) FROM partnership_proposals
UNION ALL SELECT 'guest_posts', COUNT(*) FROM guest_posts
UNION ALL SELECT 'videos', COUNT(*) FROM videos
UNION ALL SELECT 'special_recognitions', COUNT(*) FROM special_recognitions;
```

### Backup Current Database
```bash
pg_dump -h host -p port -U username -d database_name -F c -f backup.dump
```

### Restore from Backup
```bash
pg_restore -h host -p port -U username -d database_name backup.dump
```

---

## Security Notes

- ⚠️ **Never commit `.env` file** to version control
- ⚠️ **Use strong passwords** for database users
- ⚠️ **Restrict database access** to necessary hosts only
- ⚠️ **Regular backups** are essential for production
- ⚠️ **Use environment variables** for all sensitive data

---

## Support Files

| File | Purpose |
|------|---------|
| `schema.sql` | Complete database schema definition |
| `setup_db.py` | Setup from dump file |
| `setup_complete_db.py` | Complete setup with schema + optional data |
| `fresh_setup.py` | Fresh database setup |
| `apply_schema_updates.py` | Apply schema to existing database |
| `restore_db.py` | Database restore utility |
| `restore_with_compat.py` | Restore with compatibility mode |
| `fix_admin_password.py` | Reset admin password |
| `sufipulse.dump` | Database dump file (if available) |

---

## Contact & Resources

- **Project:** SufiPulse Backend
- **Database:** PostgreSQL
- **ORM:** Raw SQL with psycopg2
- **Framework:** FastAPI

For issues, check the existing documentation files:
- `DB_SETUP_COMPLETE.md`
- `ADMIN_USER_SETUP.md`
- `DB_CONFIG_SUMMARY.md`
- `CONNECTION_FIXES_SUMMARY.md`
