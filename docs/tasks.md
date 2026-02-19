### **1. The "Gentrification & Speculation" Monitor**

**Concept:** Analyze the correlation between absentee speculators and property inflation per neighborhood.

* **Hypothesis:** Neighborhoods with a high volume of non-resident hosts joining after September 2016 will show a steeper average sale price per square foot.
  
 **Integration Logic:**
 *  **Filter (Airbnb):** Identify "Speculator Hosts" as those where `is_outside_nyc` is true and their account was created after September 1, 2016.
 
* **Filter (Sales):** Only include property sales where the `gross_sqft` is greater than 0.

* **Aggregate:** Group by neighborhood to calculate the `AVG(sale_price / gross_sqft)` alongside the count of distinct speculator hosts. Order the results in descending order for both metrics.


### **2. The "Tourist Trap" Correlation**

**Concept:** Determine if property crimes temporally overlap with recent tourist activity in a given area.

* **Hypothesis:** High recent review activity temporally correlates with larceny incidents in the same neighborhood.
  
**Integration Logic:**

* **Filter (NYPD):** Select crimes where the offense type is either "GRAND LARCENY" or "PETIT LARCENY".


* **Join:** Perform a temporal overlap join by ensuring the Airbnb review date falls between the crime's start date and the end of the crime window. Aggregate the counts of listings and crimes by neighborhood.





### **3. The "Demographic Safety" Filter (Solo Traveler Analysis)**

**Concept:** A targeted safety query ranking neighborhoods for solo female travelers seeking private rooms.

* **Hypothesis:** Certain neighborhoods have lower rates of female-targeted crimes occurring within residential premises, making them safer for renting private rooms.
  
 **Integration Logic:**
* **Filter (NYPD):** Count crimes where the victim sex is "F", the premise type contains the word "residence", and the premise position is explicitly 'INSIDE'.


* **Filter (Airbnb):** Count listings where the `room_type` is strictly "Private room".


* **Result:** Group by neighborhood and order the results to show the lowest crime counts first, followed by the highest availability of private rooms.



### **4. The Commercial Overhaul Detector**

**Concept:** Identify boroughs where residential housing is potentially being sold to become Airbnbs.

* **Hypothesis:** Areas with high sales of one and two-family dwellings alongside high volumes of highly-available "Entire Home" Airbnb listings may indicate selling of properties to become Airbnbs .
  
**Integration Logic:**
* **Filter (Sales):** Select properties categorized strictly as "01 ONE FAMILY DWELLINGS" or "02 TWO FAMILY DWELLINGS".


* **Filter (Airbnb):** Select "Entire home/apt" listings where the host owns more than 2 local listings OR the listing is available for more than 300 days a year.


* **Result:** Group by borough to count the distinct suspicious listings versus family house sales, ranking the highest counts first.





### **5. The "Perception Gap" Analysis**

**Concept:** Quantify the disconnect between highly-rated guest experiences and the objective reality of severe crime.

* **Hypothesis:** Tourists may rate neighborhood locations very highly (above a 9) despite a high volume of local felonies.
  
 **Integration Logic:**
* **Filter (Airbnb):** Filter for listings with more than 10 reviews, aggregate their location scores, and keep only neighborhoods having an average score strictly greater than 9.


* **Filter (NYPD):** Count distinct criminal complaints where the offense level is classified as a "FELONY".


* **Result:** Group by neighborhood, contrasting the count of felonies against the high average location score.





### **6. The "Condo Yield" Investment Map**

**Concept:** A calculator to identify neighborhoods with high short-term rental revenue potential relative to condo prices, factoring in theft risks.

* **Hypothesis:** Comparing condo sale prices to capped Airbnb revenue, while tracking local larceny/fraud, reveals optimal investment zones.

 **Integration Logic:**
* **Sales Metric:** Calculate the average `sale_price` for buildings where the category contains "condo".


* **Airbnb Metric:** Calculate annual revenue as `daily_price` multiplied by availability (capped at a maximum of 200 days for a conservative estimate).


* **Risk Metric:** Count distinct crimes where the offense type is "GRAND LARCENY", "PETIT LARCENY", or "THEFT-FRAUD".


* **Result:** Group by neighborhood and rank by highest annual revenue, then crime counts, then average sale price.





### **7. The "Hospitality War" (Land Use Analysis)**

**Concept:** Analyze the clustering and density of commercial hotels versus "Entire Home" Airbnbs within neighborhoods.

* **Hypothesis:** Counting hotel sales alongside whole-apartment rentals reveals which neighborhoods are strictly commercialized versus mixed-use.

 **Integration Logic:**
* **Set A (Hotels):** Count distinct property sales where the building category contains "hotel".


* **Set B (Airbnbs):** Count distinct Airbnb listings where the room type is "Entire home/apt".


* **Result:** Group the counts by neighborhood and order by the highest density of entire homes, followed by hotel sales.
