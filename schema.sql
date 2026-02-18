--
-- PostgreSQL database dump
--

\restrict 5ttVqsUbIbgqcnv9tMxPEgnEXWPHGatKDINVe5nZcaKSMtgB2Xg9dKbjv2C4bBE

-- Dumped from database version 16.11
-- Dumped by pg_dump version 16.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: get_all_cms_pages(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE OR REPLACE FUNCTION public.get_all_cms_pages() RETURNS TABLE(id integer, page_name character varying, page_title character varying, page_slug character varying, is_active boolean, updated_at timestamp without time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT cp.id, cp.page_name, cp.page_title, cp.page_slug, cp.is_active, cp.updated_at
    FROM cms_pages cp
    ORDER BY cp.page_name;
END;
$$;


ALTER FUNCTION public.get_all_cms_pages() OWNER TO postgres;

--
-- Name: get_cms_page_data(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE OR REPLACE FUNCTION public.get_cms_page_data(p_page_slug character varying) RETURNS TABLE(page_id integer, page_name character varying, page_title character varying, page_slug character varying, meta_description text, meta_keywords text, hero_title character varying, hero_subtitle text, hero_quote text, hero_quote_author character varying, stats jsonb, "values" jsonb, team jsonb, timeline jsonb, testimonials jsonb, sections jsonb, hubs jsonb)
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION public.get_cms_page_data(p_page_slug character varying) OWNER TO postgres;

--
-- Name: FUNCTION get_cms_page_data(p_page_slug character varying); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.get_cms_page_data(p_page_slug character varying) IS 'Retrieve complete page data including all sections, stats, team, timeline, values, testimonials, and hubs';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: blog_submissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.blog_submissions (
    id integer NOT NULL,
    title character varying(120) NOT NULL,
    excerpt text,
    featured_image_url text,
    content text NOT NULL,
    user_id integer,
    status character varying(50) DEFAULT 'draft'::character varying,
    admin_comments text,
    editor_notes text,
    scheduled_publish_date timestamp without time zone,
    seo_meta_title character varying(255),
    seo_meta_description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    category character varying(100),
    tags text[] DEFAULT '{}'::text[],
    language character varying(50),
    CONSTRAINT blog_submissions_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'review'::character varying, 'approved'::character varying, 'revision'::character varying, 'rejected'::character varying, 'posted'::character varying])::text[])))
);


ALTER TABLE public.blog_submissions OWNER TO postgres;

--
-- Name: blog_submissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.blog_submissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_submissions_id_seq OWNER TO postgres;

--
-- Name: blog_submissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.blog_submissions_id_seq OWNED BY public.blog_submissions.id;


