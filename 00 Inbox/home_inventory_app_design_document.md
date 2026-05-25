# Personal Home Inventory App Design Document

## 1. Overview

This document describes the design for a personal home inventory application focused initially on pantry inventory. The app allows a user to scan product barcodes, identify products, track item quantities, and record expiration dates. When barcode scanning fails or a product cannot be resolved, the app supports fallback workflows such as manual entry, OCR, and image-assisted identification.

The core design principle is to separate **barcode scanning** from **product lookup** and **inventory management**. A barcode scanner should only decode the barcode value. Product metadata should be resolved through a backend lookup service with caching, provider fallbacks, and user corrections. Inventory state should be stored separately from product identity because multiple units of the same product may have different quantities, locations, and expiration dates.

## 2. Goals

### 2.1 Primary Goals

- Scan pantry item barcodes using a phone or web camera.
- Resolve barcodes into product metadata such as product name, brand, category, and image.
- Track inventory quantity by product and storage location.
- Track expiration dates per inventory lot.
- Provide a clean display of current pantry contents.
- Allow user correction when barcode lookup data is missing or incorrect.
- Cache product lookup results to reduce API usage and improve reliability.

### 2.2 Secondary Goals

- Support OCR-assisted expiration date capture.
- Support item-photo fallback when barcode scanning fails.
- Support estimated expiration dates based on product category.
- Support richer GS1 barcode formats where expiration and lot data may be encoded.
- Support future household-level sharing or multi-user inventory.

### 2.3 Non-Goals for Initial Version

- Fully automatic expiration date extraction for all products.
- Perfect universal product recognition from images.
- Retail price comparison.
- Grocery ordering integration.
- Nutrition planning or meal planning.
- Enterprise-scale inventory management.

## 3. Key Design Assumptions

Most consumer pantry barcodes encode a product identifier, usually a UPC, EAN, or GTIN-like value. They generally do not encode expiration dates, lot numbers, quantity, or storage state.

Therefore:

- Barcode scanning identifies the product.
- Expiration dates are captured manually, through OCR, or through GS1 parsing when available.
- Quantity is application state, not product metadata.
- Product lookup data should be treated as imperfect and user-correctable.

## 4. System Architecture

### 4.1 Recommended High-Level Architecture

```text
Mobile/Web Client
    |
    | scan barcode / capture image / edit inventory
    v
Backend API
    |
    | lookup barcode, normalize metadata, cache results
    v
Product Lookup Providers
    - Local product cache
    - User-corrected mappings
    - Open Food Facts
    - Commercial barcode APIs
    - OCR/image fallback pipeline

Database
    - Products
    - Inventory items/lots
    - Barcode lookup attempts
    - User corrections
```

### 4.2 Recommended Stack

```text
Frontend:
  React Native / Expo, or PWA

Scanner:
  Native mobile barcode scanner, ML Kit, Apple Vision, or ZXing JS

Backend:
  FastAPI
  httpx
  SQLAlchemy / SQLModel

Database:
  SQLite for personal/local deployment
  PostgreSQL for hosted or multi-user deployment

Product lookup:
  Open Food Facts first
  Optional commercial barcode API fallback
  Local user correction table as highest-priority source
```

## 5. Barcode Scanning Design

### 5.1 Scanner Responsibility

The scanner component should only return:

```text
raw_value
barcode_format
scan_timestamp
optional image/frame metadata
```

It should not be responsible for resolving product metadata.

### 5.2 Barcode Formats to Support

Initial support should include:

- UPC-A
- UPC-E
- EAN-13
- EAN-8
- QR Code
- Data Matrix
- Code 128 / GS1-128, if supported by scanner library

### 5.3 Barcode Normalization

Barcode values should be normalized before lookup:

- Strip non-digit characters for numeric product codes.
- Preserve raw scanned value separately.
- Support UPC-A/EAN-13 equivalents, such as UPC-A represented as EAN-13 with a leading zero.
- Record barcode format to support GS1-specific parsing.

Example:

```text
UPC-A:  036000291452
EAN-13: 0036000291452
```

Both may refer to the same product depending on source representation.

## 6. Product Lookup Design

### 6.1 Lookup Cascade

Product resolution should use a provider cascade:

