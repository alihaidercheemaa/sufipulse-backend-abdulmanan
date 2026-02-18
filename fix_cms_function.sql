-- Drop and recreate get_cms_page_data function with fixed table aliases
DROP FUNCTION IF EXISTS get_cms_page_data(VARCHAR);

-- Then recreate it by running the full schema
\i sql/cms_pages_schema.sql
