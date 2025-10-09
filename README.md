# SmartRent-Backend 🏠🔐

## 🧠 Core Purpose
The **SmartRent-Backend** repository houses the core API, business logic, and data models for the SmartRent ecosystem. It acts as the brain and the secure data layer, managing user authentication, property listings, verification logic, and transaction processing.

## 🛠️ Technology Stack
* **Language:** Python 3.10+
* **Framework:** Django 4.x
* **API:** Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Containerization:** Docker (recommended for deployment/local setup)
* **Version Control:** Git

## ✨ Key Features (MVP)
1.  **User Authentication:** JWT-based signup and login for Tenants and Landlords/Agents.
2.  **Property Management:** CRUD operations for verified property listings.
3.  **Verification Logic:** API endpoints to handle submission and status of verification documents.
4.  **Transaction API:** Integration layer for Paystack/Flutterwave for secure escrow simulation.
5.  **ML Integration:** Endpoint to consume predictions from the `SmartRent-ML-Service`.

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Poetry or Pip/Pipenv
* Docker & Docker Compose (optional but recommended)
* PostgreSQL running locally or accessible via URL.

### 2. Local Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/SmartRent-Backend.git](https://github.com/yourusername/SmartRent-Backend.git)
    cd SmartRent-Backend
    ```
2.  **Setup Virtual Environment & Install Dependencies:**
    ```bash
    # Using Poetry
    poetry install
    poetry shell
    ```
3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory with necessary settings (Database credentials, Secret Key, Payment Gateway credentials).
    ```ini
    # .env example
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    DATABASE_URL=postgres://user:password@host:port/dbname
    PAYSTACK_SECRET_KEY=sk_...
    ML_SERVICE_URL=http://localhost:8001/
    ```
4.  **Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

The API should now be running at `http://localhost:8000/`.

## 🗺️ API Documentation
**(To be added: Link to Swagger/Redoc documentation once endpoints are defined)**

## 🧪 Testing
```bash
python manage.py test