```text
1. User-corrected barcode mapping
2. Local product cache
3. Open Food Facts
4. Commercial barcode API fallback
5. OCR/search fallback
6. Manual entry
```

User-corrected mappings should take precedence over remote providers because they reflect known-good data for this specific user.

### 6.2 Provider Interface

Each lookup provider should implement the same interface:

```python
class BarcodeProvider:
    name: str

    async def lookup(self, barcode: str) -> ProductLookup | None:
        raise NotImplementedError
```

The backend should iterate through providers until a result is found.

### 6.3 Product Lookup Result

Normalized product lookup results should use a consistent shape regardless of provider:

```python
class ProductLookup(BaseModel):
    barcode: str
    name: str | None = None
    brand: str | None = None
    image_url: str | None = None
    category: str | None = None
    source: str
    confidence: float = 0.0
    raw: dict[str, Any] | None = None
```

### 6.4 Provider Strategy

#### Open Food Facts

Use as the primary source for food and pantry products. It can provide product name, brand, category, images, ingredients, nutrition, allergens, and labels.

#### Commercial Barcode APIs

Use as optional fallbacks for better coverage. Candidate providers include UPCitemdb, Barcode Lookup, Go-UPC, and EAN-oriented databases.

Commercial provider responses should be cached because they may be rate-limited, paid, or inconsistent.

#### Local Corrections

Users must be able to correct incorrect product matches. A corrected mapping should be stored locally and preferred in all future lookups.

## 7. Inventory Model

### 7.1 Product vs Inventory Item

Product identity and inventory state must be separate.

A product represents a canonical item:

```text
Campbell's Tomato Soup, 10.75 oz can
```

An inventory item or inventory lot represents the user's possession of that product:

```text
3 cans, pantry shelf, expires 2026-10-15
```

This distinction matters because two units of the same product may have different expiration dates.

### 7.2 Proposed Tables

```sql
products (
    id uuid primary key,
    barcode text unique,
    gtin text,
    name text not null,
    brand text,
    image_url text,
    category text,
    source text,
    source_confidence real,
    created_at timestamp,
    updated_at timestamp
);

inventory_items (
    id uuid primary key,
    product_id uuid references products(id),
    location text,
    quantity numeric not null,
    unit text,
    expiration_date date,
    expiration_source text,
    opened boolean default false,
    notes text,
    added_at timestamp,
    consumed_at timestamp
);

barcode_lookup_attempts (
    id uuid primary key,
    barcode text,
    barcode_format text,
    provider text,
    status text,
    raw_response jsonb,
    created_at timestamp
);

product_corrections (
    id uuid primary key,
    barcode text unique,
    product_id uuid references products(id),
    corrected_name text,
    corrected_brand text,
    corrected_category text,
    corrected_image_url text,
    created_at timestamp,
    updated_at timestamp
);
```

### 7.3 Expiration Source

Expiration dates should include provenance:

```text
explicit_user_entered
ocr_detected
gs1_encoded
estimated
unknown
```

This allows the UI to communicate confidence and avoid presenting estimated dates as authoritative.

## 8. Expiration Date Handling

### 8.1 Initial MVP Approach

Expiration dates should be manually entered during item addition.

Example flow:

```text
Found: Campbell's Tomato Soup
Quantity: [1]
Expiration: [date picker] [unknown] [estimate]
```

### 8.2 Estimated Expiration Dates

The app may offer category-based default expiration estimates:

```text
canned goods -> 18 months
pasta/rice -> 24 months
spices -> 24 months
snacks -> 6 months
```

Estimated dates must be marked as estimated.

### 8.3 OCR-Assisted Expiration Capture

A later version can allow the user to photograph the expiration date. OCR should extract candidate dates and ask the user to confirm.

Examples of supported date formats:

```text
BEST BY 05/23/26
EXP 2026-05-23
BB 23 MAY 26
LOT A123 EXP 052326
```

The OCR parser should return:

```text
candidate_date
confidence
matched_text
requires_confirmation
```

### 8.4 GS1 Application Identifier Parsing

Some 2D or logistics barcodes may encode expiration and lot information using GS1 Application Identifiers.

Relevant fields include:

```text
AI 17 -> expiration date, YYMMDD
AI 15 -> best-before date, YYMMDD
AI 10 -> batch or lot number
```