--
-- Name: bloggers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.bloggers (
    id integer NOT NULL,
    user_id integer,
    author_name character varying(255),
    author_image_url text,
    short_bio text,
    location character varying(255),
    website_url text,
    social_links jsonb DEFAULT '{}'::jsonb,
    publish_pseudonym boolean DEFAULT false,
    original_work_confirmation boolean DEFAULT false,
    publishing_rights_granted boolean DEFAULT false,
    discourse_policy_agreed boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bloggers OWNER TO postgres;

--
-- Name: bloggers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.bloggers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bloggers_id_seq OWNER TO postgres;

--
-- Name: bloggers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bloggers_id_seq OWNED BY public.bloggers.id;


--
-- Name: cms_page_achievements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_achievements (
    id integer NOT NULL,
    page_id integer,
    category_name character varying(255) NOT NULL,
    achievement_items jsonb,
    category_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_achievements OWNER TO postgres;

--
-- Name: cms_page_achievements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_achievements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_achievements_id_seq OWNER TO postgres;

--
-- Name: cms_page_achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_achievements_id_seq OWNED BY public.cms_page_achievements.id;


--
-- Name: cms_page_hubs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_hubs (
    id integer NOT NULL,
    page_id integer,
    hub_title character varying(255) NOT NULL,
    hub_details text,
    hub_description text,
    hub_icon character varying(100),
    hub_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_hubs OWNER TO postgres;

--
-- Name: cms_page_hubs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_hubs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_hubs_id_seq OWNER TO postgres;

--
-- Name: cms_page_hubs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_hubs_id_seq OWNED BY public.cms_page_hubs.id;


--
-- Name: cms_page_section_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_section_items (
    id integer NOT NULL,
    section_id integer,
    item_title character varying(255) NOT NULL,
    item_subtitle character varying(255),
    item_description text,
    item_icon character varying(100),
    item_field character varying(100),
    item_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_section_items OWNER TO postgres;

--
-- Name: cms_page_section_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_section_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_section_items_id_seq OWNER TO postgres;

--
-- Name: cms_page_section_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_section_items_id_seq OWNED BY public.cms_page_section_items.id;


--
-- Name: cms_page_sections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_sections (
    id integer NOT NULL,
    page_id integer,
    section_name character varying(100) NOT NULL,
    section_type character varying(50) NOT NULL,
    section_title character varying(255),
    section_subtitle text,
    section_content text,
    section_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_sections OWNER TO postgres;

--
-- Name: cms_page_sections_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_sections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_sections_id_seq OWNER TO postgres;

--
-- Name: cms_page_sections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_sections_id_seq OWNED BY public.cms_page_sections.id;


--
-- Name: cms_page_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_stats (
    id integer NOT NULL,
    page_id integer,
    stat_number character varying(50) NOT NULL,
    stat_label character varying(100) NOT NULL,
    stat_description text,
    stat_icon character varying(100),
    stat_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_stats OWNER TO postgres;

--
-- Name: cms_page_stats_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_stats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_stats_id_seq OWNER TO postgres;

--
-- Name: cms_page_stats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_stats_id_seq OWNED BY public.cms_page_stats.id;


--
-- Name: cms_page_team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_team (
    id integer NOT NULL,
    page_id integer,
    member_name character varying(255) NOT NULL,
    member_role character varying(255),
    member_organization character varying(255),
    member_bio text,
    member_image_url text,
    is_featured boolean DEFAULT false,
    member_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_team OWNER TO postgres;

--
-- Name: cms_page_team_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_team_id_seq OWNER TO postgres;

--
-- Name: cms_page_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_team_id_seq OWNED BY public.cms_page_team.id;


--
-- Name: cms_page_testimonials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_testimonials (
    id integer NOT NULL,
    page_id integer,
    testimonial_name character varying(255) NOT NULL,
    testimonial_location character varying(255),
    testimonial_role character varying(255),
    testimonial_quote text NOT NULL,
    testimonial_image_url text,
    testimonial_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_testimonials OWNER TO postgres;

--
-- Name: cms_page_testimonials_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_testimonials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_testimonials_id_seq OWNER TO postgres;

--
-- Name: cms_page_testimonials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_testimonials_id_seq OWNED BY public.cms_page_testimonials.id;


--
-- Name: cms_page_timeline; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_timeline (
    id integer NOT NULL,
    page_id integer,
    timeline_year character varying(50) NOT NULL,
    timeline_title character varying(255) NOT NULL,
    timeline_description text,
    timeline_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_timeline OWNER TO postgres;

--
-- Name: cms_page_timeline_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_timeline_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_timeline_id_seq OWNER TO postgres;

--
-- Name: cms_page_timeline_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_timeline_id_seq OWNED BY public.cms_page_timeline.id;


--
-- Name: cms_page_values; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_page_values (
    id integer NOT NULL,
    page_id integer,
    value_title character varying(255) NOT NULL,
    value_description text,
    value_icon character varying(100),
    value_color character varying(50) DEFAULT 'emerald'::character varying,
    value_order integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_page_values OWNER TO postgres;

--
-- Name: cms_page_values_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_page_values_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_page_values_id_seq OWNER TO postgres;

--
-- Name: cms_page_values_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_page_values_id_seq OWNED BY public.cms_page_values.id;


--
-- Name: cms_pages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.cms_pages (
    id integer NOT NULL,
    page_name character varying(100) NOT NULL,
    page_title character varying(255) NOT NULL,
    page_slug character varying(100) NOT NULL,
    meta_description text,
    meta_keywords text,
    hero_title character varying(500),
    hero_subtitle text,
    hero_quote text,
    hero_quote_author character varying(255),
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.cms_pages OWNER TO postgres;

--
-- Name: cms_pages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.cms_pages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cms_pages_id_seq OWNER TO postgres;

--
-- Name: cms_pages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cms_pages_id_seq OWNED BY public.cms_pages.id;


--
-- Name: guest_posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.guest_posts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    date date NOT NULL,
    role text,
    city text,
    country text,
    status text DEFAULT 'pending'::text NOT NULL,
    category text,
    excerpt text,
    content text,
    tags text[],
    title text NOT NULL
);


ALTER TABLE public.guest_posts OWNER TO postgres;

--
-- Name: guest_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.guest_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.guest_posts_id_seq OWNER TO postgres;

--
-- Name: guest_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.guest_posts_id_seq OWNED BY public.guest_posts.id;


--
-- Name: kalam_submissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.kalam_submissions (
    id integer NOT NULL,
    kalam_id integer,
    status character varying(50) DEFAULT 'draft'::character varying,
    user_approval_status character varying(50) DEFAULT 'pending'::character varying,
    vocalist_approval_status character varying(50) DEFAULT 'pending'::character varying,
    admin_comments text,
    writer_comments text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT kalam_submissions_status_check CHECK (((status)::text = ANY ((ARRAY['draft'::character varying, 'submitted'::character varying, 'changes_requested'::character varying, 'admin_approved'::character varying, 'admin_rejected'::character varying, 'final_approved'::character varying, 'complete_approved'::character varying, 'posted'::character varying])::text[]))),
    CONSTRAINT kalam_submissions_user_approval_status_check CHECK (((user_approval_status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying])::text[]))),
    CONSTRAINT kalam_submissions_vocalist_approval_status_check CHECK (((vocalist_approval_status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying])::text[])))
);


ALTER TABLE public.kalam_submissions OWNER TO postgres;

--
-- Name: kalam_submissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.kalam_submissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kalam_submissions_id_seq OWNER TO postgres;

--
-- Name: kalam_submissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kalam_submissions_id_seq OWNED BY public.kalam_submissions.id;


--
-- Name: kalams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.kalams (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    language character varying(100),
    theme character varying(255),
    kalam_text text,
    description text,
    sufi_influence character varying(255),
    musical_preference character varying(255),
    youtube_link character varying(255),
    writer_id integer,
    vocalist_id integer,
    published_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.kalams OWNER TO postgres;

--
-- Name: kalams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.kalams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kalams_id_seq OWNER TO postgres;

--
-- Name: kalams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kalams_id_seq OWNED BY public.kalams.id;


--
-- Name: notification_reads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.notification_reads (
    id integer NOT NULL,
    notification_id integer,
    user_id integer,
    read_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.notification_reads OWNER TO postgres;

--
-- Name: notification_reads_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.notification_reads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notification_reads_id_seq OWNER TO postgres;

--
-- Name: notification_reads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_reads_id_seq OWNED BY public.notification_reads.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.notifications (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    message text NOT NULL,
    target_type character varying(50) NOT NULL,
    target_user_ids integer[] DEFAULT '{}'::integer[],
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT notifications_target_type_check CHECK (((target_type)::text = ANY ((ARRAY['all'::character varying, 'writers'::character varying, 'vocalists'::character varying, 'specific'::character varying])::text[])))
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: partnership_proposals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.partnership_proposals (
    id integer NOT NULL,
    full_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    organization_name character varying(255) NOT NULL,
    role_title character varying(255) NOT NULL,
    organization_type character varying(100),
    partnership_type character varying(100),
    website character varying(255),
    proposal_text text NOT NULL,
    proposed_timeline character varying(100),
    resources text,
    goals text,
    sacred_alignment boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.partnership_proposals OWNER TO postgres;

--
-- Name: partnership_proposals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.partnership_proposals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.partnership_proposals_id_seq OWNER TO postgres;

--
-- Name: partnership_proposals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.partnership_proposals_id_seq OWNED BY public.partnership_proposals.id;


--
-- Name: remote_recording_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.remote_recording_requests (
    id integer NOT NULL,
    vocalist_id integer,
    kalam_id integer,
    name character varying(255),
    email character varying(255),
    city character varying(100),
    country character varying(100),
    time_zone character varying(100),
    role character varying(100),
    project_type character varying(100),
    recording_equipment text,
    internet_speed character varying(100),
    preferred_software character varying(100),
    availability text,
    recording_experience text,
    technical_setup text,
    additional_details text,
    status character varying(50) DEFAULT 'pending'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT remote_recording_requests_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying, 'completed'::character varying])::text[])))
);


ALTER TABLE public.remote_recording_requests OWNER TO postgres;

--
-- Name: remote_recording_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.remote_recording_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.remote_recording_requests_id_seq OWNER TO postgres;

--
-- Name: remote_recording_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.remote_recording_requests_id_seq OWNED BY public.remote_recording_requests.id;


--
-- Name: remote_recording_requests_new; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.remote_recording_requests_new (
    id integer NOT NULL,
    vocalist_id integer,
    kalam_id integer,
    lyric_title character varying(255) NOT NULL,
    lyric_writer character varying(255),
    lyric_language character varying(100),
    lyric_category character varying(100),
    recording_environment character varying(100) NOT NULL,
    target_submission_date date NOT NULL,
    interpretation_notes text NOT NULL,
    sample_upload_url text,
    sample_file_type character varying(50),
    sample_file_size integer,
    original_recording_confirmed boolean DEFAULT false,
    remote_production_standards_agreed boolean DEFAULT false,
    status character varying(50) DEFAULT 'under_review'::character varying,
    admin_comments text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    blog_id integer,
    CONSTRAINT remote_recording_requests_new_recording_environment_check CHECK (((recording_environment)::text = ANY ((ARRAY['Professional Studio'::character varying, 'Condenser Mic Setup'::character varying, 'USB Microphone'::character varying, 'Mobile Setup'::character varying])::text[]))),
    CONSTRAINT remote_recording_requests_new_status_check CHECK (((status)::text = ANY ((ARRAY['under_review'::character varying, 'approved'::character varying, 'rejected'::character varying, 'completed'::character varying])::text[])))
);


ALTER TABLE public.remote_recording_requests_new OWNER TO postgres;

--
-- Name: TABLE remote_recording_requests_new; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.remote_recording_requests_new IS 'Stores remote recording requests from vocalists for approved lyrics';


--
-- Name: COLUMN remote_recording_requests_new.recording_environment; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.remote_recording_requests_new.recording_environment IS 'Environment options: Professional Studio, Condenser Mic Setup, USB Microphone, Mobile Setup';


--
-- Name: COLUMN remote_recording_requests_new.interpretation_notes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.remote_recording_requests_new.interpretation_notes IS 'Emotional tone, vocal layering plans, stylistic direction';


--
-- Name: COLUMN remote_recording_requests_new.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.remote_recording_requests_new.status IS 'Request status: under_review, approved, rejected, completed';


--
-- Name: remote_recording_requests_new_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.remote_recording_requests_new_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.remote_recording_requests_new_id_seq OWNER TO postgres;

--
-- Name: remote_recording_requests_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.remote_recording_requests_new_id_seq OWNED BY public.remote_recording_requests_new.id;


--
-- Name: special_recognitions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.special_recognitions (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    subtitle character varying(255),
    description text,
    achievement text
);


ALTER TABLE public.special_recognitions OWNER TO postgres;

--
-- Name: special_recognitions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.special_recognitions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.special_recognitions_id_seq OWNER TO postgres;

--
-- Name: special_recognitions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.special_recognitions_id_seq OWNED BY public.special_recognitions.id;


--
-- Name: studio_recording_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.studio_recording_requests (
    id integer NOT NULL,
    vocalist_id integer,
    kalam_id integer,
    lyric_title character varying(255) NOT NULL,
    lyric_writer character varying(255),
    lyric_language character varying(100),
    lyric_category character varying(100),
    preferred_session_date date NOT NULL,
    preferred_time_block character varying(50) NOT NULL,
    estimated_studio_duration character varying(50) NOT NULL,
    performance_direction text NOT NULL,
    reference_upload_url text,
    reference_file_type character varying(50),
    reference_file_size integer,
    availability_confirmed boolean DEFAULT false,
    studio_policies_agreed boolean DEFAULT false,
    status character varying(50) DEFAULT 'pending_review'::character varying,
    admin_comments text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    blog_id integer,
    CONSTRAINT studio_recording_requests_estimated_studio_duration_check CHECK (((estimated_studio_duration)::text = ANY ((ARRAY['1 Hour'::character varying, '2 Hours'::character varying, 'Half Day'::character varying, 'Full Day'::character varying])::text[]))),
    CONSTRAINT studio_recording_requests_preferred_time_block_check CHECK (((preferred_time_block)::text = ANY ((ARRAY['Morning'::character varying, 'Afternoon'::character varying, 'Evening'::character varying])::text[]))),
    CONSTRAINT studio_recording_requests_status_check CHECK (((status)::text = ANY ((ARRAY['pending_review'::character varying, 'approved'::character varying, 'rejected'::character varying, 'completed'::character varying])::text[])))
);


ALTER TABLE public.studio_recording_requests OWNER TO postgres;

--
-- Name: TABLE studio_recording_requests; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.studio_recording_requests IS 'Stores studio recording (in-person) requests from vocalists for approved lyrics';


--
-- Name: COLUMN studio_recording_requests.preferred_time_block; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.studio_recording_requests.preferred_time_block IS 'Time block options: Morning, Afternoon, Evening';


--
-- Name: COLUMN studio_recording_requests.estimated_studio_duration; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.studio_recording_requests.estimated_studio_duration IS 'Duration options: 1 Hour, 2 Hours, Half Day, Full Day';


--
-- Name: COLUMN studio_recording_requests.performance_direction; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.studio_recording_requests.performance_direction IS 'Tone, delivery style, tempo sensitivity, and vocal interpretation notes';


--
-- Name: COLUMN studio_recording_requests.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.studio_recording_requests.status IS 'Request status: pending_review, approved, rejected, completed';


--
-- Name: studio_recording_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.studio_recording_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.studio_recording_requests_id_seq OWNER TO postgres;

--
-- Name: studio_recording_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.studio_recording_requests_id_seq OWNED BY public.studio_recording_requests.id;


--
-- Name: studio_visit_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.studio_visit_requests (
    id integer NOT NULL,
    vocalist_id integer,
    kalam_id integer,
    name character varying(255),
    email character varying(255),
    organization character varying(255),
    contact_number character varying(50),
    preferred_date date,
    preferred_time character varying(50),
    purpose text,
    number_of_visitors integer,
    additional_details text,
    special_requests text,
    status character varying(50) DEFAULT 'pending'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT studio_visit_requests_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying, 'completed'::character varying])::text[])))
);


