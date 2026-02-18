-- ========================================
-- NEW RECORDING REQUEST TABLES FOR VOCALIST
-- ========================================
-- These tables support the two new recording request forms:
-- 1. Studio Recording Request (In-Person)
-- 2. Remote Recording Request
-- ========================================

-- ========================================
-- STUDIO RECORDING REQUESTS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS studio_recording_requests (
    id SERIAL PRIMARY KEY,
    vocalist_id INT REFERENCES vocalists(id) ON DELETE CASCADE,
    kalam_id INT REFERENCES kalams(id) ON DELETE CASCADE,
    
    -- Lyric Selection (stored for reference)
    lyric_title VARCHAR(255) NOT NULL,
    lyric_writer VARCHAR(255),
    lyric_language VARCHAR(100),
    lyric_category VARCHAR(100),
    
    -- Session Scheduling
    preferred_session_date DATE NOT NULL,
    preferred_time_block VARCHAR(50) NOT NULL CHECK (preferred_time_block IN ('Morning', 'Afternoon', 'Evening')),
    estimated_studio_duration VARCHAR(50) NOT NULL CHECK (estimated_studio_duration IN ('1 Hour', '2 Hours', 'Half Day', 'Full Day')),
    
    -- Artistic Preparation
    performance_direction TEXT NOT NULL,
    reference_upload_url TEXT,
    reference_file_type VARCHAR(50),
    reference_file_size INT,
    
    -- Confirmation
    availability_confirmed BOOLEAN DEFAULT FALSE,
    studio_policies_agreed BOOLEAN DEFAULT FALSE,
    
    -- Status Tracking
    status VARCHAR(50) CHECK (status IN ('pending_review', 'approved', 'rejected', 'completed')) DEFAULT 'pending_review',
    admin_comments TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure unique request per vocalist per kalam
    UNIQUE(vocalist_id, kalam_id)
);

-- Indexes for Studio Recording Requests
CREATE INDEX IF NOT EXISTS idx_studio_recording_vocalist_id ON studio_recording_requests(vocalist_id);
CREATE INDEX IF NOT EXISTS idx_studio_recording_kalam_id ON studio_recording_requests(kalam_id);
CREATE INDEX IF NOT EXISTS idx_studio_recording_status ON studio_recording_requests(status);
CREATE INDEX IF NOT EXISTS idx_studio_recording_created_at ON studio_recording_requests(created_at);

-- ========================================
-- REMOTE RECORDING REQUESTS TABLE
-- ========================================
CREATE TABLE IF NOT EXISTS remote_recording_requests_new (
    id SERIAL PRIMARY KEY,
    vocalist_id INT REFERENCES vocalists(id) ON DELETE CASCADE,
    kalam_id INT REFERENCES kalams(id) ON DELETE CASCADE,
    
    -- Lyric Selection (stored for reference)
    lyric_title VARCHAR(255) NOT NULL,
    lyric_writer VARCHAR(255),
    lyric_language VARCHAR(100),
    lyric_category VARCHAR(100),
    
    -- Technical Setup
    recording_environment VARCHAR(100) NOT NULL CHECK (recording_environment IN ('Professional Studio', 'Condenser Mic Setup', 'USB Microphone', 'Mobile Setup')),
    target_submission_date DATE NOT NULL,
    
    -- Performance Plan
    interpretation_notes TEXT NOT NULL,
    sample_upload_url TEXT,
    sample_file_type VARCHAR(50),
    sample_file_size INT,
    
    -- Professional Declaration
    original_recording_confirmed BOOLEAN DEFAULT FALSE,
    remote_production_standards_agreed BOOLEAN DEFAULT FALSE,
    
    -- Status Tracking
    status VARCHAR(50) CHECK (status IN ('under_review', 'approved', 'rejected', 'completed')) DEFAULT 'under_review',
    admin_comments TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure unique request per vocalist per kalam
    UNIQUE(vocalist_id, kalam_id)
);

-- Indexes for Remote Recording Requests
CREATE INDEX IF NOT EXISTS idx_remote_recording_new_vocalist_id ON remote_recording_requests_new(vocalist_id);
CREATE INDEX IF NOT EXISTS idx_remote_recording_new_kalam_id ON remote_recording_requests_new(kalam_id);
CREATE INDEX IF NOT EXISTS idx_remote_recording_new_status ON remote_recording_requests_new(status);
CREATE INDEX IF NOT EXISTS idx_remote_recording_new_created_at ON remote_recording_requests_new(created_at);

-- ========================================
-- HELPER FUNCTIONS
-- ========================================

-- Function to get approved and unassigned kalams for vocalist
CREATE OR REPLACE FUNCTION get_approved_unassigned_kalams()
RETURNS TABLE (
    id INT,
    title VARCHAR,
    language VARCHAR,
    theme VARCHAR,
    kalam_text TEXT,
    description TEXT,
    writer_name VARCHAR,
    status VARCHAR,
    vocalist_approval_status VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        k.id,
        k.title,
        k.language,
        k.theme,
        k.kalam_text,
        k.description,
        u.name AS writer_name,
        ks.status,
        ks.vocalist_approval_status
    FROM kalams k
    JOIN users u ON k.writer_id = u.id
    LEFT JOIN kalam_submissions ks ON ks.kalam_id = k.id
    WHERE k.vocalist_id IS NULL 
      AND (ks.status = 'complete_approved' OR ks.status = 'final_approved')
      AND ks.vocalist_approval_status = 'approved'
    ORDER BY k.created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to update lyric status after request approval
CREATE OR REPLACE FUNCTION update_lyric_status_on_request_approval(
    p_kalam_id INT,
    p_vocalist_id INT
)
RETURNS VOID AS $$
BEGIN
    -- Update kalam to assign vocalist
    UPDATE kalams 
    SET vocalist_id = p_vocalist_id, 
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_kalam_id;
    
    -- Update kalam submission status
    UPDATE kalam_submissions
    SET status = 'complete_approved',
        updated_at = CURRENT_TIMESTAMP
    WHERE kalam_id = p_kalam_id;
END;
$$ LANGUAGE plpgsql;

-- ========================================
-- COMMENTS FOR DOCUMENTATION
-- ========================================
COMMENT ON TABLE studio_recording_requests IS 'Stores studio recording (in-person) requests from vocalists for approved lyrics';
COMMENT ON TABLE remote_recording_requests_new IS 'Stores remote recording requests from vocalists for approved lyrics';

COMMENT ON COLUMN studio_recording_requests.preferred_time_block IS 'Time block options: Morning, Afternoon, Evening';
COMMENT ON COLUMN studio_recording_requests.estimated_studio_duration IS 'Duration options: 1 Hour, 2 Hours, Half Day, Full Day';
COMMENT ON COLUMN studio_recording_requests.performance_direction IS 'Tone, delivery style, tempo sensitivity, and vocal interpretation notes';
COMMENT ON COLUMN studio_recording_requests.status IS 'Request status: pending_review, approved, rejected, completed';

COMMENT ON COLUMN remote_recording_requests_new.recording_environment IS 'Environment options: Professional Studio, Condenser Mic Setup, USB Microphone, Mobile Setup';
COMMENT ON COLUMN remote_recording_requests_new.interpretation_notes IS 'Emotional tone, vocal layering plans, stylistic direction';
COMMENT ON COLUMN remote_recording_requests_new.status IS 'Request status: under_review, approved, rejected, completed';
