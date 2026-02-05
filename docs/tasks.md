### **1. The "Gentrification & Speculation" Monitor (Merged)**

**Concept:** Analyze the correlation between "Absentee Speculators" (hosts living outside NYC who joined recently) and property inflation.

* **Hypothesis:** Neighborhoods with a high density of non-resident, new hosts will show a steeper `SALE PRICE` per square foot compared to neighborhoods with veteran, local hosts.
* **Datasets & Fields:**
* **Airbnb:** `host_location` (Semantic check for "NY" or "New York"), `host_since` (Date), `host_id`.
* **Sales:** `SALE PRICE`, `GROSS SQUARE FEET`, `NEIGHBORHOOD`.


* **Integration Logic:**
1. **Filter (Airbnb):** Create a "Speculator" flag where `host_location`  "New York" AND `host_since` > '2020-01-01'.
2. **Aggregate:** Calculate the percentage of listings owned by Speculators per `NEIGHBORHOOD`.
3. **Filter (Sales):** Exclude commercial buildings; focus on Residential. Calculate `Avg Price / Gross SqFt` per neighborhood.
4. **Join:** Correlate the "Speculator Percentage" with "Price per SqFt".


* **Why it's good:** It combines semantic text analysis (`host_location`) with temporal profiling (`host_since`) to explain financial trends.

### **2. The "Tourist Trap" Spatio-Temporal Correlation**

**Concept:** Determine if crimes spike in exact locations and times where tourists are most active, testing the "victim availability" theory.

* **Hypothesis:** High review activity (a proxy for tourist presence) temporally correlates with "Grand Larceny" (Pickpocketing), whereas Assaults might not.
* **Datasets & Fields:**
* **Airbnb:** `last_review` (Date), `latitude`, `longitude`.
* **NYPD:** `CMPLNT_FR_DT` (Date), `OFNS_DESC` (Crime Type), `latitude`, `longitude`.


* **Integration Logic:**
1. **Filter (Airbnb):** Identify "Active Tourist Spots" by selecting listings with `last_review` within the last 30 days of the analyzed period.
2. **Filter (NYPD):** Select `OFNS_DESC` IN ('GRAND LARCENY', 'PETIT LARCENY').
3. **Complex Join:** Perform a **Spatio-Temporal Join**:
* *Spatial:* Distance(Airbnb, Crime) < 150 meters.
* *Temporal:* Abs(Crime_Date - Last_Review_Date) < 7 days.




* **Why it's good:** This fulfills the "Complex Mapping" requirement by using non-equality joins (Distance and Time windows) rather than just ID matching.

### **3. The "Demographic Safety" Filter (Solo Traveler Analysis)**

**Concept:** A safety recommendation tool that tailors risk analysis based on the traveler's profile and accommodation type.

* **Hypothesis:** Violent crimes against women occur more frequently in specific premise types (e.g., Parks vs. Residences), and specific Airbnb room types expose travelers to these risks differently.
* **Datasets & Fields:**
* **NYPD:** `VIC_SEX` (Victim Gender), `PREM_TYP_DESC` (Location: "RESIDENCE", "STREET", "PARK").
* **Airbnb:** `room_type` ("Private room" vs "Entire home"), `neighbourhood`.


* **Integration Logic:**
1. **User Query:** "Female solo traveler looking for a Private Room."
2. **Filter (NYPD):** Select crimes where `VIC_SEX` = 'F' AND `PREM_TYP_DESC` matches 'RESIDENCE - APT. HOUSE' (Risk inside the apartment).
3. **Filter (Airbnb):** Select listings where `room_type` = 'Private room'.
4. **Result:** Rank neighborhoods by the *lowest* count of "In-Residence" crimes against females.


* **Why it's good:** It demonstrates deeply granular usage of the NYPD dataset (`PREM_TYP_DESC`) to solve a specific user problem.

### **4. The "Illegal Hotel" Detector (Merged)**

**Concept:** Identify residential buildings being misused as full-time professional hotels, violating zoning laws.

