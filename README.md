# Django Custom User, Category, and Product API

This project is a Django-based application that includes a custom user model, a category model, and a product model. It provides RESTful API endpoints for managing users, categories, and products. The application uses JSON Web Tokens (JWT) for authentication and supports integration with Swagger for API documentation.

## Features

- **Custom User Model**
  - Email-based authentication.
  - Password validation and hashing.
  - Phone number validation using regular expressions.
  
- **Category Management**
  - Create, retrieve, update, and delete categories.
  - List all categories.

- **Product Management**
  - Create, retrieve, update, and delete products.
  - List all products or products filtered by category.

- **Authentication**
  - JWT-based authentication for secure access.
  - Admin-only access for sensitive operations like creating, updating, and deleting resources.

- **API Documentation**
  - Swagger/OpenAPI integration for easy exploration of API endpoints.