### **1. The "Gentrification & Speculation" Monitor**

```math
\langle
  \{(nName, avgPriceSqft, numSpecHosts) \mid
    \exists nId, sId, bCat, units, sPrice, sSqft, yBuilt, sDate,
    hId, hName, hCreated, hLoc, outNYC, numLocal, lId .
    Neighborhood(nId, nName) \land
    PropertySale(sId, bCat, units, sSqft, yBuilt, sPrice, sDate) \land
    LocatedIn(sId, nId) \land
    AirbnbHost(hId, hName, hCreated, hLoc, outNYC, numLocal) \land
    Owns(hId, lId) \land
    LocatedIn(lId, nId) \land
    outNYC = \text{True} \land
    hCreated > \text{2016-09-01} \land
    sSqft > 0 \land
    avgPriceSqft = \text{AVG}(sPrice / sSqft)
  \}
\rangle
```

### **2. The "Tourist Trap" Correlation**

```math
\langle
  \{(nName, numListings, crimeCount) \mid
    \exists nId, lId, lRev, cId, cTime, cEnd, cType .
    Neighborhood(nId, nName) \land
    AirbnbListing(lId, \dots, lRev, \dots) \land
    LocatedIn(lId, nId) \land
    CriminalComplaint(cId, cTime, \dots, cEnd, cType, \dots) \land
    LocatedIn(cId, nId) \land
    cType \in \{\text{'GRAND LARCENY', 'PETIT LARCENY'}\} \land
    lRev \ge cTime \land lRev \le cEnd
  \}
\rangle
```

### **3. The "Demographic Safety" Filter (Solo Traveler Analysis)**

```math
\langle
  \{(nName, crimeCount, listingCount) \mid
    \exists nId, cId, cSex, cPrem, cPos, lId, rType .
    Neighborhood(nId, nName) \land
    CriminalComplaint(cId, \dots, cSex, \dots, cPrem, cPos, \dots) \land
    LocatedIn(cId, nId) \land
    cSex = \text{'F'} \land cPos = \text{'INSIDE'} \land 
    \text{Contains}(\text{LCase}(cPrem), \text{'residence'}) \land
    AirbnbListing(lId, \dots, rType, \dots) \land
    LocatedIn(lId, nId) \land
    rType = \text{'Private room'}
  \}
\rangle
```

### **4. The Commercial Overhaul Detector**

```math
\langle
  \{(nId, nName, sId, lId) \mid
    \exists bCat, units, sqft, yBuilt, price, sDate,
    lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo,
    hId, hName, hCreated, hLoc, outNYC, numLocal .
    Neighborhood(nId, nName) \land
    PropertySale(sId, bCat, units, sqft, yBuilt, price, sDate) \land
    LocatedIn(sId, nId) \land
    AirbnbListing(lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo) \land
    LocatedIn(lId, nId) \land
    Owns(hId, lId) \land
    AirbnbHost(hId, hName, hCreated, hLoc, outNYC, numLocal) \land
    (bCat = \text{01 ONE FAMILY DWELLINGS} \lor bCat = \text{02 TWO FAMILY DWELLINGS}) \land
    rType = \text{Entire home/apt} \land
    (avail > 300 \lor numLocal > 2)
  \}
\rangle
```

### **5. The "Perception Gap" Analysis**

```math
\langle
  \{(nId, nName, sPrice, annualRev, cId) \mid
    \exists sId, bCat, units, sqft, yBuilt, sDate,
    lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo,
    cTime, cType, cLevel, cStatus, cPrem, cPos, cSex, cAge, cGeo .
    Neighborhood(nId, nName) \land
    PropertySale(sId, bCat, units, sqft, yBuilt, sPrice, sDate) \land
    Contains(LCase(bCat), \text{'condo'}) \land
    AirbnbListing(lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo) \land
    LocatedIn(lId, nId) \land
    LocatedIn(sId, nId) \land
    annualRev = (dPrice \times avail) \land
    (CriminalComplaint(cId, cTime, cType, cLevel, cStatus, cPrem, cPos, cSex, cAge, cGeo) \land
    LocatedIn(cId, nId) \land
    cType \in \{\text{'GRAND LARCENY', 'PETIT LARCENY', 'THEFT-FRAUD'}\})
  \}
\rangle
```
### **6. The "Condo Yield" Investment Map**

```math
\langle
  \{(sId, lId) \mid
    \exists bCat, units, sqft, yBuilt, price, sDate, nId,
    lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo .
    PropertySale(sId, bCat, units, sqft, yBuilt, price, sDate) \land
    Contains(bCat, \text{'HOTELS'}) \land
    AirbnbListing(lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo) \land
    rType = \text{'Entire home/apt'}
  \}
\rangle
```

### **7. The "Hospitality War" (Land Use Analysis)**

```math
\langle
  \{(nName, hotelCount, entireHomeCount) \mid
    \exists nId, sId, bCat, lId, rType .
    Neighborhood(nId, nName) \land
    PropertySale(sId, bCat, \dots) \land 
    \text{Contains}(\text{LCase}(bCat), \text{'hotel'}) \land
    \text{OPTIONAL}(AirbnbListing(lId, \dots, rType, \dots) \text{ s.t. } rType = \text{'Entire home/apt'})
  \}
\rangle
```