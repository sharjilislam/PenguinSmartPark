# Penguin SmartPark

## Project Information

Course: CSCI 5801 - Software Engineering
Institution: Youngstown State University

Team Members:
- Sharjil Islam
- Zenifa Islam Saify

## Project Overview

Penguin SmartPark is a prototype smart parking recommendation system designed for Youngstown State University.

The system recommends parking lots based on user eligibility, available parking spaces, and walking time to a destination.

The current implementation focuses on testable backend functionality using simulated parking lot data.

## Implemented Features

- Parking lot capacity and occupancy management
- Regular and ADA parking space tracking
- Vehicle entry and exit processing
- Parking access validation
- Parking recommendations based on walking time
- Filtering of closed, full, and unauthorized parking lots
- FastAPI backend with basic endpoints
- Automated unit and component tests

## Technologies

- Python 3.13
- FastAPI
- pytest
- Uvicorn

## Installation

1. Install Python 3.13.
2. Download or clone this repository.
3. Open PowerShell in the project directory.

4. Create a virtual environment:

   python -m venv .venv

5. Install the required packages:

   .\.venv\Scripts\python.exe -m pip install -r requirements.txt

## Run the Application

Start the FastAPI backend:

   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload

Open the API documentation:

   http://127.0.0.1:8000/docs

## Run Automated Tests

Run all automated tests:

   .\.venv\Scripts\python.exe -m pytest tests -v

Run unit tests only:

   .\.venv\Scripts\python.exe -m pytest tests/test_parking_lot.py tests/test_availability.py tests/test_recommendation.py tests/test_access.py -v

Run component tests only:

   .\.venv\Scripts\python.exe -m pytest tests/test_component_availability.py tests/test_component_recommendation.py -v

## Testing Summary

Unit tests:
- ParkingLot: 5
- AvailabilityService: 6
- RecommendationService: 6
- AccessService: 5

Component tests:
- Availability component: 3
- Recommendation component: 3

Total: 28 automated tests.

Latest verified result: 28 passed, 0 failed.

## Testing Approach

Automated tests use simulated parking data and in-memory ParkingLot objects.

Tests do not depend on a live database, external API, or CARLA simulator.

## API Endpoints

After starting the application, open `http://127.0.0.1:8000/docs` for interactive API documentation.

- `GET /` - service information
- `GET /health` - health status
- `GET /lots` - simulated parking-lot availability
- `GET /lots/{lot_id}/access?user_type=STUDENT` - access decision for a user type
- `POST /lots/{lot_id}/events` - regular or ADA `ENTER` and `EXIT` events
- `POST /recommendations` - eligible recommendations ranked by walking time

The API uses simulated in-memory lots. Restarting the application restores the original demo data.

## Final Testing Summary

The final suite contains 40 automated tests:

- 22 unit tests across ParkingLot, AvailabilityService, RecommendationService, and AccessService
- 15 component tests across five components: ParkingLot, AvailabilityService, AccessService, RecommendationService, and FastAPI API
- 3 system tests that exercise access, availability updates, recommendation, and an invalid-event failure path through the API

Run the complete suite from the project directory:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

Latest verified result: 40 passed, 1 deprecation warning.


