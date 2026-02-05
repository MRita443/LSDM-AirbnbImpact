
## Neighborhood
_(Union of mappings from Sales and Airbnb Listings)

### Mapping from Sales

```math
\forall nName . \\
\exists sId, bName, bCat, units, sqft, yBuilt, price, sDate . \\
NYC\_Rolling\_Sales(
  sId,
  bName,
  nName,
  bCat,
  units,
  sqft,
  yBuilt,
  price,
  sDate
)
\rightarrow
Neighborhood(Hash(nName), nName)
```

```math
\langle
  \{(nId, nName) \mid
    \exists sId, bName, bCat, units, sqft, yBuilt, price, sDate .
    NYC\_Rolling\_Sales(sId, bName, nName, bCat, units, sqft, yBuilt, price, sDate)
    \land nId = Hash(nName)
  \},
  \;
  \{(nId, nName) \mid
    Neighborhood(nId, nName)
  \}
\rangle
```

### Mapping from Airbnb

```math
\forall nName . \\
\exists lId, sDate, lName, hId, hSince, hLoc, hNeigh, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore, hList, isOut . \\
Airbnb\_Listings(
  lId,
  sDate,
  lName,
  hId,
  hSince,
  hLoc,
  hNeigh,
  nName,
  bName,
  lat,
  lon,
  pType,
  rType,
  cap,
  sqft,
  dPrice,
  minN,
  maxN,
  availYear,
  nRev,
  fRev,
  lRev,
  lScore,
  hList,
  isOut
)
\rightarrow
Neighborhood(Hash(nName), nName)
```

```math
\langle
  \{(nId, nName) \mid
    \exists lId, \dots, isOut .
    Airbnb\_Listings(lId, \dots, nName, \dots, isOut)
    \land nId = Hash(nName)
  \},
  \;
  \{(nId, nName) \mid
    Neighborhood(nId, nName)
  \}
\rangle
```


## Borough

_(Union of mappings from Sales, Airbnb Listings and NYPD Complaints)_

### Mapping from Sales

```math
\forall bName . \\
\exists sId, nName, bCat, units, sqft, yBuilt, price, sDate . \\
NYC\_Rolling\_Sales(
  sId,
  bName,
  nName,
  bCat,
  units,
  sqft,
  yBuilt,
  price,
  sDate
)
\rightarrow
Borough(Hash(bName), bName)
```

```math
\langle
  \{(bId, bName) \mid
    \exists sId, nName, \dots, sDate .
    NYC\_Rolling\_Sales(sId, bName, nName, \dots)
    \land bId = Hash(bName)
  \},
  \;
  \{(bId, bName) \mid
    Borough(bId, bName)
  \}
\rangle
```
### Mapping from Airbnb

```math
\forall bName . \\
\exists lId, \dots, isOut . \\
Airbnb\_Listings(lId, \dots, bName, \dots, isOut)
\rightarrow
Borough(Hash(bName), bName)
```

```math
\langle
  \{(bId, bName) \mid
    \exists lId, \dots, isOut .
    Airbnb\_Listings(lId, \dots, bName, \dots)
    \land bId = Hash(bName)
  \},
  \;
  \{(bId, bName) \mid
    Borough(bId, bName)
  \}
\rangle
```

### Mapping from NYPD

```math
\forall bName . \\
\exists cId, cDate, offStat, offLvl, premPos, offType, premType, vSex, vAge, lat, lon . \\
NYPD\_Complaints(
  cId,
  bName,
  cDate,
  offStat,
  offLvl,
  premPos,
  offType,
  premType,
  vSex,
  vAge,
  lat,
  lon
)
\rightarrow
Borough(Hash(bName), bName)
```

```math
\langle
  \{(bId, bName) \mid
    \exists cId, \dots, lon .
    NYPD\_Complaints(cId, bName, \dots)
    \land bId = Hash(bName)
  \},
  \;
  \{(bId, bName) \mid
    Borough(bId, bName)
  \}
\rangle
```

## PropertySale

