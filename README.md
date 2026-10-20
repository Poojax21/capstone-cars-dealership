# Cars Dealership – Full Stack Capstone Project

**Repository name:** `capstone-cars-dealership`
**Project name:** Cars Dealership – Full Stack Application Development Capstone

A responsive full-stack web application for **Cars Dealership**, a national car retailer in the U.S.
It displays dealership branches and lets authenticated users view and submit dealer reviews, with
sentiment analysis on review text.

## Tech Stack

- **Backend:** Django (Python), Django REST-style JSON endpoints, SQLite
- **Frontend:** React components + Django templates, Bootstrap/CSS
- **Data:** Dealers, car makes/models and reviews
- **DevOps:** GitHub Actions CI/CD, Docker, Kubernetes, IBM Cloud Code Engine

## Features

- Home page listing all dealerships, filterable by state
- Dealer details page with existing reviews and ratings
- Post a review (logged-in users) with sentiment analysis
- User registration and login/logout
- Admin site for managing dealers, cars and reviews

## Running Locally

```bash
cd server
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Open http://localhost:8000/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/djangoapp/get_dealers/` | All dealers |
| GET | `/djangoapp/get_dealers/<state>` | Dealers in a state |
| GET | `/djangoapp/dealer/<id>` | Dealer details |
| GET | `/djangoapp/reviews/dealer/<id>` | Reviews for a dealer |
| GET | `/djangoapp/get_cars/` | All car makes and models |
| GET | `/djangoapp/analyze/<text>` | Sentiment analysis |
| POST | `/djangoapp/login` | Log in a user |
| POST | `/djangoapp/logout` | Log out the current user |
| POST | `/djangoapp/register` | Register a new user |