When the scanner returns QR Code, Data Matrix, or GS1-128 values, the backend should attempt GS1 parsing before falling back to ordinary lookup.

## 9. Fallback Identification Workflows

### 9.1 OCR Label Fallback

If barcode scanning fails, the user may photograph the front label. OCR can extract text such as:

```text
Barilla Penne Rigate 16 oz
```

The backend can use this text to search product APIs or suggest a likely manual entry.

### 9.2 Image Classification Fallback

Image classification may identify broad item categories such as:

```text
canned beans
box of cereal
bottle of olive oil
```

This should be treated as an assistive feature only. The user should confirm or edit the result before saving.

### 9.3 Manual Entry

Manual entry must always be available. It is the final fallback and should also allow the user to associate the manually entered product with the scanned barcode for future use.

## 10. Core User Flows

### 10.1 Add Item by Barcode

```text
User scans barcode
    -> client decodes barcode locally
    -> client sends barcode and format to backend
    -> backend checks user correction table
    -> backend checks local product cache
    -> backend queries remote providers
    -> backend returns product candidate
    -> user confirms or edits product
    -> user enters quantity and expiration date
    -> inventory lot is created
```

### 10.2 Add Item When Barcode Lookup Fails

```text
User scans barcode
    -> no product match found
    -> app offers options:
        - search by label photo
        - enter manually
        - retry scan
    -> user creates product manually
    -> app stores barcode-to-product correction
    -> inventory lot is created
```

### 10.3 Update Quantity

```text
User opens pantry inventory
    -> selects product or inventory lot
    -> increments/decrements quantity
    -> app updates inventory item
    -> if quantity reaches zero, item is marked consumed or removed
```

### 10.4 Expiration Review

```text
User opens expiration dashboard
    -> app groups items by expiration window:
        - expired
        - expires this week
        - expires this month
        - no expiration date
    -> user consumes, edits, or dismisses items
```

## 11. API Design

### 11.1 Barcode Lookup

```http
GET /barcode/{barcode}
```

Returns a normalized product lookup result.

### 11.2 Add Inventory Item

```http
POST /inventory-items
```

Example request:

```json
{
  "product_id": "uuid",
  "quantity": 3,
  "unit": "each",
  "location": "pantry",
  "expiration_date": "2026-10-15",
  "expiration_source": "explicit_user_entered",
  "opened": false,
  "notes": null
}
```

### 11.3 Search Inventory

```http
GET /inventory-items?query=beans&location=pantry
```

### 11.4 Update Inventory Item

```http
PATCH /inventory-items/{id}
```

### 11.5 Create Product Correction

```http
POST /product-corrections
```

Example request:

```json
{
  "barcode": "036000291452",
  "product_id": "uuid",
  "corrected_name": "Example Product Name",
  "corrected_brand": "Example Brand"
}
```

## 12. Backend Lookup Service Example

```python
from __future__ import annotations

from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class ProductLookup(BaseModel):
    barcode: str
    name: str | None = None
    brand: str | None = None
    image_url: str | None = None
    category: str | None = None
    source: str
    confidence: float = 0.0
    raw: dict[str, Any] | None = None


def normalize_barcode(barcode: str) -> str:
    digits = "".join(ch for ch in barcode if ch.isdigit())
    if not 6 <= len(digits) <= 14:
        raise ValueError("Barcode must be 6-14 digits")
    return digits


async def lookup_open_food_facts(barcode: str) -> ProductLookup | None:
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(
            url,
            headers={
                "User-Agent": "HomeInventoryApp/0.1 contact@example.com",
            },
        )
        response.raise_for_status()
        data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    name = (
        product.get("product_name")
        or product.get("generic_name")
        or product.get("abbreviated_product_name")
    )

    brand = product.get("brands")
    image_url = product.get("image_front_url") or product.get("image_url")
    category = product.get("categories")

    return ProductLookup(
        barcode=barcode,
        name=name,
        brand=brand,
        image_url=image_url,
        category=category,
        source="open_food_facts",
        confidence=0.85 if name else 0.5,
        raw=product,
    )


@app.get("/barcode/{barcode}", response_model=ProductLookup)
async def lookup_barcode(barcode: str) -> ProductLookup:
    try:
        normalized = normalize_barcode(barcode)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # 1. Check user-corrected barcode mappings.
    # corrected_product = await get_corrected_product_by_barcode(normalized)
    # if corrected_product:
    #     return corrected_product

    # 2. Check local product cache.
    # cached_product = await get_product_by_barcode(normalized)
    # if cached_product:
    #     return cached_product

    # 3. Try Open Food Facts.
    product = await lookup_open_food_facts(normalized)
    if product:
        # await save_product_cache(product)
        return product

    # 4. Try commercial provider fallback.
    # product = await lookup_commercial_provider(normalized)
    # if product:
    #     return product

    raise HTTPException(
        status_code=404,
        detail="No product found for this barcode",
    )
```

