# Project Name

This project provides a set of APIs for managing vendors, purchase orders, and historical performance records.

## Overview

This project is built using Django and Django Rest Framework (DRF) for creating RESTful APIs. It includes endpoints for user authentication, managing vendors, purchase orders, and retrieving historical performance data.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd project-directory
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run migrations:

    ```bash
    python manage.py migrate
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Authentication

- **Endpoint**: `/login/`
  - Method: `POST`
  - Description: User login endpoint.
  
- **Endpoint**: `/register/`
  - Method: `POST`
  - Description: User registration endpoint.
  
- **Endpoint**: `/token/`
  - Method: `POST`
  - Description: Obtain JWT token pair (access and refresh tokens).
  
- **Endpoint**: `/token/refresh/`
  - Method: `POST`
  - Description: Refresh JWT token pair.

### Vendor APIs

- **Endpoint**: `/api/vendors/`
  - Method: `GET`, `POST`
  - Description: Get a list of vendors or create a new vendor.

- **Endpoint**: `/api/vendors/<vendor_id>/`
  - Method: `GET`, `PUT`, `DELETE`
  - Description: Retrieve, update, or delete a specific vendor.

### Purchase Order APIs

- **Endpoint**: `/api/purchase_orders/`
  - Method: `GET`, `POST`
  - Description: Get a list of purchase orders or create a new purchase order.

- **Endpoint**: `/api/purchase_orders/<po_id>/`
  - Method: `GET`, `PUT`, `DELETE`
  - Description: Retrieve, update, or delete a specific purchase order.

- **Endpoint**: `/api/purchase_orders/<po_id>/acknowledge/`
  - Method: `PUT`
  - Description: Acknowledge a purchase order.

### Performance APIs

- **Endpoint**: `/api/vendors/<vendor_id>/performance/`
  - Method: `GET`
  - Description: Retrieve historical performance of a vendor.

## Usage

You can use tools like Postman or cURL to interact with the APIs provided by this project. Make sure to authenticate using JWT tokens before accessing protected endpoints.