* **Hypothesis:** "One Family Dwellings" with "Entire Home" listings available 300+ days a year are likely illegal operations.
* **Datasets & Fields:**
* **Sales:** `BUILDING CLASS CATEGORY` ("01 ONE FAMILY DWELLINGS"), `ADDRESS`.
* **Airbnb:** `room_type` ("Entire home/apt"), `calculated_host_listings_count` (Professionality), `availability_365` (Occupancy).


* **Integration Logic:**
1. **Filter (Sales):** Select strictly `One Family Dwellings` or `Two Family Dwellings`.
2. **Filter (Airbnb):** Select listings where (`calculated_host_listings_count` > 2 OR `availability_365` > 300).
3. **Join:** On `NEIGHBORHOOD` (or fuzzy match Address if you want to be advanced).
4. **Result:** A "Watchlist" of neighborhoods where residential zoning is being eroded by commercial hospitality.



### **5. The "Perception Gap" Analysis**

**Concept:** Quantify the disconnect between subjective guest experience and objective safety reality.

* **Hypothesis:** Tourists often rate locations 5/5 stars even in neighborhoods with crime rates in the 90th percentile ("Deceptive Safety").
* **Datasets & Fields:**
* **Airbnb:** `review_scores_location` (1-5 scale), `number_of_reviews` (Confidence).
* **NYPD:** `OFNS_DESC` (Filter for 'VIOLENT' categories), `CMPLNT_NUM` (Count).


* **Integration Logic:**
1. **Aggregate (Airbnb):** Calculate weighted average `review_scores_location` per neighborhood (ignore listings with < 10 reviews).
2. **Aggregate (NYPD):** Calculate "Violent Crimes per Listing" density.
3. **Compare:** Select neighborhoods where `Review Score` > 4.8 AND `Crime Density` is in the top 10%.


* **Why it's good:** It contrasts "Sentiment Data" (Reviews) against "Administrative Data" (Police Reports).

### **6. The "Condo Yield" Investment Map**

**Concept:** A calculator to identify the most profitable *and* safe locations for real estate investors looking to convert condos into short-term rentals.

* **Hypothesis:** Some neighborhoods offer low purchase prices but high rental demand, provided the burglary risk is managed.
* **Datasets & Fields:**
* **Sales:** `BUILDING CLASS CATEGORY` (Filter for "%CONDOS%"), `SALE PRICE`.
* **Airbnb:** `price` (Nightly Rate), `availability_365` (Yield potential).
* **NYPD:** `OFNS_DESC` (Filter for 'BURGLARY').


* **Integration Logic:**
1. **Sales Metric:** Avg `SALE PRICE` for Condos per neighborhood.
2. **Airbnb Metric:** Annual Potential Revenue = `Avg Price` * `min(availability_365, 200)` (Conservative occupancy).
3. **Risk Metric:** Count of `BURGLARY` per neighborhood.
4. **Final Calculation:** `(Annual Revenue / Sale Price) * (1 / Normalized Burglary Score)`.


* **Why it's good:** It creates a derived metric ("Yield Ratio") that relies on data from all three sources existing simultaneously.

### **7. The "Hospitality War" (Land Use Analysis)**

**Concept:** Analyze if Airbnbs are clustering near established Hotel districts (complementary) or invading residential sanctuaries (cannibalistic).

* **Hypothesis:** "Entire Home" Airbnbs cluster near buildings sold as "HOTELS", whereas "Private Rooms" scatter further out.
* **Datasets & Fields:**
* **Sales:** `BUILDING CLASS CATEGORY` (Filter for "HOTELS"), `YEAR BUILT` (New vs Old hotels).
* **Airbnb:** `room_type`, `latitude`, `longitude`.


* **Integration Logic:**
1. **Set A (Hotels):** Geolocation of all sales where Building Class contains "HOTEL".
2. **Set B (Airbnbs):** Geolocation of all "Entire Home" listings.
3. **Spatial Analysis:** Calculate the average distance from every Airbnb to the nearest sold Hotel.
4. **Grouping:** Group by `NEIGHBORHOOD` to see which areas are mixed-use vs. strictly segregated.