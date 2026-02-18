-- =========================
-- CMS PAGES MANAGEMENT SYSTEM
-- =========================

-- Main pages table for storing page metadata
CREATE TABLE cms_pages (
    id SERIAL PRIMARY KEY,
    page_name VARCHAR(100) UNIQUE NOT NULL,
    page_title VARCHAR(255) NOT NULL,
    page_slug VARCHAR(100) UNIQUE NOT NULL,
    meta_description TEXT,
    meta_keywords TEXT,
    hero_title VARCHAR(500),
    hero_subtitle TEXT,
    hero_quote TEXT,
    hero_quote_author VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Page stats (for statistics sections)
CREATE TABLE cms_page_stats (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    stat_number VARCHAR(50) NOT NULL,
    stat_label VARCHAR(100) NOT NULL,
    stat_description TEXT,
    stat_icon VARCHAR(100),
    stat_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Page values/principles/core values
CREATE TABLE cms_page_values (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    value_title VARCHAR(255) NOT NULL,
    value_description TEXT,
    value_icon VARCHAR(100),
    value_color VARCHAR(50) DEFAULT 'emerald',
    value_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Team members (for founders, team sections)
CREATE TABLE cms_page_team (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    member_name VARCHAR(255) NOT NULL,
    member_role VARCHAR(255),
    member_organization VARCHAR(255),
    member_bio TEXT,
    member_image_url TEXT,
    is_featured BOOLEAN DEFAULT FALSE,
    member_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Timeline/milestones
CREATE TABLE cms_page_timeline (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    timeline_year VARCHAR(50) NOT NULL,
    timeline_title VARCHAR(255) NOT NULL,
    timeline_description TEXT,
    timeline_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Testimonials/quotes
CREATE TABLE cms_page_testimonials (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    testimonial_name VARCHAR(255) NOT NULL,
    testimonial_location VARCHAR(255),
    testimonial_role VARCHAR(255),
    testimonial_quote TEXT NOT NULL,
    testimonial_image_url TEXT,
    testimonial_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Page sections (for custom content sections)
CREATE TABLE cms_page_sections (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    section_name VARCHAR(100) NOT NULL,
    section_type VARCHAR(50) NOT NULL,
    section_title VARCHAR(255),
    section_subtitle TEXT,
    section_content TEXT,
    section_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Page section items (for items within sections like roles, expertise, etc.)
CREATE TABLE cms_page_section_items (
    id SERIAL PRIMARY KEY,
    section_id INT REFERENCES cms_page_sections(id) ON DELETE CASCADE,
    item_title VARCHAR(255) NOT NULL,
    item_subtitle VARCHAR(255),
    item_description TEXT,
    item_icon VARCHAR(100),
    item_field VARCHAR(100),
    item_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Achievement categories and items
CREATE TABLE cms_page_achievements (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    category_name VARCHAR(255) NOT NULL,
    achievement_items JSONB,
    category_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contact/Global hubs
CREATE TABLE cms_page_hubs (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES cms_pages(id) ON DELETE CASCADE,
    hub_title VARCHAR(255) NOT NULL,
    hub_details TEXT,
    hub_description TEXT,
    hub_icon VARCHAR(100),
    hub_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_cms_pages_slug ON cms_pages(page_slug);
CREATE INDEX idx_cms_page_stats_page_id ON cms_page_stats(page_id);
CREATE INDEX idx_cms_page_values_page_id ON cms_page_values(page_id);
CREATE INDEX idx_cms_page_team_page_id ON cms_page_team(page_id);
CREATE INDEX idx_cms_page_timeline_page_id ON cms_page_timeline(page_id);
CREATE INDEX idx_cms_page_testimonials_page_id ON cms_page_testimonials(page_id);
CREATE INDEX idx_cms_page_sections_page_id ON cms_page_sections(page_id);
CREATE INDEX idx_cms_page_section_items_section_id ON cms_page_section_items(section_id);
CREATE INDEX idx_cms_page_achievements_page_id ON cms_page_achievements(page_id);
CREATE INDEX idx_cms_page_hubs_page_id ON cms_page_hubs(page_id);

-- =========================
-- SEED DATA FOR EXISTING PAGES
-- =========================

-- Home Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, hero_title, hero_subtitle, hero_quote, hero_quote_author)
VALUES (
    'Home', 
    'SufiPulse - Global Sufi Music Platform', 
    'home',
    'SufiPulse is a global platform for Sufi music collaboration, connecting writers and vocalists worldwide to create sacred kalam.',
    'sufi music, kalam, spiritual music, qawwali, sufism, global platform',
    'Global Sufi Collaboration Studio',
    'From Kashmir''s sacred valleys to the global ummah submit your Sufi kalam. Let the world hear its pulse.',
    'We don''t sell divine lyrics. We amplify them.',
    'SufiPulse Promise'
);

-- Home Page Stats
INSERT INTO cms_page_stats (page_id, stat_number, stat_label, stat_description, stat_icon, stat_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'home'), '300+', 'Sacred Collaborations', 'Divine kalam brought to life', 'Heart', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'home'), '43+', 'Countries Represented', 'Global spiritual community', 'Globe', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'home'), '150+', 'Divine Kalam Created', 'Sacred productions', 'Music', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'home'), '100%', 'Free for Writers', 'No cost ever', 'Award', 4);

-- Home Page Testimonials (sample - can add more)
INSERT INTO cms_page_testimonials (page_id, testimonial_name, testimonial_location, testimonial_role, testimonial_quote, testimonial_image_url, testimonial_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'home'), 'Amina Rahman', 'Delhi, India', 'Sufi Writer', 
    'SufiPulse turned my kalam into a global spiritual experience with exceptional production quality.',
    'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=200', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'home'), 'Omar Ali', 'London, UK', 'Sufi Devotee', 
    'SufiPulse evokes the warmth of zikr circles, deepening my spiritual connection.',
    '/pics/38-min.png', 2);

-- About Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, hero_title, hero_subtitle)
VALUES (
    'About', 
    'About SufiPulse - Our Story', 
    'about',
    'Learn about SufiPulse mission to preserve and promote Sufi music through global collaboration.',
    'about sufiPulse, our mission, sufi music platform, spiritual collaboration',
    'Our Sacred Mission',
    'Serving the divine through the preservation, production, and global sharing of sacred Sufi kalam'
);

-- About Page Values
INSERT INTO cms_page_values (page_id, value_title, value_description, value_icon, value_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), 'Spiritual Integrity', 
    'Every project is approached with deep reverence for the sacred nature of Sufi poetry and spiritual expression.',
    'Heart', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), 'Global Unity', 
    'Bridging cultures and languages through the universal language of divine love and spiritual awakening.',
    'Globe', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), 'Non-Commercial Service', 
    'We serve the sacred, not profit. All our services are provided freely to uplift the spiritual community.',
    'Shield', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), 'Excellence in Craft', 
    'Combining technical mastery with spiritual sensitivity to create productions worthy of the divine message.',
    'Award', 4);