```math
\forall sId, bCat, units, sqft, yBuilt, price, sDate . \\
\exists bName, nName . \\
NYC\_Rolling\_Sales(
  sId,
  bName,
  nName,
  bCat,
  units,
  sqft,
  yBuilt,
  price,
  sDate
)
\rightarrow
PropertySale(sId, bCat, units, sqft, yBuilt, price, sDate)
```


```math
\langle
  \{(sId, bCat, units, sqft, yBuilt, price, sDate) \mid
    \exists bName, nName .
    NYC\_Rolling\_Sales(sId, bName, nName, bCat, units, sqft, yBuilt, price, sDate)
  \},
  \;
  \{(sId, bCat, units, sqft, yBuilt, price, sDate) \mid
    PropertySale(sId, bCat, units, sqft, yBuilt, price, sDate)
  \}
\rangle
```



## CriminalComplaint

```math
\forall cId, cDate, offStat, offLvl, premPos, offType, premType, vSex, vAge, lat, lon . \\
\exists bName . \\
NYPD\_Complaints(
  cId,
  bName,
  cDate,
  offStat,
  offLvl,
  premPos,
  offType,
  premType,
  vSex,
  vAge,
  lat,
  lon
)
\rightarrow
CriminalComplaint(
  cId,
  cDate,
  offType,
  offLvl,
  offStat,
  premType,
  premPos,
  vSex,
  vAge,
  ToPoint(lat, lon)
)
```

```math
\langle
  \{(cId, cDate, offType, offLvl, offStat, premType, premPos, vSex, vAge, geo) \mid
    \exists bName, lat, lon .
    NYPD\_Complaints(
      cId,
      bName,
      cDate,
      offStat,
      offLvl,
      premPos,
      offType,
      premType,
      vSex,
      vAge,
      lat,
      lon
    )
    \land geo = ToPoint(lat, lon)
  \},
  \;
  \{(cId, cDate, offType, offLvl, offStat, premType, premPos, vSex, vAge, geo) \mid
    CriminalComplaint(
      cId,
      cDate,
      offType,
      offLvl,
      offStat,
      premType,
      premPos,
      vSex,
      vAge,
      geo
    )
  \}
\rangle
```


## AirbnbListing

```math
\forall lId, lName, sDate, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, fRev, lRev, lScore, lat, lon . \\
\exists hId, hSince, hLoc, hNeigh, nName, bName, nRev, hList, isOut . \\
Airbnb\_Listings(
  lId,
  sDate,
  lName,
  hId,
  hSince,
  hLoc,
  hNeigh,
  nName,
  bName,
  lat,
  lon,
  pType,
  rType,
  cap,
  sqft,
  dPrice,
  minN,
  maxN,
  availYear,
  nRev,
  fRev,
  lRev,
  lScore,
  hList,
  isOut
)
\rightarrow
AirbnbListing(
  lId,
  lName,
  sDate,
  pType,
  rType,
  cap,
  sqft,
  dPrice,
  minN,
  maxN,
  availYear,
  fRev,
  lRev,
  lScore,
  ToPoint(lat, lon)
)
```

```math
\langle
  \{(lId, lName, sDate, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, fRev, lRev, lScore, geo) \mid
    \exists hId, hSince, hLoc, hNeigh, nName, bName, nRev, hList, isOut, lat, lon .
    Airbnb\_Listings(
      lId,
      sDate,
      lName,
      hId,
      \dots,
      lat,
      lon,
      \dots,
      isOut
    )
    \land geo = ToPoint(lat, lon)
  \},
  \;
  \{(lId, lName, sDate, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, fRev, lRev, lScore, geo) \mid
    AirbnbListing(
      lId,
      lName,
      sDate,
      pType,
      rType,
      cap,
      sqft,
      dPrice,
      minN,
      maxN,
      availYear,
      fRev,
      lRev,
      lScore,
      geo
    )
  \}
\rangle
```

## AirbnbHost

