# Plate Number Recognition System

This is a FastAPI-based application that captures vehicle plate numbers using a webcam and stores the plate number along with the date and time of detection in a SQLite database.

## Features

- 📷 Captures video stream from a webcam using OpenCV  
- 🔍 Detects and validates vehicle plate numbers  
- 🗄️ Saves recognized plate numbers with timestamps to a SQLite database  
- ⚡ Built with FastAPI for high-performance API endpoints  
- 📦 Dependency management with Poetry  

## Tech Stack

- **Backend Framework**: FastAPI  
- **Image Processing**: OpenCV  
- **Database**: SQLite  
- **Dependency Manager**: Poetry  
- **ORM**: SQLAlchemy  

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- Poetry: https://python-poetry.org/docs/#installation

### Installation

```bash
# Clone the repository
git clone https://github.com/Professor-Douel/PlateNumberFromVideoToDatabase.git
cd plate-number-recognition

# Install dependencies
poetry install
```

### Run the Application

```bash
# Activate the virtual environment
poetry shell

# Start the FastAPI server
uvicorn main:app --reload
```

# Start the script file
python service.py

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Start Webcam Plate Number Capture

You can use a separate Python script or background process to:

- Capture frames from the webcam
- Extract plate numbers using OCR or heuristics
- Send valid results to the FastAPI backend via a POST request

Example script:

```python
import cv2
import requests
from datetime import datetime

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    # TODO: process frame to detect plate
    plate_number = "AA1234BB"  # example
    timestamp = datetime.utcnow().isoformat()

    if plate_number:
        requests.post("http://127.0.0.1:8000/plate/", json={
            "plate_number": plate_number,
            "date_created": timestamp
        })

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

> ⚠️ Consider implementing a cooldown mechanism to avoid frequent duplicate entries.

## API Endpoints

- `GET /plates/` – Retrieve all recorded plate numbers
- `GET /plates/{plate_number}` – Retrieve a specific plate number entry  

## Database Schema

**Table: `plate_number`**

| Column       | Type     | Description               |
|--------------|----------|---------------------------|
| id           | Integer  | Primary key               |
| plate_number | String   | Vehicle plate number      |
| date_created | DateTime | Timestamp of detection    |