-- About Page Team
INSERT INTO cms_page_team (page_id, member_name, member_role, member_organization, member_bio, member_image_url, is_featured, member_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), 'Dr. Zarf-e-Noori', 'Founder & Visionary', 'SufiPulse Global',
    'Kashmiri-American visionary bridging ancient Sufi wisdom with modern innovation. Writer, Lyricist, Composer, and Creative Director.',
    'https://images.pexels.com/photos/1587927/pexels-photo-1587927.jpeg?auto=compress&cs=tinysrgb&w=200', TRUE, 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), 'Dr. Amara Kumar', 'Spiritual Director', 'Dr. Kumar Foundation',
    'Renowned scholar of comparative mysticism and founder of the Dr. Kumar Foundation, dedicated to preserving spiritual wisdom.',
    'https://images.pexels.com/photos/1181519/pexels-photo-1181519.jpeg?auto=compress&cs=tinysrgb&w=200', FALSE, 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), 'Prof. Hassan Al-Sufi', 'Academic Advisor', 'Sufi Science Center USA',
    'Leading authority on Sufi literature and Islamic spirituality, bringing decades of scholarly research to our mission.',
    'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=200', FALSE, 3);

-- About Page Timeline
INSERT INTO cms_page_timeline (page_id, timeline_year, timeline_title, timeline_description, timeline_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '2022', 'Vision Conceived', 
    'Dr. Zarf-e-Noori envisions a global platform for Sufi collaboration, inspired by Kashmir''s mystical heritage', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '2023', 'Foundation Established', 
    'SufiPulse launched as a joint initiative of Dr. Kumar Foundation and Sufi Science Center USA', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '2024', 'Global Expansion', 
    'Connected writers and vocalists from 50+ countries for sacred kalam productions', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '2024', 'Studio Development', 
    'Established world-class recording facilities with specialized acoustic treatment for spiritual music', 4),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '2025', 'Digital Platform Launch', 
    'Launched comprehensive online platform for global Sufi collaboration and sharing', 5);

