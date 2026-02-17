```math
\langle
  \{(nId, nName, sPrice, sSqft, hId) \mid
    \exists sId, bCat, units, yBuilt, sDate,
    lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo,
    hName, hCreated, hLoc, outNYC, numLocal .
    Neighborhood(nId, nName) \land
    PropertySale(sId, bCat, units, sSqft, yBuilt, sPrice, sDate) \land
    LocatedIn(sId, nId) \land
    AirbnbHost(hId, hName, hCreated, hLoc, outNYC, numLocal) \land
    Owns(hId, lId) \land
    AirbnbListing(lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo) \land
    LocatedIn(lId, nId) \land
    outNYC = \text{True} \land
    hCreated > \text{2016-12-01} \land
    sSqft > 0
  \}
\rangle
```

```math
\langle
  \{(bId, bName, lId, cId) \mid
    \exists nId, nName,
    lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo,
    cTime, cEnd, cType, cLevel, cStatus, cPrem, cPos, cSex, cAge, cGeo .
    Borough(bId, bName) \land
    Neighborhood(nId, nName) \land
    PartOf(nId, bId) \land
    AirbnbListing(lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo) \land
    LocatedIn(lId, nId) \land
    CriminalComplaint(cId, cTime, cType, cLevel, cStatus, cPrem, cPos, cSex, cAge, cGeo) \land
    LocatedIn(cId, bId) \land
    (cType = \text{GRAND LARCENY} \lor cType = \text{PETIT LARCENY}) \land
    lRev \ge \text{2016-06-01} \land
    lRev \le cEnd \land lRev \ge cTime
  \}
\rangle
```

```math
\langle
  \{(nId, nName, cId, lId) \mid
    \exists cTime, cType, cLevel, cStatus, cPrem, cPos, cSex, cAge, cGeo,
    lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo .
    Neighborhood(nId, nName) \land
    CriminalComplaint(cId, cTime, cType, cLevel, cStatus, cPrem, cPos, cSex, cAge, cGeo) \land
    LocatedIn(cId, nId) \land
    AirbnbListing(lId, lName, lDate, pType, rType, cap, lSqft, dPrice, minN, maxN, avail, fRev, lRev, lScore, lGeo) \land
    LocatedIn(lId, nId) \land
    cSex = \text{F} \land
    Contains(cPrem, \text{RESIDENCE}) \land
    rType = \text{Private room}
  \}
\rangle
```

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