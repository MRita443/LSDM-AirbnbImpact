# Global Schema Formal Constraints & Axioms

This document defines the Global Schema ($G$) of the Information Integration System $J = \langle G, M, S \rangle$ as a logical theory over the relational alphabet $A_G$.

## 1. Equality Generating Dependencies (EGDs)
In the ontology, EGDs are implemented via `owl:hasKey`. These axioms state that if two entities of the same class share the same identifier, they must be the same individual (i.e., they must share all other attribute values).

### **Neighborhood Identity**
* **Logic:** Ensures the hashing mechanism for neighborhood names does not produce collisions.
$$\forall n, name_1, name_2 . (Neighborhood(n) \land neighborhood\_id(n, id) \land name(n, name_1) \land name(n, name_2)) \rightarrow (name_1 = name_2)$$

### **Criminal Complaint Identity**
* **Logic:** Validates that a police report ID uniquely identifies a single occurrence.
$$\forall c, type_1, type_2 . (CriminalComplaint(c) \land complaint\_id(c, id) \land offense\_type(c, type_1) \land offense\_type(c, type_2)) \rightarrow (type_1 = type_2)$$

### **PropertySale Identity**
* **Logic:** Ensures a single transaction ID uniquely determines its financial and structural attributes.
$$\forall s, p_1, p_2 . (PropertySale(s) \land sale\_id(s, id) \land sale\_price(s, p_1) \land sale\_price(s, p_2)) \rightarrow (p_1 = p_2)$$

### **Borough Identity**
* **Logic:** Ensures the borough ID uniquely identifies the administrative district name.
$$\forall b, n_1, n_2 . (Borough(b) \land borough\_id(b, id) \land name(b, n_1) \land name(b, n_2)) \rightarrow (n_1 = n_2)$$

### **AirbnbHost Identity**
* **Logic:** Uniquely identifies a host to prevent contradictory residence flags (e.g., inside vs outside NYC).
$$\forall h, l_1, l_2 . (AirbnbHost(h) \land host\_id(h, id) \land host\_location(h, l_1) \land host\_location(h, l_2)) \rightarrow (l_1 = l_2)$$

---

## 2. Functional Properties (Uniqueness Constraints)
Functional properties are a specific subset of EGDs where a relationship can point to at most one target. In the TTL ontology, these are marked with `owl:FunctionalProperty`.

### **Spatial Location Uniqueness (`locatedIn`)**
* **Logic:** A physical entity (listing, sale, or crime) cannot be located in two different places simultaneously.
$$\forall x, y, z . (locatedIn(x, y) \land locatedIn(x, z)) \rightarrow (y = z)$$

### **Administrative Hierarchy (`partOf`)**
* **Logic:** A neighborhood belongs to exactly one borough.
$$\forall n, b_1, b_2 . (partOf(n, b_1) \land partOf(n, b_2)) \rightarrow (b_1 = b_2)$$

---

## 3. Negative Constraints (Disjointness)
Negative constraints prevent logical contradictions by asserting that certain classes share no members. This is important when merging distinct datasets where IDs might overlap. These are marked with `owl:AllDisjointClasses`

### **Class Disjointness**
* **Logic:** An entity cannot belong to more than one of these primary classes.
$$(AirbnbListing \cap CriminalComplaint = \emptyset)$$
$$(AirbnbListing \cap PropertySale = \emptyset)$$
$$(AirbnbListing \cap AirbnbHost = \emptyset)$$
$$(CriminalComplaint \cap PropertySale = \emptyset)$$
$$(CriminalComplaint \cap AirbnbHost = \emptyset)$$
$$(PropertySale \cap AirbnbHost = \emptyset)$$

---

## 4. Domain and Range Constraints (Typing)
These axioms ensure that relationships connect the correct types of objects as defined in the Global Schema alphabet.

### **Ownership Typing (`owns`)**
* **Logic:** Only an Airbnb Host can own an Airbnb Listing.
$$\forall x, y . owns(x, y) \rightarrow (AirbnbHost(x) \land AirbnbListing(y))$$

### **Location Typing (`locatedIn`)**
* **Logic:** The destination of a location relationship must be a "Place" (Borough or Neighborhood).
$$\forall x, y . locatedIn(x, y) \rightarrow Place(y)$$

### **Administrative Hierarchy (`partOf`)**
* **Logic:** Ensures that the relationship correctly connects a Neighborhood entity to a Borough entity.
$$\forall x, y . partOf(x, y) \rightarrow (Neighborhood(x) \land Borough(y))$$