-- About Page Stats
INSERT INTO cms_page_stats (page_id, stat_number, stat_label, stat_description, stat_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '300+', 'Sacred Collaborations', 'Divine kalam brought to life', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '89', 'Writers', 'From 50+ countries', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '43', 'Vocalists', 'Diverse spiritual voices', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '25+', 'Languages', 'Bridging cultural divides', 4),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '127K+', 'Global Views', 'Hearts touched worldwide', 5),
    ((SELECT id FROM cms_pages WHERE page_slug = 'about'), '100%', 'Free Service', 'No cost to writers ever', 6);

-- Our Mission Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, hero_title, hero_subtitle, hero_quote)
VALUES (
    'Our Mission', 
    'Our Mission - SufiPulse Vision', 
    'our-mission',
    'Discover the three sacred vows that guide SufiPulse in serving the divine word through music.',
    'sufiPulse mission, vision, spiritual service, sufi music preservation',
    'Our Mission',
    'Our mission is rooted in three sacred vows',
    'Our mission is rooted in three sacred vows'
);

-- Our Mission Page Values (Sacred Vows)
INSERT INTO cms_page_values (page_id, value_title, value_description, value_icon, value_color, value_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'our-mission'), 'To Serve the Divine Word', 
    'We do not monetize, modify, or exploit kalam. We protect its essence and amplify its reach.',
    'Heart', 'emerald', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'our-mission'), 'Unity Through Sound', 
    'From Kashmir to Los Angeles, from Cairo to Kuala Lumpur we believe every soul carrying divine lyrics deserves a global stage.',
    'Globe', 'emerald', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'our-mission'), 'To Produce With Purity', 
    'No marketing agenda. No monetization. No fame game. Just sincere production powered by sincerity, silence, and surrender.',
    'Shield', 'emerald', 3);

-- Our Mission Page Stats
INSERT INTO cms_page_stats (page_id, stat_number, stat_label, stat_description, stat_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'our-mission'), '300+', 'Writers', 'Global contributors', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'our-mission'), '43', 'Vocalists', 'Sacred voices', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'our-mission'), '300+', 'Collaborations', 'Divine productions', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'our-mission'), '100%', 'Free Service', 'No cost to writers ever', 4);

-- Who We Are Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, hero_title, hero_subtitle, hero_quote)
VALUES (
    'Who We Are', 
    'Who We Are - SufiPulse Team', 
    'who-we-are',
    'Meet the visionaries and organizations behind SufiPulse global initiative.',
    'sufiPulse team, founders, organizations, sufi music leaders',
    'Who We Are',
    'SufiPulse is a spiritually-driven, non-commercial Sufi music production platform',
    'We are not a label. We are a legacy.'
);

-- Who We Are Page Values
INSERT INTO cms_page_values (page_id, value_title, value_description, value_icon, value_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'who-we-are'), 'Serve the Divine Word', 
    'We do not monetize, modify, or exploit kalam. We protect its essence and amplify its reach.',
    'Heart', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'who-we-are'), 'Unite Ummah via Sound', 
    'From Kashmir to Los Angeles, from Cairo to Kuala Lumpur every soul carrying divine lyrics deserves a global stage.',
    'Globe', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'who-we-are'), 'Produce With Purity', 
    'No marketing agenda. No monetization. No fame game. Just sincere production powered by sincerity, silence, and surrender.',
    'Shield', 3);

