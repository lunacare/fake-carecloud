# Fake CareCloud API

A mock implementation of the CareCloud API for testing purposes. This lightweight FastAPI server emulates the core CareCloud endpoints to support testing of integrations without requiring access to the real CareCloud API.

## Features

- **Authentication**: Simple token-based authentication
- **Patient Management**: Create, search, and retrieve patients
- **Provider/Location Management**: List providers, locations, appointment resources, and visit reasons
- **Appointment Management**: Create, read, update, and cancel appointments
- **Auto-initialization**: Database and seed data created on first startup
- **API Documentation**: Automatic OpenAPI docs at `/docs`

## Quick Start

### Option 1: Using direnv (Recommended)

1. **Install direnv** (if not already installed)
   ```bash
   # On Ubuntu/Debian
   sudo apt install direnv
   
   # On macOS
   brew install direnv
   ```

2. **Setup the project**
   ```bash
   cd fake_carecloud
   python -m venv venv  # Create virtual environment
   source venv/bin/activate && pip install -r requirements.txt  # Install dependencies
   direnv allow  # Load environment variables
   ```

3. **Run the Server**
   ```bash
   python app.py
   ```

### Option 2: Manual Setup

1. **Create Virtual Environment**
   ```bash
   cd fake_carecloud
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```bash
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

### Access the API
- API Base URL: `http://localhost:7000/v2`
- API Documentation: `http://localhost:7000/docs`
- Health Check: `http://localhost:7000/health`

## Usage Example

Based on the original notebook workflow:

### 1. Get Access Token

**Option A: Form Data (matches original CareCloud)**
```bash
curl -X POST "http://localhost:7000/oauth2/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=dummy"
```

**Option B: JSON**
```bash
curl -X POST "http://localhost:7000/oauth2/access_token" \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "refresh_token", "refresh_token": "dummy"}'
```

### 2. Create/Search Patient
```bash
# Search for existing patient
curl -X POST "http://localhost:7000/v2/patients/search" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1970-01-01"
    }
  }'

# Create new patient if not found
curl -X POST "http://localhost:7000/v2/patients" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": {
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1970-01-01"
    },
    "addresses": [{
      "line1": "123 Main St",
      "city": "Lyons",
      "state": "CO",
      "zip_code": "80540",
      "country_name": "USA",
      "is_primary": true
    }],
    "phones": [{
      "phone_number": "303-867-5309",
      "phone_type_code": "M",
      "is_primary": true
    }]
  }'
```

### 3. Get Available Resources
```bash
# Get providers
curl -X GET "http://localhost:7000/v2/providers" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get locations  
curl -X GET "http://localhost:7000/v2/locations" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get appointment resources
curl -X GET "http://localhost:7000/v2/appointment_resources" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get visit reasons
curl -X GET "http://localhost:7000/v2/visit_reasons" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Create Appointment
```bash
curl -X POST "http://localhost:7000/v2/appointments" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "appointment": {
      "start_time": "2025-07-10T13:00:00",
      "end_time": "2025-07-10T13:30:00",
      "provider_id": 40483,
      "location_id": 55491,
      "visit_reason_id": 119104,
      "resource_id": 37367,
      "patient": {
        "id": "37d480d1-fe7d-4600-bbb1-bd79367e418d"
      }
    }
  }'
```

## Seed Data

The API comes pre-loaded with sample data matching the original CareCloud notebook:

- **Provider**: Dr. Kris Duggan (ID: 40483)
- **Location**: Luna Care Physical Therapy (ID: 55491)
- **Resource**: Dr. Kris Duggan (ID: 37367)
- **Visit Reasons**: Initial, Standard, Progress, Re-evaluation, Discharge visits
- **Sample Patient**: John Doe (ID: 37d480d1-fe7d-4600-bbb1-bd79367e418d)

## Database

The API uses SQLite with the database file `carecloud.db` created automatically in the project directory. You can inspect or modify the database using any SQLite client.

## API Endpoints

### Authentication
- `POST /v2/oauth2/access_token` - Get access token

### Patients
- `POST /v2/patients` - Create patient
- `POST /v2/patients/search` - Search patients
- `GET /v2/patients/{id}` - Get patient by ID

### Resources
- `GET /v2/providers` - List providers
- `GET /v2/locations` - List locations
- `GET /v2/appointment_resources` - List appointment resources
- `GET /v2/visit_reasons` - List visit reasons

### Appointments
- `POST /v2/appointments` - Create appointment
- `GET /v2/appointments/{id}` - Get appointment
- `PUT /v2/appointments/{id}` - Update appointment
- `DELETE /v2/appointments/{id}` - Cancel appointment

## Configuration

The API can be configured using environment variables:

- `FAKE_CARECLOUD_HOST` - Server host (default: "0.0.0.0")
- `FAKE_CARECLOUD_PORT` - Server port (default: "8000")  
- `FAKE_CARECLOUD_DEBUG` - Enable debug/reload mode (default: "false")
- `DATABASE_URL` - Database connection string (default: "sqlite:///./carecloud.db")
- `API_TITLE` - API title in documentation (default: "Fake CareCloud API")
- `API_VERSION` - API version (default: "1.0.0")

When using direnv, these are automatically set in the `.envrc` file. You can modify them as needed.

## Notes

- This is a **testing tool only** and should not be used in production
- The authentication is simplified and not secure
- All data is stored locally in SQLite
- The API responses match the structure observed in the real CareCloud API
- UUIDs are generated for new patients and appointments to match expected formats

## Integration Testing

This fake API can be used as a drop-in replacement for the real CareCloud API during development and testing by simply changing the base URL from `https://api.carecloud.com/v2` to `http://localhost:7000/v2`.