
# I. Spatial Domain

### **Borough**

**Borough**(`borough_id`, `name`)

Represents a major administrative district of New York City (e.g., Manhattan, Queens).

* **Attributes:**
* `borough_id` (Integer): Internal unique identifier.
* `name` (String): The official name of the borough.



---

### **Neighborhood**

**Neighborhood**(`neighborhood_id`, `name`)

Represents a distinct administrative or historical area within a borough (e.g., "West Village", "Bushwick").

* **Attributes:**
* `neighborhood_id` (Integer): Internal unique identifier.
* `name` (String): The standardized name of the neighborhood.



---

# II. Commercial & Housing Domain

### **PropertySale**

**PropertySale**(`sale_id`, `building_category`, `total_units`, `gross_sqft`, `year_built`, `sale_price`, `sale_date`)

Represents a confirmed transaction of a real estate asset recorded by the NYC Department of Finance.

* **Attributes:**
* `sale_id` (Integer): Unique identifier for the transaction.
* `sale_price` (Decimal): The financial cost of the transaction in USD.
* `sale_date` (Date): The official date of the transaction.
* `building_category` (String): Classification of the property (e.g., "01 ONE FAMILY DWELLINGS").
* `gross_sqft` (Integer): The total gross area of the property in square feet.
* `total_units` (Integer): The total number of residential and commercial units in the building.
* `year_built` (Integer): The year the building was originally constructed.



### **AirbnbListing**

**AirbnbListing**(`listing_id`, `name`, `listing_date`, `property_type`, `room_type`, `capacity`, `square_feet`, `daily_price`, `min_nights`, `max_nights`, `availability_year`, `first_review_date`, `last_review_date`, `location_score`, `geo_location`)

Represents a specific unit or room available for short-term rental on the platform.

* **Attributes:**
* `listing_id` (Integer): Unique identifier for the listing.
* `name` (String): The descriptive title of the listing.
* `listing_date` (Date): The date the data was scraped/recorded.
* `daily_price` (Decimal): The nightly rental cost in USD.
* `property_type` (String): The structural type (e.g., "Apartment", "Loft", "House").
* `room_type` (String): The privacy level (e.g., "Entire home/apt", "Private room").
* `capacity` (Integer): The maximum number of guests accommodated.
* `square_feet` (Integer): The size of the listing (if reported).
* `min_nights` / `max_nights` (Integer): The constraint on stay duration.
* `availability_year` (Integer): The number of days the unit is available within the next 365 days.
* `location_score` (Integer): Aggregate user rating for the location (Scale: 1-5 or 1-10).
* `first_review_date` (Date): The date of the first review received.
* `last_review_date` (Date): The date of the most recent review.
* `geo_location` (Point): The spatial coordinates (Latitude/Longitude).



### **AirbnbHost**

**AirbnbHost**(`host_id`, `host_name`, `account_created`, `location`, `is_outside_nyc`, `num_local_listings`)

Represents the registered owner or manager of one or more listings.

* **Attributes:**
* `host_id` (Integer): Unique identifier for the host account.
* `account_created` (Date): The date the host joined the platform.
* `location` (String): The self-reported location text (e.g., "Paris, France").
* `is_outside_nyc` (Boolean): Derived flag indicating if the host lives outside the NYC area.
* `num_local_listings` (Integer): The total count of listings managed by this host in NYC.



---

# III. Safety Domain

### **CriminalComplaint**

**CriminalComplaint**(`complaint_id`, `timestamp`, `offense_type`, `offense_level`, `offense_status`, `premise_type`, `premise_pos`, `victim_sex`, `victim_age_group`, `geo_location`)

Represents a specific police report filed with the NYPD regarding a felony, misdemeanor, or violation.

* **Attributes:**
* `complaint_id` (Integer): Unique identifier for the complaint.
* `timestamp` (DateTime): The exact date and time the crime occurred.
* `offense_type` (String): The description of the crime (e.g., "BURGLARY", "FELONY ASSAULT").
* `offense_level` (String): The legal severity (e.g., "FELONY", "MISDEMEANOR").
* `offense_status` (String): The state of the crime (e.g., "COMPLETED", "ATTEMPTED").
* `premise_type` (String): The specific location description (e.g., "RESIDENCE - APT. HOUSE", "PARK").
* `premise_pos` (String): Indication of occurrence inside or outside.
* `victim_sex` (String): Gender of the victim (e.g., "M", "F").
* `victim_age_group` (String): Age bracket of the victim.
* `geo_location` (Point): The spatial coordinates (Latitude/Longitude).



---

# Relationships

### **:locatedIn**

*Connects entities to their logical geographic area.*

* **Domain:** `PropertySale`, `AirbnbListing`, `CriminalComplaint`, `AirbnbHost`
* **Range:** `Neighborhood`
* **Usage:**
* `PropertySale`  `Neighborhood`
* `AirbnbListing`  `Neighborhood`
* `CriminalComplaint`  `Neighborhood`
* `AirbnbHost`  `Neighborhood`



### **:owns**

*Connects a Host entity to the Listings they manage.*

* **Domain:** `AirbnbHost`
* **Range:** `AirbnbListing`
* **Usage:**
* `AirbnbHost`  `AirbnbListing`



### **:partOf**

*Connects a Neighborhood to the Borough it belongs to.*

* **Domain:** `Neighborhood`
* **Range:** `Borough`
* **Usage:**
* `Neighborhood`  `Borough`