-- Who We Are Page Stats
INSERT INTO cms_page_stats (page_id, stat_number, stat_label, stat_description, stat_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'who-we-are'), '300+', 'Sacred Collaborations', 'Divine kalam brought to life', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'who-we-are'), '89+', 'Writers', 'From 50+ countries', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'who-we-are'), '43+', 'Vocalists', 'Diverse spiritual voices', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'who-we-are'), '100%', 'Free Service', 'No cost to writers ever', 4);

-- Founder Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, hero_title, hero_subtitle)
VALUES (
    'Founder', 
    'Dr. Zarf-e-Noori - SufiPulse Founder', 
    'founder',
    'Learn about Dr. Zarf-e-Noori, the visionary founder of SufiPulse Global.',
    'Dr. Zarf-e-Noori, sufiPulse founder, sufi music visionary, kashmiri lyricist',
    'Dr. Zarf-e-Noori',
    'Founder & Visionary of SufiPulse - Bridging the sacred valleys of Kashmir with the global spiritual community'
);

-- Founder Page - Creative Roles (using section_items)
INSERT INTO cms_page_sections (page_id, section_name, section_type, section_title, section_subtitle, section_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'founder'), 'Creative Roles', 'roles', 
    'Creative Leadership', 'Dr. Zarf-e-Noori''s multifaceted creative roles in shaping SufiPulse''s artistic vision', 1);

INSERT INTO cms_page_section_items (section_id, item_title, item_description, item_icon, item_order)
VALUES 
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Creative Roles'), 'Writer', 
    'Crafting sacred Sufi poetry with deep spiritual insight', 'PenTool', 1),
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Creative Roles'), 'Lyricist', 
    'Creating divine verses that resonate with the soul', 'Music', 2),
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Creative Roles'), 'Composer', 
    'Harmonizing words with melodies for spiritual elevation', 'Mic', 3),
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Creative Roles'), 'Creative Director', 
    'Guiding SufiPulse''s artistic vision and mission', 'Users', 4);

-- Founder Page - Professional Expertise
INSERT INTO cms_page_sections (page_id, section_name, section_type, section_title, section_subtitle, section_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'founder'), 'Professional Expertise', 'expertise', 
    'Professional Expertise', 'A unique blend of technical expertise and entrepreneurial vision supporting the spiritual mission', 2);

INSERT INTO cms_page_section_items (section_id, item_title, item_subtitle, item_icon, item_field, item_order)
VALUES 
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Professional Expertise'), 'Remote Sensing Interpreter', 
    'Geospatial Analysis', 'Satellite', 'field', 1),
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Professional Expertise'), 'Environmental Scientist', 
    'Ecological Research', 'Leaf', 'field', 2),
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Professional Expertise'), 'Emergency Planner', 
    'Crisis Management', 'Shield', 'field', 3),
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Professional Expertise'), 'SaaS Developer', 
    'Technology Solutions', 'Code', 'field', 4),
    ((SELECT id FROM cms_page_sections WHERE section_name = 'Professional Expertise'), 'Entrepreneur', 
    'Business Innovation', 'Building', 'field', 5);

-- Founder Page - Quotes
INSERT INTO cms_page_testimonials (page_id, testimonial_name, testimonial_role, testimonial_quote, testimonial_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'founder'), 'Dr. Zarf-e-Noori', 'Core Philosophy', 
    'We don''t sell divine lyrics. We amplify them.', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'founder'), 'Dr. Zarf-e-Noori', 'On Innovation', 
    'Technology should serve the sacred, not the other way around.', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'founder'), 'Dr. Zarf-e-Noori', 'Mission Statement', 
    'From Kashmir''s valleys to the world''s heart - every soul deserves to hear the divine pulse.', 3);

