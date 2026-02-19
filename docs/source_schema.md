### **Source Schema Definition**

```text
S = {NYPD_Complaints, NYC_Rolling_Sales, Airbnb_Listings, Neighbourhoods_CSV, Neighbourhoods_GeoJSON}
```
---

### 1. Source Relation: `NYPD_Complaints`

**Source File:** `data_raw/nypd-complaints.csv`

**Description:** Records of reported criminal complaints in New York City.

| Attribute | Data Type | Constraint | Description |
| --- | --- | --- | --- |
| **`CMPLNT_NUM`** | `String` | **PK** | Unique identifier for the complaint |
| `BORO_NM` | `String` |  | Borough name (e.g., 'BRONX', 'QUEENS') |
| `CMPLNT_FR_DT` | `Date` |  | Date of the crime occurrence |
| `CMPLNT_FR_TM` | `Time` | | Time of the crime occurrence |
| `CRM_ATPT_CPTD_CD` | `String` |  | Status of the crime (e.g., 'COMPLETED', 'ATTEMPTED') |
| `LAW_CAT_CD` | `String` |  | Level of offense (e.g., 'FELONY', 'MISDEMEANOR') |
| `LOC_OF_OCCUR_DESC` | `String` |  | Location category (e.g., 'INSIDE', 'FRONT OF') |
| `OFNS_DESC` | `String` |  | Description of the offense (e.g., 'GRAND LARCENY') |
| `PREM_TYP_DESC` | `String` |  | Specific premise type (e.g., 'RESIDENCE - APT. HOUSE', 'PARK') |
| `VIC_SEX` | `String` |  | Gender of the victim ('M', 'F', 'E', 'D') |
| `VIC_AGE_GROUP` | `String` |  | Age bracket of the victim (e.g., '25-44') |
| `Latitude` | `Float` |  | Latitude coordinate |
| `Longitude` | `Float` |  | Longitude coordinate |

---

### 2. Source Relation: `NYC_Rolling_Sales`

**Source File:** `data_raw/nyc-rolling-sales.csv`

**Description:** Real estate sales transactions in NYC.

| Attribute | Data Type | Constraint | Description |
| --- | --- | --- | --- |
| **`NULL`** | `Integer` | **PK** | Line identifier with empty header |
| `BOROUGH` | `Integer` |  | Borough number |
| `NEIGHBORHOOD` | `String` |  | Neighborhood name |
| `BUILDING CLASS CATEGORY` | `String` |  | Classification of the property (e.g., '01 ONE FAMILY DWELLINGS') |
| `TOTAL UNITS` | `Integer` |  | Total number of units in the property |
| `GROSS SQUARE FEET` | `Integer` |  | Gross square footage of the property |
| `YEAR BUILT` | `Integer` |  | Year the building was constructed |
| `SALE PRICE` | `Float` |  | Sale price in USD |
| `SALE DATE` | `Date` |  | Date the sale was finalized |

---

### 3. Source Relation: `Airbnb_Listings`

**Source File:** `data_raw/nyc-airbnb/listings_detail.csv`

**Description:** Airbnb listing details including host information and availability metrics.

| Attribute | Data Type | Constraint | Description |
| --- | --- | --- | --- |
| **`id`** | `String` | **PK** | Unique identifier for the listing |
| `last_scraped` | `Date` |  | Date the data was scraped |
| `name` | `String` |  | Title of the listing |
| `host_id` | `String` |  | Unique identifier for the host |
| `host_name` | `String` |  | Name of the host |
| `host_since` | `Date` |  | Date the host joined Airbnb |
| `host_location` | `String` |  | Location string provided by the host |
| `host_neighbourhood` | `String` |  | Host's self-reported neighborhood |
| `neighbourhood_cleansed` | `String` |  | Normalized neighborhood name |
| `neighbourhood_group_cleansed` | `String` |  | Normalized borough name |
| `latitude` | `Float` |  | Latitude coordinate |
| `longitude` | `Float` |  | Longitude coordinate |
| `property_type` | `String` |  | Type of building (e.g., 'Apartment', 'House') |
| `room_type` | `String` |  | Type of room (e.g., 'Entire home/apt', 'Private room') |
| `accommodates` | `Integer` |  | Maximum number of guests |
| `square_feet` | `Float` |  | Size of the listing in square feet (often NULL) |
| `price` | `Float` |  | Nightly price in USD |
| `minimum_nights` | `Integer` |  | Minimum stay required |
| `maximum_nights` | `Integer` |  | Maximum stay allowed |
| `availability_365` | `Integer` |  | Days available out of the next 365 |
| `first_review` | `Date` |  | Date of the first review |
| `last_review` | `Date` |  | Date of the most recent review |
| `review_scores_location` | `Integer` |  | Review score for location (0-10) |
| `calculated_host_listings_count` | `Integer` |  | Number of NYC listings managed by this host |

---

### 4. Source Relation: `Neighbourhoods_CSV`

**Source File:** `data_raw/nyc-airbnb/neighbourhoods.csv`

**Description:** A mapping list connecting individual NYC neighborhoods to their respective boroughs.

| Attribute | Data Type | Constraint | Description |
| --- | --- | --- | --- |
| `neighbourhood_group` | `String` |  | Borough or group name the neighborhood belongs to (e.g., 'Bronx') |
| **`neighbourhood`** | `String` | **PK** | Name of the neighborhood |

---

### 5. Source Relation: `Neighbourhoods_GeoJSON`

**Source File:** `data_raw/nyc-airbnb/neighbourhoods.geojson`

**Description:** Geographic boundaries for New York City neighborhoods, typically used for spatial analysis, geofencing, and mapping visualization.

| Attribute | Data Type | Constraint | Description |
| --- | --- | --- | --- |
| `neighbourhood_group` | `String` |  | Borough or group name the neighborhood belongs to |
| **`neighbourhood`** | `String` | **PK** | Name of the neighborhood |
| `geometry` | `Geometry` |  | Spatial boundaries (Polygons/MultiPolygons) representing the exact borders of the neighborhood |