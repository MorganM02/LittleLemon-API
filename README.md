# Little Lemon API

A restaurant management REST API built with Django and Django REST Framework.

## Overview

Little Lemon is a backend API that provides functionality for managing a restaurant's menu, customers, carts, orders, and delivery crew.

The project was built as an independent backend development project while completing the Meta Back-End Developer Professional Certificate.

## Technologies

- Python
- Django
- Django REST Framework
- Djoser
- django-filter
- SQLite
- Pipenv

## Features

- User registration and authentication
- Role-based permissions
- Customer, Manager, and Delivery Crew roles
- Menu item and category management
- Shopping cart functionality
- Order creation and management
- Delivery crew order assignment
- Filtering, pagination, and ordering
- API testing

## API Functionality

The API supports workflows including:

- Customer registration and login
- Browsing menu items and categories
- Filtering and ordering menu items
- Adding and retrieving cart items
- Placing orders
- Viewing customer orders
- Managers assigning orders to delivery crew
- Delivery crew viewing assigned orders
- Updating order delivery status

## Testing

The API was tested through complete user workflows, including authentication, permissions, menu access, cart operations, ordering, and delivery workflows.

## Running the Project

1. Clone the repository.
2. Install the dependencies using Pipenv.
3. Activate the virtual environment.
4. Run the Django development server.

```bash
python manage.py runserver
