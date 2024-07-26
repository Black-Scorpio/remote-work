# Cafe Management Web Application

This Flask web application allows users to manage a list of cafes, including viewing, adding, and deleting cafes. The application uses an SQLite database to store cafe information and includes a web interface for managing the cafes.

## Features

- Display a list of cafes with details such as location, number of seats, amenities, and coffee price.
- Add new cafes through a web form.
- Delete existing cafes from the list.
- Filter cafes by location.

## Prerequisites

- Python 3.x
- Flask
- Flask-Bootstrap-5
- Flask-SQLAlchemy

## Installation

1. **Clone & Run:**
   ```bash
   git clone https://github.com/Black-Scorpio/remote-work
   cd remote-work
   
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   
   pip install -r requirements.txt

   python main.py
   
   Open your web browser and navigate to:
   http://127.0.0.1:5000

