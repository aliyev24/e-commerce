# e-commerce
<div align='center'>
 
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square)
![DjangoRestFramework](https://img.shields.io/badge/-Django%20Rest%20-880808?logo=django&logoColor=white&style=flat-square)
![Celery](https://img.shields.io/badge/-Celery-37814A?logo=celery&logoColor=white&style=flat-square)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-3776AB?logo=postgresql&logoColor=white&style=flat-square)
![Redis](https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white&style=flat-square)
![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat-square)
![PayPal](https://img.shields.io/badge/-PayPal-00457C?logo=paypal&logoColor=white&style=flat-square) </div>

E-commerce with categories, products, shooping cart and payment.

### Features
- [x] **PayPal** payment integration
- [x] Shopping Cart
- [x] Adding products to Cart
- [x] **Search** for products
- [x] Sending email notifications to users
- [x] Total Cart price calculation
- [x] Unit Testing

_ _ _ _ _ _ _ _ _ _ _
### Installation

1. Create '.env' file in settings.py root and paste this:

 ```
DEBUG=0
SECRET_KEY=your_secret_key

POSTGRES_NAME=your_postgres_name
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
   ```
2. Create a docker image and run:

```
docker-compose up --build
```
