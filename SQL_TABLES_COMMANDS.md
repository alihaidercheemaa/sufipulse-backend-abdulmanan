# SQL Commands for Database Setup

## Quick Setup Command

Run the complete schema with one command:

```bash
psql -h your_host -p your_port -U your_username -d your_database_name -f schema.sql
```

Or connect to database and run:

```bash
psql -h your_host -p your_port -U your_username -d your_database_name
\i schema.sql
```

---

## Individual Table Creation Commands

### 1. Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    permissions JSONB DEFAULT '{}'::jsonb,
    role VARCHAR(50) CHECK (role IN ('writer', 'vocalist', 'blogger', 'admin')),
    country VARCHAR(100),
    city VARCHAR(100),
    is_registered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    otp VARCHAR(6),
    otp_expiry TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_country_city ON users(country, city);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### 2. Vocalists Table

```sql
CREATE TABLE vocalists (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    vocal_range VARCHAR(100),
    languages TEXT[],
    sample_title VARCHAR(255),
    audio_sample_url TEXT,
    sample_description TEXT,
    experience_background TEXT,
    portfolio TEXT,
    availability TEXT,
    status VARCHAR(50) CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_vocalists_user_id ON vocalists(user_id);
CREATE INDEX idx_vocalists_status ON vocalists(status);
CREATE INDEX idx_vocalists_created_at ON vocalists(created_at);
```

### 3. Writers Table

```sql
CREATE TABLE writers (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    writing_styles TEXT[],
    languages TEXT[],
    sample_title VARCHAR(255),
    experience_background TEXT,
    portfolio TEXT,
    availability TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_writer_user_id ON writers(user_id);
```

### 4. Bloggers Table

```sql
CREATE TABLE bloggers (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    author_name VARCHAR(255),
    author_image_url TEXT,
    short_bio TEXT,
    location VARCHAR(255),
    website_url TEXT,
    social_links JSONB DEFAULT '{}'::jsonb,
    publish_pseudonym BOOLEAN DEFAULT FALSE,
    original_work_confirmation BOOLEAN DEFAULT FALSE,
    publishing_rights_granted BOOLEAN DEFAULT FALSE,
    discourse_policy_agreed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_bloggers_user_id ON bloggers(user_id);
CREATE INDEX idx_bloggers_created_at ON bloggers(created_at);
```

### 5. Kalams Table

