-- ==========================================
-- 1. Drop and Create Staging Table
-- ==========================================
DROP TABLE IF EXISTS staging_airbnb;

CREATE TABLE staging_airbnb (
    id VARCHAR,
    listing_url VARCHAR,
    scrape_id VARCHAR,
    last_scraped VARCHAR,
    name VARCHAR,
    summary VARCHAR,
    space VARCHAR,
    description VARCHAR,
    experiences_offered VARCHAR,
    neighborhood_overview VARCHAR,
    notes VARCHAR,
    transit VARCHAR,
    access VARCHAR,
    interaction VARCHAR,
    house_rules VARCHAR,
    thumbnail_url VARCHAR,
    medium_url VARCHAR,
    picture_url VARCHAR,
    xl_picture_url VARCHAR,
    host_id VARCHAR,
    host_url VARCHAR,
    host_name VARCHAR,
    host_since VARCHAR,
    host_location VARCHAR,
    host_about VARCHAR,
    host_response_time VARCHAR,
    host_response_rate VARCHAR,
    host_acceptance_rate VARCHAR,
    host_is_superhost VARCHAR,
    host_thumbnail_url VARCHAR,
    host_picture_url VARCHAR,
    host_neighbourhood VARCHAR,
    host_listings_count VARCHAR,
    host_total_listings_count VARCHAR,
    host_verifications VARCHAR,
    host_has_profile_pic VARCHAR,
    host_identity_verified VARCHAR,
    street VARCHAR,
    neighbourhood VARCHAR,
    neighbourhood_cleansed VARCHAR,
    neighbourhood_group_cleansed VARCHAR,
    city VARCHAR,
    state VARCHAR,
    zipcode VARCHAR,
    market VARCHAR,
    smart_location VARCHAR,
    country_code VARCHAR,
    country VARCHAR,
    latitude VARCHAR,
    longitude VARCHAR,
    is_location_exact VARCHAR,
    property_type VARCHAR,
    room_type VARCHAR,
    accommodates VARCHAR,
    bathrooms VARCHAR,
    bedrooms VARCHAR,
    beds VARCHAR,
    bed_type VARCHAR,
    amenities VARCHAR,
    square_feet VARCHAR,
    price VARCHAR,
    weekly_price VARCHAR,
    monthly_price VARCHAR,
    security_deposit VARCHAR,
    cleaning_fee VARCHAR,
    guests_included VARCHAR,
    extra_people VARCHAR,
    minimum_nights VARCHAR,
    maximum_nights VARCHAR,
    calendar_updated VARCHAR,
    has_availability VARCHAR,
    availability_30 VARCHAR,
    availability_60 VARCHAR,
    availability_90 VARCHAR,
    availability_365 VARCHAR,
    calendar_last_scraped VARCHAR,
    number_of_reviews VARCHAR,
    first_review VARCHAR,
    last_review VARCHAR,
    review_scores_rating VARCHAR,
    review_scores_accuracy VARCHAR,
    review_scores_cleanliness VARCHAR,
    review_scores_checkin VARCHAR,
    review_scores_communication VARCHAR,
    review_scores_location VARCHAR,
    review_scores_value VARCHAR,
    requires_license VARCHAR,
    license VARCHAR,
    jurisdiction_names VARCHAR,
    instant_bookable VARCHAR,
    is_business_travel_ready VARCHAR,
    cancellation_policy VARCHAR,
    require_guest_profile_picture VARCHAR,
    require_guest_phone_verification VARCHAR,
    calculated_host_listings_count VARCHAR,
    reviews_per_month VARCHAR
);