-- Contact Page - Global Hubs
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, hero_title, hero_subtitle, hero_quote)
VALUES (
    'Contact', 
    'Contact SufiPulse - Connect With Us', 
    'contact',
    'Get in touch with SufiPulse for writer submissions, vocalist applications, or partnership inquiries.',
    'contact sufiPulse, submit kalam, join vocalist pool, partnership',
    'Connect With Our Sacred Community',
    'Ready to share your divine Sufi kalam or collaborate with our global spiritual community?',
    'Every connection is a bridge between hearts seeking the Divine'
);

-- Contact Page Hubs
INSERT INTO cms_page_hubs (page_id, hub_title, hub_details, hub_description, hub_icon, hub_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'contact'), 'Global Creative Hub', 
    'SufiPulse Studio, Virginia, USA', 'Our main creative center', 'MapPin', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'contact'), 'Spiritual Heritage Hub', 
    'SufiPulse – Kashmir, Srinagar, Jammu & Kashmir, India', 'Rooted in spiritual tradition', 'MapPin', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'contact'), 'Remote Vocalist Recording Hubs', 
    'Srinagar, Kashmir – India
Dubai – UAE
Mumbai – India
Istanbul – Turkey', 'Global recording facilities', 'Music', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'contact'), 'Email Us', 
    'connect@sufipulse.com', 'Connect with us globally', 'Mail', 4);

-- Gallery Page
INSERT INTO cms_pages (page_name, page_title, page_slug, meta_description, meta_keywords, hero_title, hero_subtitle)
VALUES (
    'Gallery', 
    'Gallery - Sacred Kalam Videos', 
    'gallery',
    'Watch our collection of sacred Sufi kalam videos from our global community of writers and vocalists.',
    'sufi videos, kalam gallery, sufi music, spiritual songs, qawwali videos',
    'Sacred Kalam Gallery',
    'Experience the divine fusion of sacred poetry and spiritual voices'
);

-- Gallery Page Stats
INSERT INTO cms_page_stats (page_id, stat_number, stat_label, stat_description, stat_icon, stat_order)
VALUES 
    ((SELECT id FROM cms_pages WHERE page_slug = 'gallery'), '0', 'Sacred Videos', 'Our complete collection', 'Play', 1),
    ((SELECT id FROM cms_pages WHERE page_slug = 'gallery'), '17+', 'Languages', 'Multilingual content', 'Globe', 2),
    ((SELECT id FROM cms_pages WHERE page_slug = 'gallery'), '0K+', 'Total Views', 'Global reach', 'Eye', 3),
    ((SELECT id FROM cms_pages WHERE page_slug = 'gallery'), '43+', 'Countries Reached', 'Worldwide audience', 'Heart', 4);

-- =========================
-- HELPER FUNCTIONS
-- =========================