```sql
CREATE TABLE kalams (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    language VARCHAR(100),
    theme VARCHAR(255),
    kalam_text TEXT,
    description TEXT,
    sufi_influence VARCHAR(255),
    musical_preference VARCHAR(255),
    youtube_link VARCHAR(255),
    writer_id INT REFERENCES users(id),
    vocalist_id INT REFERENCES vocalists(id),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Kalam Submissions Table

```sql
CREATE TABLE kalam_submissions (
    id SERIAL PRIMARY KEY,
    kalam_id INT REFERENCES kalams(id) ON DELETE CASCADE,
    status VARCHAR(50) CHECK (
        status IN (
            'draft',
            'submitted',
            'changes_requested',
            'admin_approved',
            'admin_rejected',
            'final_approved',
            'complete_approved',
            'posted'
        )
    ) DEFAULT 'draft',
    user_approval_status VARCHAR(50) CHECK (
        user_approval_status IN ('pending','approved','rejected')
    ) DEFAULT 'pending',
    vocalist_approval_status VARCHAR(50) CHECK (
        vocalist_approval_status IN ('pending','approved','rejected')
    ) DEFAULT 'pending',
    admin_comments TEXT,
    writer_comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. Blog Submissions Table

```sql
CREATE TABLE blog_submissions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    excerpt TEXT,
    featured_image_url TEXT,
    content TEXT NOT NULL,
    user_id INT REFERENCES users(id),
    status VARCHAR(50) CHECK (
        status IN (
            'pending',
            'review',
            'approved',
            'revision',
            'rejected',
            'posted'
        )
    ) DEFAULT 'pending',
    category VARCHAR(100),
    tags TEXT[],
    language VARCHAR(50),
    admin_comments TEXT,
    editor_notes TEXT,
    scheduled_publish_date TIMESTAMP,
    seo_meta_title VARCHAR(255),
    seo_meta_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_blog_submissions_user_id ON blog_submissions(user_id);
CREATE INDEX idx_blog_submissions_status ON blog_submissions(status);
CREATE INDEX idx_blog_submissions_category ON blog_submissions(category);
CREATE INDEX idx_blog_submissions_language ON blog_submissions(language);
CREATE INDEX idx_blog_submissions_created_at ON blog_submissions(created_at);
```

### 8. Studio Visit Requests Table

```sql
CREATE TABLE studio_visit_requests (
    id SERIAL PRIMARY KEY,
    vocalist_id INT REFERENCES vocalists(id) ON DELETE CASCADE,
    kalam_id INT REFERENCES kalams(id) ON DELETE CASCADE,
    name VARCHAR(255),
    email VARCHAR(255),
    organization VARCHAR(255),
    contact_number VARCHAR(50),
    preferred_date DATE,
    preferred_time VARCHAR(50),
    purpose TEXT,
    number_of_visitors INT,
    additional_details TEXT,
    special_requests TEXT,
    status VARCHAR(50) CHECK (status IN ('pending', 'approved', 'rejected', 'completed')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_studio_visit_vocalist_id ON studio_visit_requests(vocalist_id);
CREATE INDEX idx_studio_visit_kalam_id ON studio_visit_requests(kalam_id);
CREATE INDEX idx_studio_visit_status ON studio_visit_requests(status);
CREATE INDEX idx_studio_visit_created_at ON studio_visit_requests(created_at);
```

### 9. Remote Recording Requests Table

```sql
CREATE TABLE remote_recording_requests (
    id SERIAL PRIMARY KEY,
    vocalist_id INT REFERENCES vocalists(id) ON DELETE CASCADE,
    kalam_id INT REFERENCES kalams(id) ON DELETE CASCADE,
    name VARCHAR(255),
    email VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    time_zone VARCHAR(100),
    role VARCHAR(100),
    project_type VARCHAR(100),
    recording_equipment TEXT,
    internet_speed VARCHAR(100),
    preferred_software VARCHAR(100),
    availability TEXT,
    recording_experience TEXT,
    technical_setup TEXT,
    additional_details TEXT,
    status VARCHAR(50) CHECK (status IN ('pending', 'approved', 'rejected', 'completed')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_remote_recording_vocalist_id ON remote_recording_requests(vocalist_id);
CREATE INDEX idx_remote_recording_kalam_id ON remote_recording_requests(kalam_id);
CREATE INDEX idx_remote_recording_status ON remote_recording_requests(status);
CREATE INDEX idx_remote_recording_created_at ON remote_recording_requests(created_at);
```

### 10. Notifications Table

```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    target_type VARCHAR(50) NOT NULL CHECK (
        target_type IN ('all', 'writers', 'vocalists', 'bloggers', 'specific')
    ),
    target_user_ids INT[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 11. Notification Reads Table

```sql
CREATE TABLE notification_reads (
    id SERIAL PRIMARY KEY,
    notification_id INT REFERENCES notifications(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(notification_id, user_id)
);
```

### 12. Partnership Proposals Table

```sql
CREATE TABLE partnership_proposals (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) NOT NULL,
    role_title VARCHAR(255) NOT NULL,
    organization_type VARCHAR(100),
    partnership_type VARCHAR(100),
    website VARCHAR(255),
    proposal_text TEXT NOT NULL,
    proposed_timeline VARCHAR(100),
    resources TEXT,
    goals TEXT,
    sacred_alignment BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 13. Guest Posts Table

```sql
CREATE TABLE guest_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    role TEXT,
    city TEXT,
    country TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    category TEXT,
    excerpt TEXT,
    content TEXT,
    tags TEXT[],
    title TEXT NOT NULL
);
```

### 14. Videos Table

```sql
CREATE TABLE videos (
    id TEXT PRIMARY KEY,
    title TEXT,
    writer TEXT,
    vocalist TEXT,
    thumbnail TEXT,
    views TEXT,
    duration TEXT
);
```

### 15. Special Recognitions Table

```sql
CREATE TABLE special_recognitions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    description TEXT,
    achievement TEXT
);
```

---

## Essential Data Inserts

### Create Admin User

```sql
-- First, create the admin user
INSERT INTO users (email, name, password_hash, role, is_registered, permissions)
VALUES (
    'admin@sufipulse.com',
    'Admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu',  -- 'admin123' hashed with bcrypt
    'admin',
    TRUE,
    '{"can_manage_users": true, "can_manage_content": true, "can_manage_settings": true}'::jsonb
);
```

### Sample Default Data (Optional)

```sql
-- Sample Special Recognition
INSERT INTO special_recognitions (title, subtitle, description, achievement)
VALUES (
    'Founding Member',
    'Early Contributor',
    'Recognized for being an early contributor to the SufiPulse community',
    'Joined in the first year and contributed multiple kalams'
);
```

---

## Verification Commands

### Check All Tables Created

```sql
\dt

-- Expected output should show all 15 tables:
-- users
-- vocalists
-- writers
-- bloggers
-- kalams
-- kalam_submissions
-- blog_submissions
-- studio_visit_requests
-- remote_recording_requests
-- notifications
-- notification_reads
-- partnership_proposals
-- guest_posts
-- videos
-- special_recognitions
```

### Check All Indexes Created

```sql
SELECT tablename, indexname, indexdef 
FROM pg_indexes 
WHERE schemaname = 'public' 
ORDER BY tablename, indexname;
```

### Check Table Structure

```sql
-- For any table, use:
\d users
\d vocalists
\d kalams
-- etc.
```

### Check Foreign Key Constraints

```sql
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY';
```

---

## One-Command Full Setup

Copy this entire block and run in psql:

```sql
-- Connect to your database first:
-- \c your_database_name

-- Run all table creation commands
\i schema.sql

-- Verify tables
\dt

-- Create admin user (update password hash as needed)
INSERT INTO users (email, name, password_hash, role, is_registered, permissions)
VALUES (
    'admin@sufipulse.com',
    'Admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu',
    'admin',
    TRUE,
    '{"can_manage_users": true, "can_manage_content": true, "can_manage_settings": true}'::jsonb
) ON CONFLICT (email) DO NOTHING;
```

---

## Python Script Alternative

You can also use the provided Python scripts:

```bash
# Complete setup (recommended)
python setup_complete_db.py

# Or fresh setup
python fresh_setup.py

# Or apply schema updates only
python apply_schema_updates.py
```

These scripts will:
1. Create the database if it doesn't exist
2. Apply the schema from `schema.sql`
3. Create all tables and indexes
4. Optionally import data from dump file

---

## Common Issues & Solutions

### Table Already Exists Error

```sql
-- Drop table if exists and recreate
DROP TABLE IF EXISTS table_name CASCADE;
-- Then run CREATE TABLE again
```

### Foreign Key Constraint Fails

Make sure to create tables in this order:
1. users (no dependencies)
2. vocalists (depends on users)
3. writers (depends on users)
4. bloggers (depends on users)
5. kalams (depends on users, vocalists)
6. kalam_submissions (depends on kalams)
7. blog_submissions (depends on users)
8. studio_visit_requests (depends on vocalists, kalams)
9. remote_recording_requests (depends on vocalists, kalams)
10. notifications (no dependencies)
11. notification_reads (depends on notifications, users)
12. partnership_proposals (no dependencies)
13. guest_posts (depends on users)
14. videos (no dependencies)
15. special_recognitions (no dependencies)

### Permission Denied Error

```sql
-- Grant all privileges to your user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_username;
```
