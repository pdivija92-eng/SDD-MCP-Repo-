# API Spec: [Endpoint or Service Name]

## Metadata
- **ID:** API-XXX
- **Status:** Draft | Review | Approved | Implemented
- **Author:**
- **Created:** YYYY-MM-DD

---

## Overview
<!-- What this API does -->

## Base URL
```
https://api.example.com/v1
```

---

## Endpoints

### `METHOD /path`

**Description:** 

**Request**
```json
{
  "field": "type"
}
```

**Response (200)**
```json
{
  "field": "type"
}
```

**Error Responses**
| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_INPUT | |
| 404 | NOT_FOUND | |

---

## Data Models

### ModelName
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier |

---

## Authentication
<!-- Auth method: Bearer token, API key, etc. -->

## Rate Limits
<!-- Limits and throttling behavior -->
