-- ==========================================
-- 1. CLEANUP
-- ==========================================
DROP TABLE IF EXISTS public.NYC_Rolling_Sales CASCADE;

DROP TABLE IF EXISTS public.NYPD_Complaints CASCADE;

DROP TABLE IF EXISTS public.Airbnb_Listings CASCADE;

-- ==========================================
-- 2. SOURCE TABLES (Strictly Source Schema)
-- ==========================================
-- A. SALES DATA
CREATE TABLE
    public.NYC_Rolling_Sales (
        -- Keys
        sale_id BIGINT PRIMARY KEY, -- Generated in Pentaho (Add Sequence)
        borough_id BIGINT, -- Calculated in Pentaho (CRC32)
        neighborhood_id BIGINT, -- Calculated in Pentaho (CRC32)
        -- Attributes (From Source Schema)
        building_category TEXT,
        total_units INTEGER,
        gross_sqft INTEGER,
        year_built INTEGER,
        sale_price NUMERIC,
        sale_date DATE
    );

-- B. CRIME DATA
CREATE TABLE
    public.NYPD_Complaints (
        -- Keys
        complaint_id BIGINT PRIMARY KEY, -- From Source
        borough_id BIGINT, -- Calculated in Pentaho (CRC32)
        neighborhood_id BIGINT, -- Calculated in Pentaho (CRC32)
        -- Attributes (From Source Schema)
        complaint_timestamp TIMESTAMP, -- *ADDED* (Merged Date+Time to match Global Schema)
        offense_type TEXT,
        offense_level TEXT,
        offense_status TEXT,
        premise_type TEXT,
        premise_pos TEXT,
        victim_sex TEXT,
        victim_age_group TEXT,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION
    );

-- C. AIRBNB DATA
CREATE TABLE
    public.Airbnb_Listings (
        -- Keys
        listing_id BIGINT PRIMARY KEY, -- From Source
        borough_id BIGINT, -- Calculated in Pentaho (CRC32)
        neighborhood_id BIGINT, -- Calculated in Pentaho (CRC32)
        -- Attributes (From Source Schema)
        name TEXT,
        listing_date DATE,
        host_id BIGINT,
        host_since DATE,
        host_location TEXT,
        host_neighborhood TEXT,
        property_type TEXT,
        room_type TEXT,
        capacity INTEGER,
        square_feet DOUBLE PRECISION,
        daily_price NUMERIC,
        min_nights INTEGER,
        max_nights INTEGER,
        availability_year INTEGER,
        first_review_date DATE,
        last_review_date DATE,
        review_scores_rating INTEGER,
        location_score INTEGER,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION
    );