-- Function to get complete page data
CREATE OR REPLACE FUNCTION get_cms_page_data(p_page_slug VARCHAR)
RETURNS TABLE (
    page_id INT,
    page_name VARCHAR,
    page_title VARCHAR,
    page_slug VARCHAR,
    meta_description TEXT,
    meta_keywords TEXT,
    hero_title VARCHAR,
    hero_subtitle TEXT,
    hero_quote TEXT,
    hero_quote_author VARCHAR,
    stats JSONB,
    "values" JSONB,
    team JSONB,
    timeline JSONB,
    testimonials JSONB,
    sections JSONB,
    hubs JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        cp.id as page_id,
        cp.page_name,
        cp.page_title,
        cp.page_slug,
        cp.meta_description,
        cp.meta_keywords,
        cp.hero_title,
        cp.hero_subtitle,
        cp.hero_quote,
        cp.hero_quote_author,
        (
            SELECT COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        'stat_number', stat_number,
                        'stat_label', stat_label,
                        'stat_description', stat_description,
                        'stat_icon', stat_icon,
                        'stat_order', stat_order
                    ) ORDER BY stat_order
                ),
                '[]'::jsonb
            )
            FROM cms_page_stats cps_stats
            WHERE cps_stats.page_id = cp.id AND cps_stats.is_active = TRUE
        ) as stats,
        (
            SELECT COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        'value_title', value_title,
                        'value_description', value_description,
                        'value_icon', value_icon,
                        'value_color', value_color,
                        'value_order', value_order
                    ) ORDER BY value_order
                ),
                '[]'::jsonb
            )
            FROM cms_page_values cps_values
            WHERE cps_values.page_id = cp.id AND cps_values.is_active = TRUE
        ) as "values",
        (
            SELECT COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        'member_name', member_name,
                        'member_role', member_role,
                        'member_organization', member_organization,
                        'member_bio', member_bio,
                        'member_image_url', member_image_url,
                        'is_featured', is_featured,
                        'member_order', member_order
                    ) ORDER BY member_order
                ),
                '[]'::jsonb
            )
            FROM cms_page_team cps_team
            WHERE cps_team.page_id = cp.id AND cps_team.is_active = TRUE
        ) as team,
        (
            SELECT COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        'timeline_year', timeline_year,
                        'timeline_title', timeline_title,
                        'timeline_description', timeline_description,
                        'timeline_order', timeline_order
                    ) ORDER BY timeline_order
                ),
                '[]'::jsonb
            )
            FROM cms_page_timeline cps_timeline
            WHERE cps_timeline.page_id = cp.id AND cps_timeline.is_active = TRUE
        ) as timeline,
        (
            SELECT COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        'testimonial_name', testimonial_name,
                        'testimonial_location', testimonial_location,
                        'testimonial_role', testimonial_role,
                        'testimonial_quote', testimonial_quote,
                        'testimonial_image_url', testimonial_image_url,
                        'testimonial_order', testimonial_order
                    ) ORDER BY testimonial_order
                ),
                '[]'::jsonb
            )
            FROM cms_page_testimonials cps_testimonials
            WHERE cps_testimonials.page_id = cp.id AND cps_testimonials.is_active = TRUE
        ) as testimonials,
        (
            SELECT COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        'section_name', section_name,
                        'section_type', section_type,
                        'section_title', section_title,
                        'section_subtitle', section_subtitle,
                        'section_content', section_content,
                        'section_order', section_order,
                        'items', (
                            SELECT COALESCE(
                                jsonb_agg(
                                    jsonb_build_object(
                                        'item_title', item_title,
                                        'item_subtitle', item_subtitle,
                                        'item_description', item_description,
                                        'item_icon', item_icon,
                                        'item_field', item_field,
                                        'item_order', item_order
                                    ) ORDER BY item_order
                                ),
                                '[]'::jsonb
                            )
                            FROM cms_page_section_items
                            WHERE section_id = cps.id AND is_active = TRUE
                        )
                    ) ORDER BY section_order
                ),
                '[]'::jsonb
            )
            FROM cms_page_sections cps
            WHERE cps.page_id = cp.id AND cps.is_active = TRUE
        ) as sections,
        (
            SELECT COALESCE(
                jsonb_agg(
                    jsonb_build_object(
                        'hub_title', hub_title,
                        'hub_details', hub_details,
                        'hub_description', hub_description,
                        'hub_icon', hub_icon,
                        'hub_order', hub_order
                    ) ORDER BY hub_order
                ),
                '[]'::jsonb
            )
            FROM cms_page_hubs cps_hubs
            WHERE cps_hubs.page_id = cp.id AND cps_hubs.is_active = TRUE
        ) as hubs
    FROM cms_pages cp
    WHERE cp.page_slug = p_page_slug AND cp.is_active = TRUE;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_cms_page_data IS 'Retrieve complete page data including all sections, stats, team, timeline, values, testimonials, and hubs';

-- Function to get all pages list
CREATE OR REPLACE FUNCTION get_all_cms_pages()
RETURNS TABLE (
    id INT,
    page_name VARCHAR,
    page_title VARCHAR,
    page_slug VARCHAR,
    is_active BOOLEAN,
    updated_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT cp.id, cp.page_name, cp.page_title, cp.page_slug, cp.is_active, cp.updated_at
    FROM cms_pages cp
    ORDER BY cp.page_name;
END;
$$ LANGUAGE plpgsql;
