-- Update studio_recording_requests to support blogs
ALTER TABLE studio_recording_requests 
DROP CONSTRAINT IF EXISTS studio_recording_requests_kalam_id_fkey;

ALTER TABLE studio_recording_requests 
ADD COLUMN blog_id INT REFERENCES blog_submissions(id) ON DELETE CASCADE;

-- Update remote_recording_requests_new to support blogs
ALTER TABLE remote_recording_requests_new 
DROP CONSTRAINT IF EXISTS remote_recording_requests_new_kalam_id_fkey;

ALTER TABLE remote_recording_requests_new 
ADD COLUMN blog_id INT REFERENCES blog_submissions(id) ON DELETE CASCADE;

-- Make kalam_id nullable since we're using blogs now
ALTER TABLE studio_recording_requests 
ALTER COLUMN kalam_id DROP NOT NULL;

ALTER TABLE remote_recording_requests_new 
ALTER COLUMN kalam_id DROP NOT NULL;