ALTER TABLE public.studio_visit_requests OWNER TO postgres;

--
-- Name: studio_visit_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.studio_visit_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.studio_visit_requests_id_seq OWNER TO postgres;

--
-- Name: studio_visit_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.studio_visit_requests_id_seq OWNED BY public.studio_visit_requests.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    password_hash text NOT NULL,
    permissions jsonb DEFAULT '{}'::jsonb,
    role character varying(50),
    country character varying(100),
    city character varying(100),
    is_registered boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    otp character varying(6),
    otp_expiry timestamp without time zone,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['writer'::character varying, 'vocalist'::character varying, 'blogger'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: videos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.videos (
    id text NOT NULL,
    title text,
    writer text,
    vocalist text,
    thumbnail text,
    views text,
    duration text
);


ALTER TABLE public.videos OWNER TO postgres;

--
-- Name: vocalists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.vocalists (
    id integer NOT NULL,
    user_id integer,
    vocal_range character varying(100),
    languages text[],
    sample_title character varying(255),
    audio_sample_url text,
    sample_description text,
    experience_background text,
    portfolio text,
    availability text,
    status character varying(50) DEFAULT 'pending'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT vocalists_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying])::text[])))
);


ALTER TABLE public.vocalists OWNER TO postgres;

--
-- Name: vocalists_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.vocalists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vocalists_id_seq OWNER TO postgres;