```math
\forall hId, hSince, hLoc, isOut, hList . \\
\exists lId, sDate, lName, hNeigh, nName, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore . \\
Airbnb\_Listings(
  lId,
  sDate,
  lName,
  hId,
  hSince,
  hLoc,
  hNeigh,
  nName,
  bName,
  lat,
  lon,
  pType,
  rType,
  cap,
  sqft,
  dPrice,
  minN,
  maxN,
  availYear,
  nRev,
  fRev,
  lRev,
  lScore,
  hList,
  isOut
)
\rightarrow
AirbnbHost(hId, hSince, hLoc, isOut, hList)
```

```math
\langle
  \{(hId, hSince, hLoc, isOut, hList) \mid
    \exists lId, sDate, lName, hNeigh, nName, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore .
    Airbnb\_Listings(
      lId,
      sDate,
      lName,
      hId,
      hSince,
      hLoc,
      hNeigh,
      nName,
      bName,
      lat,
      lon,
      pType,
      rType,
      cap,
      sqft,
      dPrice,
      minN,
      maxN,
      availYear,
      nRev,
      fRev,
      lRev,
      lScore,
      hList,
      isOut
    )
  \},
  \;
  \{(hId, hSince, hLoc, isOut, hList) \mid
    AirbnbHost(hId, hSince, hLoc, isOut, hList)
  \}
\rangle
```


## owns (Host → Listing)

```math
\forall hId, lId . \\
\exists sDate, lName, hSince, hLoc, hNeigh, nName, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore, hList, isOut . \\
Airbnb\_Listings(
  lId,
  sDate,
  lName,
  hId,
  hSince,
  hLoc,
  hNeigh,
  nName,
  bName,
  lat,
  lon,
  pType,
  rType,
  cap,
  sqft,
  dPrice,
  minN,
  maxN,
  availYear,
  nRev,
  fRev,
  lRev,
  lScore,
  hList,
  isOut
)
\rightarrow
owns(hId, lId)
```

```math
\langle
  \{(hId, lId) \mid
    \exists sDate, lName, hSince, hLoc, hNeigh, nName, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore, hList, isOut .
    Airbnb\_Listings(
      lId,
      sDate,
      lName,
      hId,
      hSince,
      hLoc,
      hNeigh,
      nName,
      bName,
      lat,
      lon,
      pType,
      rType,
      cap,
      sqft,
      dPrice,
      minN,
      maxN,
      availYear,
      nRev,
      fRev,
      lRev,
      lScore,
      hList,
      isOut
    )
  \},
  \;
  \{(hId, lId) \mid
    owns(hId, lId)
  \}
\rangle
```


## partOf (Neighborhood → Borough)

```math
\forall nName, bName . \\
\exists sId, bCat, units, sqft, yBuilt, price, sDate . \\
NYC\_Rolling\_Sales(
  sId,
  bName,
  nName,
  bCat,
  units,
  sqft,
  yBuilt,
  price,
  sDate
)
\rightarrow
partOf(Hash(nName), Hash(bName))
```

```math
\langle
  \{(nId, bId) \mid
    \exists sId, bCat, units, sqft, yBuilt, price, sDate .
    NYC\_Rolling\_Sales(
      sId,
      bName,
      nName,
      bCat,
      units,
      sqft,
      yBuilt,
      price,
      sDate
    )
    \land nId = Hash(nName)
    \land bId = Hash(bName)
  \},
  \;
  \{(nId, bId) \mid
    partOf(nId, bId)
  \}
\rangle
```

## locatedIn

_(Union of mappings for Sales, Listings, and Hosts)_

### Mapping PropertySale → Neighborhood

```math
\forall sId, nName . \\
\exists bName, bCat, units, sqft, yBuilt, price, sDate . \\
NYC\_Rolling\_Sales(
  sId,
  bName,
  nName,
  bCat,
  units,
  sqft,
  yBuilt,
  price,
  sDate
)
\rightarrow
locatedIn(sId, Hash(nName))

```

```math
\langle
  \{(sId, nId) \mid
    \exists bName, bCat, units, sqft, yBuilt, price, sDate .
    NYC\_Rolling\_Sales(
      sId,
      bName,
      nName,
      bCat,
      units,
      sqft,
      yBuilt,
      price,
      sDate
    )
    \land nId = Hash(nName)
  \},
  \;
  \{(sId, nId) \mid
    locatedIn(sId, nId)
  \}
\rangle

```

