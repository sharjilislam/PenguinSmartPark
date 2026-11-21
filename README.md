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

## Current Limitations

- Parking lot information is simulated.
- PostgreSQL persistence is not implemented.
- React frontend is not implemented.
- Google Maps integration is not implemented.
- CARLA is not connected to the backend test workflow.
- Automated alerts are not implemented.
- ADA-specific parking recommendations are not implemented.

## Future Improvements

- PostgreSQL database integration
- CARLA gate-event integration
- React frontend
- Google Maps walking directions
- Parking alerts
- Administrative parking management

## Academic Purpose

This project was developed for CSCI 5801 Software Engineering at Youngstown State University.
