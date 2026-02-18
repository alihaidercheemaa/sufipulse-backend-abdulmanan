-- =========================
-- ADD ALL 20 PAGES TO CMS
-- Run this AFTER cms_pages_schema.sql
-- =========================

-- 8. Acknowledgments Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Acknowledgments', 
    'Acknowledgments - SufiPulse', 
    'acknowledgments',
    'Acknowledging all contributors to the SufiPulse mission.',
    'acknowledgments, contributors, community, thanks',
    TRUE
);

-- 9. Ethical Policy Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Ethical Policy', 
    'Ethical Policy - SufiPulse', 
    'ethical-policy',
    'Our ethical guidelines and principles for serving the sacred.',
    'ethics, policy, guidelines, principles',
    TRUE
);

-- 10. How It Works Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'How It Works', 
    'How It Works - SufiPulse', 
    'how-it-works',
    'Learn how SufiPulse works from submission to publication.',
    'how it works, process, steps, guide',
    TRUE
);

-- 11. Partnership Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Partnership', 
    'Partnership - SufiPulse', 
    'partnership',
    'Partnership opportunities with SufiPulse.',
    'partnership, collaboration, alliance',
    TRUE
);

-- 12. Guest Blogs Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Guest Blogs', 
    'Guest Blogs - SufiPulse', 
    'guest-blogs',
    'Guest blog posts from our community.',
    'guest blogs, articles, community posts',
    TRUE
);

-- 13. Music Style Selection Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Music Style Selection', 
    'Music Style Selection - SufiPulse', 
    'music-style-selection',
    'Choose your musical style for kalam adaptation.',
    'music style, selection, musical styles',
    TRUE
);

-- 14. Kalam Library Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Kalam Library', 
    'Kalam Library - SufiPulse', 
    'kalam-library',
    'Browse our library of kalam.',
    'kalam library, browse kalam, kalam collection',
    TRUE
);

-- 15. Writer FAQs Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Writer FAQs', 
    'Writer FAQs - SufiPulse', 
    'writer-faqs',
    'Frequently asked questions for writers.',
    'writer faqs, FAQs, questions, answers',
    TRUE
);

-- 16. Studio Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Studio', 
    'Studio - SufiPulse', 
    'studio',
    'SufiPulse recording studio.',
    'studio, recording studio, sufi studio',
    TRUE
);

-- 17. Studio Engineers Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Studio Engineers', 
    'Studio Engineers - SufiPulse', 
    'studio-engineers',
    'Meet our studio engineering team.',
    'studio engineers, audio engineers, team',
    TRUE
);

-- 18. Sufi Science Center Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Sufi Science Center', 
    'Sufi Science Center - SufiPulse', 
    'sufi-science-center',
    'Sufi Science Center research and education.',
    'sufi science center, research, education',
    TRUE
);

-- 19. Sufi Music Theory Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Sufi Music Theory', 
    'Sufi Music Theory - SufiPulse', 
    'sufi-music-theory',
    'Learn about Sufi music theory.',
    'sufi music theory, music theory, sufi music',
    TRUE
);

-- 20. Vocalist How It Works Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, is_active)
VALUES (
    'Vocalist How It Works', 
    'Vocalist How It Works - SufiPulse', 
    'vocalist-how-it-works',
    'How the vocalist journey works.',
    'vocalist how it works, vocalist process, vocalist guide',
    TRUE
);

-- Verify all 20 pages
SELECT COUNT(*) as total_pages FROM cms_pages;
SELECT id, page_name, page_slug FROM cms_pages ORDER BY id;