-- ==========================================
-- 2. Load CSV into Staging Table
-- ==========================================
SET CLIENT_ENCODING TO 'utf8';
\copy staging_airbnb FROM 'data_processed/nyc-airbnb/listings_detail_no_bad_lines.csv' WITH (FORMAT csv, HEADER true, QUOTE '"', ESCAPE '\');


-- ==========================================
-- 3. Create Clean Table
-- ==========================================
DROP TABLE IF EXISTS clean_airbnb;

CREATE TABLE clean_airbnb (
    id VARCHAR PRIMARY KEY,
    last_scraped DATE,
    name VARCHAR,
    host_id VARCHAR,
    host_name VARCHAR,
    host_since DATE,
    host_location VARCHAR,
    host_neighbourhood VARCHAR,
    neighbourhood_cleansed VARCHAR,
    neighbourhood_group_cleansed VARCHAR,
    latitude FLOAT,
    longitude FLOAT,
    property_type VARCHAR,
    room_type VARCHAR,
    accommodates INT,
    square_feet FLOAT,
    price FLOAT,
    minimum_nights INT,
    maximum_nights INT,
    availability_365 INT,
    first_review DATE,
    last_review DATE,
    number_of_reviews INT,
    review_scores_location INT,
    calculated_host_listings_count INT,
    host_is_outside_nyc BOOLEAN
);

-- ==========================================
-- 4. Insert Cleaned Data
-- ==========================================
INSERT INTO clean_airbnb (
    id,
    last_scraped,
    name,
    host_id,
    host_name,
    host_since,
    host_location,
    host_neighbourhood,
    neighbourhood_cleansed,
    neighbourhood_group_cleansed,
    latitude,
    longitude,
    property_type,
    room_type,
    accommodates,
    square_feet,
    price,
    minimum_nights,
    maximum_nights,
    availability_365,
    first_review,
    last_review,
    number_of_reviews,
    review_scores_location,
    calculated_host_listings_count,
    host_is_outside_nyc
)
SELECT
    id,
    
    -- Dates
    CASE WHEN TRIM(last_scraped) IN ('', '-', 'N/A') THEN NULL ELSE TO_DATE(last_scraped, 'YYYY-MM-DD') END AS last_scraped,
    name,
    host_id,
    NULLIF(TRIM(host_name), '-') AS host_name,
    CASE WHEN TRIM(host_since) IN ('', '-', 'N/A') THEN NULL ELSE TO_DATE(host_since, 'YYYY-MM-DD') END AS host_since,
    NULLIF(TRIM(host_location), '-') AS host_location,
    NULLIF(TRIM(host_neighbourhood), '-') AS host_neighbourhood,
    NULLIF(TRIM(neighbourhood_cleansed), '-') AS neighbourhood_cleansed,
    CASE 
        WHEN TRIM(neighbourhood_group_cleansed) IN ('', '-', 'N/A') THEN NULL
        ELSE UPPER(TRIM(neighbourhood_group_cleansed))
    END AS neighbourhood_group_cleansed,
    
    -- Floats
    CASE WHEN TRIM(latitude) IN ('', '-', 'N/A') THEN NULL ELSE CAST(TRIM(latitude) AS DOUBLE PRECISION) END AS latitude,
    CASE WHEN TRIM(longitude) IN ('', '-', 'N/A') THEN NULL ELSE CAST(TRIM(longitude) AS DOUBLE PRECISION) END AS longitude,
    
    property_type,
    room_type,
    
    -- Integers (double cast to handle 10.0, 1.0 etc)
    CASE WHEN TRIM(accommodates) IN ('', '-', 'N/A') THEN NULL ELSE CAST(CAST(TRIM(accommodates) AS DOUBLE PRECISION) AS INT) END AS accommodates,
    CASE WHEN TRIM(square_feet) IN ('', '-', 'N/A') THEN NULL ELSE CAST(TRIM(square_feet) AS DOUBLE PRECISION) END AS square_feet,
    CASE WHEN TRIM(price) IN ('', '-', 'N/A') THEN NULL ELSE CAST(REPLACE(REPLACE(TRIM(price), '$', ''), ',', '') AS DOUBLE PRECISION) END AS price,
    CASE WHEN TRIM(minimum_nights) IN ('', '-', 'N/A') THEN NULL ELSE CAST(CAST(TRIM(minimum_nights) AS DOUBLE PRECISION) AS INT) END AS minimum_nights,
    CASE WHEN TRIM(maximum_nights) IN ('', '-', 'N/A') THEN NULL ELSE CAST(CAST(TRIM(maximum_nights) AS DOUBLE PRECISION) AS INT) END AS maximum_nights,
    CASE WHEN TRIM(availability_365) IN ('', '-', 'N/A') THEN NULL ELSE CAST(CAST(TRIM(availability_365) AS DOUBLE PRECISION) AS INT) END AS availability_365,
    
    -- Review dates
    CASE WHEN TRIM(first_review) IN ('', '-', 'N/A') THEN NULL ELSE TO_DATE(first_review, 'YYYY-MM-DD') END AS first_review,
    CASE WHEN TRIM(last_review) IN ('', '-', 'N/A') THEN NULL ELSE TO_DATE(last_review, 'YYYY-MM-DD') END AS last_review,
    
    -- Scores / counts
    CASE WHEN TRIM(number_of_reviews) IN ('', '-', 'N/A') THEN NULL ELSE CAST(CAST(TRIM(number_of_reviews) AS DOUBLE PRECISION) AS INT) END AS number_of_reviews,
    CASE WHEN TRIM(review_scores_location) IN ('', '-', 'N/A') THEN NULL ELSE CAST(CAST(TRIM(review_scores_location) AS DOUBLE PRECISION) AS INT) END AS review_scores_location,
    CASE WHEN TRIM(calculated_host_listings_count) IN ('', '-', 'N/A') THEN NULL ELSE CAST(CAST(TRIM(calculated_host_listings_count) AS DOUBLE PRECISION) AS INT) END AS calculated_host_listings_count,
    
    -- Boolean: host outside NYC
    CASE 
        WHEN host_location IS NULL THEN FALSE
        WHEN UPPER(host_location) ~ '(NEW YORK|NY|QUEENS|BROOKLYN|BRONX|MANHATTAN|STATEN ISLAND)' THEN FALSE
        ELSE TRUE
    END AS host_is_outside_nyc
FROM staging_airbnb;