--
-- Name: vocalists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vocalists_id_seq OWNED BY public.vocalists.id;


--
-- Name: writers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.writers (
    id integer NOT NULL,
    user_id integer,
    writing_styles text[],
    languages text[],
    sample_title character varying(255),
    experience_background text,
    portfolio text,
    availability text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.writers OWNER TO postgres;

--
-- Name: writers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE IF NOT EXISTS public.writers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.writers_id_seq OWNER TO postgres;

--
-- Name: writers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.writers_id_seq OWNED BY public.writers.id;


--
-- Name: youtube_videos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE IF NOT EXISTS public.youtube_videos (
    id character varying(50) NOT NULL,
    title character varying(500) NOT NULL,
    writer character varying(255),
    vocalist character varying(255),
    thumbnail character varying(500),
    views character varying(50),
    duration character varying(20),
    uploaded_at timestamp with time zone,
    tags text[] DEFAULT '{}'::text[],
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.youtube_videos OWNER TO postgres;

--
-- Name: TABLE youtube_videos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.youtube_videos IS 'Stores YouTube video information fetched from YouTube API';


--
-- Name: COLUMN youtube_videos.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.id IS 'YouTube video ID';


--
-- Name: COLUMN youtube_videos.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.title IS 'Video title';


--
-- Name: COLUMN youtube_videos.writer; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.writer IS 'Writer/Creator name';


--
-- Name: COLUMN youtube_videos.vocalist; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.vocalist IS 'Vocalist name';


--
-- Name: COLUMN youtube_videos.thumbnail; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.thumbnail IS 'Thumbnail image URL';


--
-- Name: COLUMN youtube_videos.views; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.views IS 'View count (formatted as K/M)';


--
-- Name: COLUMN youtube_videos.duration; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.duration IS 'Video duration (MM:SS or H:MM:SS)';


--
-- Name: COLUMN youtube_videos.uploaded_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.uploaded_at IS 'Video publication date';


--
-- Name: COLUMN youtube_videos.tags; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.youtube_videos.tags IS 'YouTube video tags';


--
-- Name: blog_submissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_submissions ALTER COLUMN id SET DEFAULT nextval('public.blog_submissions_id_seq'::regclass);


--
-- Name: bloggers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloggers ALTER COLUMN id SET DEFAULT nextval('public.bloggers_id_seq'::regclass);


--
-- Name: cms_page_achievements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_achievements ALTER COLUMN id SET DEFAULT nextval('public.cms_page_achievements_id_seq'::regclass);


--
-- Name: cms_page_hubs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_hubs ALTER COLUMN id SET DEFAULT nextval('public.cms_page_hubs_id_seq'::regclass);


--
-- Name: cms_page_section_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_section_items ALTER COLUMN id SET DEFAULT nextval('public.cms_page_section_items_id_seq'::regclass);


--
-- Name: cms_page_sections id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_sections ALTER COLUMN id SET DEFAULT nextval('public.cms_page_sections_id_seq'::regclass);


--
-- Name: cms_page_stats id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_stats ALTER COLUMN id SET DEFAULT nextval('public.cms_page_stats_id_seq'::regclass);


--
-- Name: cms_page_team id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_team ALTER COLUMN id SET DEFAULT nextval('public.cms_page_team_id_seq'::regclass);


--
-- Name: cms_page_testimonials id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_testimonials ALTER COLUMN id SET DEFAULT nextval('public.cms_page_testimonials_id_seq'::regclass);


--
-- Name: cms_page_timeline id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_timeline ALTER COLUMN id SET DEFAULT nextval('public.cms_page_timeline_id_seq'::regclass);


--
-- Name: cms_page_values id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_values ALTER COLUMN id SET DEFAULT nextval('public.cms_page_values_id_seq'::regclass);


--
-- Name: cms_pages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_pages ALTER COLUMN id SET DEFAULT nextval('public.cms_pages_id_seq'::regclass);


--
-- Name: guest_posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guest_posts ALTER COLUMN id SET DEFAULT nextval('public.guest_posts_id_seq'::regclass);


--
-- Name: kalam_submissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kalam_submissions ALTER COLUMN id SET DEFAULT nextval('public.kalam_submissions_id_seq'::regclass);


--
-- Name: kalams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kalams ALTER COLUMN id SET DEFAULT nextval('public.kalams_id_seq'::regclass);


--
-- Name: notification_reads id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_reads ALTER COLUMN id SET DEFAULT nextval('public.notification_reads_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: partnership_proposals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partnership_proposals ALTER COLUMN id SET DEFAULT nextval('public.partnership_proposals_id_seq'::regclass);


--
-- Name: remote_recording_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests ALTER COLUMN id SET DEFAULT nextval('public.remote_recording_requests_id_seq'::regclass);


--
-- Name: remote_recording_requests_new id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests_new ALTER COLUMN id SET DEFAULT nextval('public.remote_recording_requests_new_id_seq'::regclass);


--
-- Name: special_recognitions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.special_recognitions ALTER COLUMN id SET DEFAULT nextval('public.special_recognitions_id_seq'::regclass);


--
-- Name: studio_recording_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_recording_requests ALTER COLUMN id SET DEFAULT nextval('public.studio_recording_requests_id_seq'::regclass);


--
-- Name: studio_visit_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_visit_requests ALTER COLUMN id SET DEFAULT nextval('public.studio_visit_requests_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: vocalists id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vocalists ALTER COLUMN id SET DEFAULT nextval('public.vocalists_id_seq'::regclass);


--
-- Name: writers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.writers ALTER COLUMN id SET DEFAULT nextval('public.writers_id_seq'::regclass);


--
-- Name: blog_submissions blog_submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_submissions
    ADD CONSTRAINT blog_submissions_pkey PRIMARY KEY (id);


--
-- Name: bloggers bloggers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloggers
    ADD CONSTRAINT bloggers_pkey PRIMARY KEY (id);


--
-- Name: bloggers bloggers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloggers
    ADD CONSTRAINT bloggers_user_id_key UNIQUE (user_id);


--
-- Name: cms_page_achievements cms_page_achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_achievements
    ADD CONSTRAINT cms_page_achievements_pkey PRIMARY KEY (id);


--
-- Name: cms_page_hubs cms_page_hubs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_hubs
    ADD CONSTRAINT cms_page_hubs_pkey PRIMARY KEY (id);


--
-- Name: cms_page_section_items cms_page_section_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_section_items
    ADD CONSTRAINT cms_page_section_items_pkey PRIMARY KEY (id);


--
-- Name: cms_page_sections cms_page_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_sections
    ADD CONSTRAINT cms_page_sections_pkey PRIMARY KEY (id);


--
-- Name: cms_page_stats cms_page_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_stats
    ADD CONSTRAINT cms_page_stats_pkey PRIMARY KEY (id);


--
-- Name: cms_page_team cms_page_team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_team
    ADD CONSTRAINT cms_page_team_pkey PRIMARY KEY (id);


--
-- Name: cms_page_testimonials cms_page_testimonials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_testimonials
    ADD CONSTRAINT cms_page_testimonials_pkey PRIMARY KEY (id);


--
-- Name: cms_page_timeline cms_page_timeline_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_timeline
    ADD CONSTRAINT cms_page_timeline_pkey PRIMARY KEY (id);


--
-- Name: cms_page_values cms_page_values_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_values
    ADD CONSTRAINT cms_page_values_pkey PRIMARY KEY (id);


--
-- Name: cms_pages cms_pages_page_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_pages
    ADD CONSTRAINT cms_pages_page_name_key UNIQUE (page_name);


--
-- Name: cms_pages cms_pages_page_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_pages
    ADD CONSTRAINT cms_pages_page_slug_key UNIQUE (page_slug);


--
-- Name: cms_pages cms_pages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_pages
    ADD CONSTRAINT cms_pages_pkey PRIMARY KEY (id);


--
-- Name: guest_posts guest_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guest_posts
    ADD CONSTRAINT guest_posts_pkey PRIMARY KEY (id);


--
-- Name: kalam_submissions kalam_submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kalam_submissions
    ADD CONSTRAINT kalam_submissions_pkey PRIMARY KEY (id);


--
-- Name: kalams kalams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kalams
    ADD CONSTRAINT kalams_pkey PRIMARY KEY (id);


--
-- Name: notification_reads notification_reads_notification_id_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_reads
    ADD CONSTRAINT notification_reads_notification_id_user_id_key UNIQUE (notification_id, user_id);


--
-- Name: notification_reads notification_reads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_reads
    ADD CONSTRAINT notification_reads_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: partnership_proposals partnership_proposals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partnership_proposals
    ADD CONSTRAINT partnership_proposals_pkey PRIMARY KEY (id);


--
-- Name: remote_recording_requests_new remote_recording_requests_new_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests_new
    ADD CONSTRAINT remote_recording_requests_new_pkey PRIMARY KEY (id);


--
-- Name: remote_recording_requests_new remote_recording_requests_new_vocalist_id_kalam_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests_new
    ADD CONSTRAINT remote_recording_requests_new_vocalist_id_kalam_id_key UNIQUE (vocalist_id, kalam_id);


--
-- Name: remote_recording_requests remote_recording_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests
    ADD CONSTRAINT remote_recording_requests_pkey PRIMARY KEY (id);


--
-- Name: special_recognitions special_recognitions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.special_recognitions
    ADD CONSTRAINT special_recognitions_pkey PRIMARY KEY (id);


--
-- Name: studio_recording_requests studio_recording_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_recording_requests
    ADD CONSTRAINT studio_recording_requests_pkey PRIMARY KEY (id);


--
-- Name: studio_recording_requests studio_recording_requests_vocalist_id_kalam_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_recording_requests
    ADD CONSTRAINT studio_recording_requests_vocalist_id_kalam_id_key UNIQUE (vocalist_id, kalam_id);


--
-- Name: studio_visit_requests studio_visit_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_visit_requests
    ADD CONSTRAINT studio_visit_requests_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: videos videos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.videos
    ADD CONSTRAINT videos_pkey PRIMARY KEY (id);


--
-- Name: vocalists vocalists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vocalists
    ADD CONSTRAINT vocalists_pkey PRIMARY KEY (id);


--
-- Name: vocalists vocalists_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vocalists
    ADD CONSTRAINT vocalists_user_id_key UNIQUE (user_id);


--
-- Name: writers writers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.writers
    ADD CONSTRAINT writers_pkey PRIMARY KEY (id);


--
-- Name: writers writers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.writers
    ADD CONSTRAINT writers_user_id_key UNIQUE (user_id);


--
-- Name: youtube_videos youtube_videos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.youtube_videos
    ADD CONSTRAINT youtube_videos_pkey PRIMARY KEY (id);


--
-- Name: idx_blog_submissions_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_blog_submissions_category ON public.blog_submissions USING btree (category);


--
-- Name: idx_blog_submissions_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_blog_submissions_created_at ON public.blog_submissions USING btree (created_at);


--
-- Name: idx_blog_submissions_language; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_blog_submissions_language ON public.blog_submissions USING btree (language);


--
-- Name: idx_blog_submissions_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_blog_submissions_status ON public.blog_submissions USING btree (status);


--
-- Name: idx_blog_submissions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_blog_submissions_user_id ON public.blog_submissions USING btree (user_id);


--
-- Name: idx_bloggers_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_bloggers_created_at ON public.bloggers USING btree (created_at);


--
-- Name: idx_bloggers_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_bloggers_user_id ON public.bloggers USING btree (user_id);


--
-- Name: idx_cms_page_achievements_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_achievements_page_id ON public.cms_page_achievements USING btree (page_id);


--
-- Name: idx_cms_page_hubs_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_hubs_page_id ON public.cms_page_hubs USING btree (page_id);


--
-- Name: idx_cms_page_section_items_section_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_section_items_section_id ON public.cms_page_section_items USING btree (section_id);


--
-- Name: idx_cms_page_sections_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_sections_page_id ON public.cms_page_sections USING btree (page_id);


--
-- Name: idx_cms_page_stats_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_stats_page_id ON public.cms_page_stats USING btree (page_id);


--
-- Name: idx_cms_page_team_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_team_page_id ON public.cms_page_team USING btree (page_id);


--
-- Name: idx_cms_page_testimonials_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_testimonials_page_id ON public.cms_page_testimonials USING btree (page_id);


--
-- Name: idx_cms_page_timeline_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_timeline_page_id ON public.cms_page_timeline USING btree (page_id);


--
-- Name: idx_cms_page_values_page_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_page_values_page_id ON public.cms_page_values USING btree (page_id);


--
-- Name: idx_cms_pages_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_cms_pages_slug ON public.cms_pages USING btree (page_slug);


--
-- Name: idx_remote_recording_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_created_at ON public.remote_recording_requests USING btree (created_at);


--
-- Name: idx_remote_recording_kalam_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_kalam_id ON public.remote_recording_requests USING btree (kalam_id);


--
-- Name: idx_remote_recording_new_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_new_created_at ON public.remote_recording_requests_new USING btree (created_at);


--
-- Name: idx_remote_recording_new_kalam_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_new_kalam_id ON public.remote_recording_requests_new USING btree (kalam_id);


--
-- Name: idx_remote_recording_new_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_new_status ON public.remote_recording_requests_new USING btree (status);


--
-- Name: idx_remote_recording_new_vocalist_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_new_vocalist_id ON public.remote_recording_requests_new USING btree (vocalist_id);


--
-- Name: idx_remote_recording_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_status ON public.remote_recording_requests USING btree (status);


--
-- Name: idx_remote_recording_vocalist_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_remote_recording_vocalist_id ON public.remote_recording_requests USING btree (vocalist_id);


--
-- Name: idx_studio_recording_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_recording_created_at ON public.studio_recording_requests USING btree (created_at);


--
-- Name: idx_studio_recording_kalam_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_recording_kalam_id ON public.studio_recording_requests USING btree (kalam_id);


--
-- Name: idx_studio_recording_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_recording_status ON public.studio_recording_requests USING btree (status);


--
-- Name: idx_studio_recording_vocalist_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_recording_vocalist_id ON public.studio_recording_requests USING btree (vocalist_id);


--
-- Name: idx_studio_visit_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_visit_created_at ON public.studio_visit_requests USING btree (created_at);


--
-- Name: idx_studio_visit_kalam_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_visit_kalam_id ON public.studio_visit_requests USING btree (kalam_id);


--
-- Name: idx_studio_visit_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_visit_status ON public.studio_visit_requests USING btree (status);


--
-- Name: idx_studio_visit_vocalist_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_studio_visit_vocalist_id ON public.studio_visit_requests USING btree (vocalist_id);


--
-- Name: idx_users_country_city; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_users_country_city ON public.users USING btree (country, city);


--
-- Name: idx_users_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_users_created_at ON public.users USING btree (created_at);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_users_email ON public.users USING btree (email);


--
-- Name: idx_users_role; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_users_role ON public.users USING btree (role);


--
-- Name: idx_vocalists_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_vocalists_created_at ON public.vocalists USING btree (created_at);


--
-- Name: idx_vocalists_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_vocalists_status ON public.vocalists USING btree (status);


--
-- Name: idx_vocalists_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_vocalists_user_id ON public.vocalists USING btree (user_id);


--
-- Name: idx_writer_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_writer_user_id ON public.writers USING btree (user_id);


--
-- Name: idx_youtube_videos_title; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_youtube_videos_title ON public.youtube_videos USING btree (title);


--
-- Name: idx_youtube_videos_uploaded_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX IF NOT EXISTS idx_youtube_videos_uploaded_at ON public.youtube_videos USING btree (uploaded_at DESC);


--
-- Name: blog_submissions blog_submissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_submissions
    ADD CONSTRAINT blog_submissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: bloggers bloggers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bloggers
    ADD CONSTRAINT bloggers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: cms_page_achievements cms_page_achievements_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_achievements
    ADD CONSTRAINT cms_page_achievements_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: cms_page_hubs cms_page_hubs_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_hubs
    ADD CONSTRAINT cms_page_hubs_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: cms_page_section_items cms_page_section_items_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_section_items
    ADD CONSTRAINT cms_page_section_items_section_id_fkey FOREIGN KEY (section_id) REFERENCES public.cms_page_sections(id) ON DELETE CASCADE;


--
-- Name: cms_page_sections cms_page_sections_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_sections
    ADD CONSTRAINT cms_page_sections_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: cms_page_stats cms_page_stats_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_stats
    ADD CONSTRAINT cms_page_stats_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: cms_page_team cms_page_team_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_team
    ADD CONSTRAINT cms_page_team_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: cms_page_testimonials cms_page_testimonials_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_testimonials
    ADD CONSTRAINT cms_page_testimonials_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: cms_page_timeline cms_page_timeline_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_timeline
    ADD CONSTRAINT cms_page_timeline_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: cms_page_values cms_page_values_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_page_values
    ADD CONSTRAINT cms_page_values_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.cms_pages(id) ON DELETE CASCADE;


--
-- Name: kalam_submissions kalam_submissions_kalam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kalam_submissions
    ADD CONSTRAINT kalam_submissions_kalam_id_fkey FOREIGN KEY (kalam_id) REFERENCES public.kalams(id) ON DELETE CASCADE;


--
-- Name: kalams kalams_vocalist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kalams
    ADD CONSTRAINT kalams_vocalist_id_fkey FOREIGN KEY (vocalist_id) REFERENCES public.vocalists(id);


--
-- Name: kalams kalams_writer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kalams
    ADD CONSTRAINT kalams_writer_id_fkey FOREIGN KEY (writer_id) REFERENCES public.users(id);


--
-- Name: notification_reads notification_reads_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_reads
    ADD CONSTRAINT notification_reads_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.notifications(id) ON DELETE CASCADE;


--
-- Name: notification_reads notification_reads_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_reads
    ADD CONSTRAINT notification_reads_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: remote_recording_requests remote_recording_requests_kalam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests
    ADD CONSTRAINT remote_recording_requests_kalam_id_fkey FOREIGN KEY (kalam_id) REFERENCES public.kalams(id) ON DELETE CASCADE;


--
-- Name: remote_recording_requests_new remote_recording_requests_new_blog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests_new
    ADD CONSTRAINT remote_recording_requests_new_blog_id_fkey FOREIGN KEY (blog_id) REFERENCES public.blog_submissions(id) ON DELETE CASCADE;


--
-- Name: remote_recording_requests_new remote_recording_requests_new_vocalist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests_new
    ADD CONSTRAINT remote_recording_requests_new_vocalist_id_fkey FOREIGN KEY (vocalist_id) REFERENCES public.vocalists(id) ON DELETE CASCADE;


--
-- Name: remote_recording_requests remote_recording_requests_vocalist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.remote_recording_requests
    ADD CONSTRAINT remote_recording_requests_vocalist_id_fkey FOREIGN KEY (vocalist_id) REFERENCES public.vocalists(id) ON DELETE CASCADE;


--
-- Name: studio_recording_requests studio_recording_requests_blog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_recording_requests
    ADD CONSTRAINT studio_recording_requests_blog_id_fkey FOREIGN KEY (blog_id) REFERENCES public.blog_submissions(id) ON DELETE CASCADE;


--
-- Name: studio_recording_requests studio_recording_requests_vocalist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_recording_requests
    ADD CONSTRAINT studio_recording_requests_vocalist_id_fkey FOREIGN KEY (vocalist_id) REFERENCES public.vocalists(id) ON DELETE CASCADE;


--
-- Name: studio_visit_requests studio_visit_requests_kalam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_visit_requests
    ADD CONSTRAINT studio_visit_requests_kalam_id_fkey FOREIGN KEY (kalam_id) REFERENCES public.kalams(id) ON DELETE CASCADE;


--
-- Name: studio_visit_requests studio_visit_requests_vocalist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studio_visit_requests
    ADD CONSTRAINT studio_visit_requests_vocalist_id_fkey FOREIGN KEY (vocalist_id) REFERENCES public.vocalists(id) ON DELETE CASCADE;


--
-- Name: vocalists vocalists_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vocalists
    ADD CONSTRAINT vocalists_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: writers writers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.writers
    ADD CONSTRAINT writers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 5ttVqsUbIbgqcnv9tMxPEgnEXWPHGatKDINVe5nZcaKSMtgB2Xg9dKbjv2C4bBE

