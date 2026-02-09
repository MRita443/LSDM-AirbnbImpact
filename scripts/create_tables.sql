-- ==========================================
-- 1. CLEANUP
-- ==========================================
DROP TABLE IF EXISTS public.NYC_Rolling_Sales CASCADE;
DROP TABLE IF EXISTS public.NYPD_Complaints CASCADE;
DROP TABLE IF EXISTS public.Airbnb_Listings CASCADE;
DROP TABLE IF EXISTS public.Airbnb_Hosts CASCADE;
DROP TABLE IF EXISTS public.Neighborhood CASCADE;
DROP TABLE IF EXISTS public.Borough CASCADE;

-- ==========================================
-- 2. TABLES 
-- ==========================================

-- A. REFERENCE TABLES (Create these first usually)
CREATE TABLE public.Borough (
    borough_id BIGINT PRIMARY KEY,       -- CRC32(Name)
    name TEXT
);

CREATE TABLE public.Neighborhood (
    neighborhood_id BIGINT PRIMARY KEY,  -- CRC32(Name)
    borough_id BIGINT,                   -- Link to Borough
    name TEXT
);

-- B. SALES DATA
CREATE TABLE public.NYC_Rolling_Sales (
    -- Keys
    sale_id BIGINT PRIMARY KEY,         -- Generated in Pentaho
    neighborhood_id BIGINT,             -- FK to Neighborhood
    
    -- Attributes
    building_category TEXT,
    total_units INTEGER,
    gross_sqft INTEGER,
    year_built INTEGER,
    sale_price NUMERIC,
    sale_date DATE
);

-- C. CRIME DATA
CREATE TABLE public.NYPD_Complaints (
    -- Keys
    complaint_id BIGINT PRIMARY KEY,    -- Source ID
    neighborhood_id BIGINT,             -- FK to Neighborhood
    
    -- Attributes
    complaint_timestamp TIMESTAMP,
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

-- D. AIRBNB HOSTS
CREATE TABLE public.Airbnb_Hosts (
    -- Keys
    host_id BIGINT PRIMARY KEY,
    neighborhood_id BIGINT,             -- Calculated in Pentaho (CRC32)
    
    -- Attributes
    name TEXT,
    account_created DATE,
    location TEXT,
    num_local_listings INTEGER
);

-- E. AIRBNB LISTINGS
CREATE TABLE public.Airbnb_Listings (
    -- Keys
    listing_id BIGINT PRIMARY KEY,
    host_id BIGINT,                     -- FK to Airbnb_Hosts
    neighborhood_id BIGINT,             -- FK to Neighborhood
    
    -- Attributes
    name TEXT,
    listing_date DATE,
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
    location_score INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- ==========================================
-- 3. ADD FOREIGN KEYS
-- ==========================================

-- Neighborhood -> Borough
ALTER TABLE public.Neighborhood
    ADD CONSTRAINT fk_neigh_borough FOREIGN KEY (borough_id) 
    REFERENCES public.Borough (borough_id);

-- Hosts -> Neighborhood
ALTER TABLE public.Airbnb_Hosts
    ADD CONSTRAINT fk_host_neigh FOREIGN KEY (neighborhood_id) 
    REFERENCES public.Neighborhood (neighborhood_id);

-- Listings -> Hosts, Borough, Neighborhood
ALTER TABLE public.Airbnb_Listings
    ADD CONSTRAINT fk_list_host FOREIGN KEY (host_id) 
    REFERENCES public.Airbnb_Hosts (host_id);

ALTER TABLE public.Airbnb_Listings
    ADD CONSTRAINT fk_list_neigh FOREIGN KEY (neighborhood_id) 
    REFERENCES public.Neighborhood (neighborhood_id);

-- Sales -> Borough, Neighborhood
ALTER TABLE public.NYC_Rolling_Sales
    ADD CONSTRAINT fk_sale_neigh FOREIGN KEY (neighborhood_id) 
    REFERENCES public.Neighborhood (neighborhood_id);

-- Crime -> Borough, Neighborhood
ALTER TABLE public.NYPD_Complaints
    ADD CONSTRAINT fk_crime_neigh FOREIGN KEY (neighborhood_id) 
    REFERENCES public.Neighborhood (neighborhood_id);