## 13. UI Design Considerations

### 13.1 Inventory Display

The main inventory screen should show:

- Product image
- Product name
- Brand
- Quantity
- Location
- Nearest expiration date
- Expiration status indicator

Useful grouping modes:

- By location
- By category
- By expiration date
- By recently added
- By low quantity

### 13.2 Product Detail View

A product detail page should show:

- Product metadata
- Barcode
- All inventory lots for that product
- Quantity by lot
- Expiration dates by lot
- Edit/correction controls

### 13.3 Expiration Dashboard

The app should include an expiration-focused dashboard:

```text
Expired
Expiring this week
Expiring this month
Unknown expiration
```

### 13.4 Correction UX

When lookup data is wrong, the user should be able to edit:

- Name
- Brand
- Category
- Product image
- Unit size

The correction should be saved and reused on future scans.

## 14. Data Quality and Reliability

### 14.1 Caching

All external lookup responses should be cached. Store both raw provider responses and normalized product data.

### 14.2 Provider Failures

Remote lookup failure should not block inventory entry. The app should gracefully offer manual entry.

### 14.3 Confidence Scores

Each product lookup should carry confidence metadata. For example:

```text
0.95 -> user-corrected mapping
0.85 -> strong Open Food Facts match with product name and brand
0.60 -> product name only
0.40 -> OCR/image-derived candidate
```

Low-confidence results should require explicit confirmation.

## 15. Security and Privacy

For a personal app, the security model can start simple but should still account for:

- Authentication if hosted remotely.
- Private storage of household inventory data.
- Avoiding unnecessary image uploads.
- Keeping barcode scanning local on-device when possible.
- Storing only required product metadata.
- Hiding or protecting API keys for commercial barcode providers on the backend.

## 16. Implementation Phases

### Phase 1: MVP

- Barcode scanning in client.
- FastAPI barcode lookup endpoint.
- Open Food Facts provider.
- Product cache.
- Manual quantity and expiration entry.
- Inventory list and detail pages.
- Basic search/filter.

### Phase 2: Data Quality and UX

- User product corrections.
- Commercial barcode API fallback.
- Expiration dashboard.
- Location/category grouping.
- UPC/EAN normalization improvements.
- Scan history and lookup diagnostics.

### Phase 3: Assisted Capture

- OCR-based expiration date detection.
- Label OCR fallback for failed barcode scans.
- Product search from OCR text.
- Confidence scoring and confirmation UI.

### Phase 4: Advanced Features

- GS1 Application Identifier parser.
- Household sharing.
- Low-stock alerts.
- Shopping list integration.
- Meal planning or recipe integration.
- Offline-first mode with sync.

## 17. Open Questions

- Should the app be mobile-native, PWA, or both?
- Is this intended to be single-user only or household-shared?
- Should the app support offline-first operation?
- Should inventory quantities be strict numeric counts, flexible units, or both?
- Should the app support non-food household inventory later?
- How much manual data correction is acceptable during initial use?

## 18. Recommended Initial Build Path

The recommended first implementation is:

```text
1. Build a FastAPI backend with Product and InventoryItem models.
2. Add Open Food Facts barcode lookup.
3. Add local product caching.
4. Build a simple scan-to-add flow in the frontend.
5. Require manual expiration date entry.
6. Add product correction support before adding more lookup providers.
7. Add OCR expiration capture only after the manual workflow feels solid.
```

This path minimizes technical risk while preserving a clean architecture for future enhancements.

