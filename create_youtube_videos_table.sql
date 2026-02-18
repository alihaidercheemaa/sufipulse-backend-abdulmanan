-- YouTube Videos Table Schema
-- This table stores cached YouTube video information for the SufiPulse channel

CREATE TABLE IF NOT EXISTS youtube_videos (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    writer VARCHAR(255),
    vocalist VARCHAR(255),
    thumbnail VARCHAR(500),
    views VARCHAR(50),
    duration VARCHAR(20),
    uploaded_at TIMESTAMP WITH TIME ZONE,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_youtube_videos_uploaded_at ON youtube_videos(uploaded_at DESC);
CREATE INDEX IF NOT EXISTS idx_youtube_videos_title ON youtube_videos(title);

-- Add comments for documentation
COMMENT ON TABLE youtube_videos IS 'Stores YouTube video information fetched from YouTube API';
COMMENT ON COLUMN youtube_videos.id IS 'YouTube video ID';
COMMENT ON COLUMN youtube_videos.title IS 'Video title';
COMMENT ON COLUMN youtube_videos.writer IS 'Writer/Creator name';
COMMENT ON COLUMN youtube_videos.vocalist IS 'Vocalist name';
COMMENT ON COLUMN youtube_videos.thumbnail IS 'Thumbnail image URL';
COMMENT ON COLUMN youtube_videos.views IS 'View count (formatted as K/M)';
COMMENT ON COLUMN youtube_videos.duration IS 'Video duration (MM:SS or H:MM:SS)';
COMMENT ON COLUMN youtube_videos.uploaded_at IS 'Video publication date';
COMMENT ON COLUMN youtube_videos.tags IS 'YouTube video tags';