### Mapping AirbnbListing → Neighborhood

```math
\forall lId, nName . \\
\exists sDate, lName, hId, hSince, hLoc, hNeigh, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore, hList, isOut . \\
Airbnb\_Listings(
  lId,
  sDate,
  lName,
  hId,
  hSince,
  hLoc,
  hNeigh,
  nName,
  bName,
  lat,
  lon,
  pType,
  rType,
  cap,
  sqft,
  dPrice,
  minN,
  maxN,
  availYear,
  nRev,
  fRev,
  lRev,
  lScore,
  hList,
  isOut
)
\rightarrow
locatedIn(lId, Hash(nName))

```

```math
\langle
  \{(lId, nId) \mid
    \exists sDate, lName, hId, hSince, hLoc, hNeigh, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore, hList, isOut .
    Airbnb\_Listings(
      lId,
      sDate,
      lName,
      hId,
      hSince,
      hLoc,
      hNeigh,
      nName,
      bName,
      lat,
      lon,
      pType,
      rType,
      cap,
      sqft,
      dPrice,
      minN,
      maxN,
      availYear,
      nRev,
      fRev,
      lRev,
      lScore,
      hList,
      isOut
    )
    \land nId = Hash(nName)
  \},
  \;
  \{(lId, nId) \mid
    locatedIn(lId, nId)
  \}
\rangle

```

### Mapping AirbnbHost → Neighborhood

```math
\forall hId, hNeigh . \\
\exists lId, sDate, lName, hSince, hLoc, nName, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore, hList, isOut . \\
Airbnb\_Listings(
  lId,
  sDate,
  lName,
  hId,
  hSince,
  hLoc,
  hNeigh,
  nName,
  bName,
  lat,
  lon,
  pType,
  rType,
  cap,
  sqft,
  dPrice,
  minN,
  maxN,
  availYear,
  nRev,
  fRev,
  lRev,
  lScore,
  hList,
  isOut
)
\rightarrow
locatedIn(hId, Hash(hNeigh))

```

```math
\langle
  \{(hId, nId) \mid
    \exists lId, sDate, lName, hSince, hLoc, nName, bName, lat, lon, pType, rType, cap, sqft, dPrice, minN, maxN, availYear, nRev, fRev, lRev, lScore, hList, isOut .
    Airbnb\_Listings(
      lId,
      sDate,
      lName,
      hId,
      hSince,
      hLoc,
      hNeigh,
      nName,
      bName,
      lat,
      lon,
      pType,
      rType,
      cap,
      sqft,
      dPrice,
      minN,
      maxN,
      availYear,
      nRev,
      fRev,
      lRev,
      lScore,
      hList,
      isOut
    )
    \land nId = Hash(hNeigh)
  \},
  \;
  \{(hId, nId) \mid
    locatedIn(hId, nId)
  \}
\rangle

```

### Mapping CriminalComplaint → Neighborhood 

_(Derived from Geolocation)_

```math
\forall cId, lat, lon . \\
\exists bName, cDate, offStat, offLvl, premPos, offType, premType, vSex, vAge . \\
NYPD\_Complaints(
  cId,
  bName,
  cDate,
  offStat,
  offLvl,
  premPos,
  offType,
  premType,
  vSex,
  vAge,
  lat,
  lon
)
\rightarrow
locatedIn(cId, Hash(GetNeighName(lat, lon)))
```

```math
\langle
  \{(cId, nId) \mid
    \exists bName, cDate, offStat, offLvl, premPos, offType, premType, vSex, vAge, lat, lon .
    NYPD\_Complaints(
      cId,
      bName,
      cDate,
      offStat,
      offLvl,
      premPos,
      offType,
      premType,
      vSex,
      vAge,
      lat,
      lon
    ) 
    \land nId = Hash(GetNeighName(lat, lon))
  \},
  \;
  \{(cId, nId) \mid
    locatedIn(cId, nId)
  \}
\rangle
```