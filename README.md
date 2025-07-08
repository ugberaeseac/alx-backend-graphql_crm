# Understanding GraphQL

A simple CRM (Customer Relationship Management) API built using **Graphene-Django** and **GraphQL**. The system manages **Customers**, **Products**, and **Orders** with full CRUD functionality via GraphQL mutations and queries.

---

## Technologies Used

- Python 3
- Django
- Graphene-Django
- GraphQL
- Postman (for testing)

---

## Features

1. **Customer Management:**
   - Create Customer
   - Bulk Create Customers
   - Query all Customers
   - Query Customer by ID

2. **Product Management:**
   - Create Product
   - Query all Products
   - Query product by ID

3. **Order Management:**
   - Create Order (with Customer and multiple Products)
   - Query All Orders
   - Query Order by ID

---

## Setup Instructions

1. Clone the repository:

```bash
https://github.com/ugberaeseac/alx-backend-graphql_crm.git
cd alx-backend-graphql_crm
```

2. Create and activate virtual environment:

```bash
python -m venv env
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

---

## GraphQL Playground

Visit: `http://localhost:8000/graphql/`

---

## Queries & Mutations

### 1. Customers

#### Create Customer
```graphql
mutation {
  createCustomer(input: {
    name: "John Doe",
    email: "johndoe@demo.com",
    phone: "123-456-7890"
  }) {
    customer {
      customerId
      name
      email
      phone
    }
    message
  }
}
```

#### Bulk Create Customers
```graphql
mutation {
  bulkCreateCustomers(input: [
    { name: "Charles", email: "charles@demo.com", phone: "123-456-7890" },
    { name: "Caroline", email: "caroline@demo.com" }
  ]) {
    customers {
      customerId
      name
      email
    }
    message
  }
}
```

#### Query All Customers
```graphql
query {
  allCustomers {
    customerId
    name
    email
    phone
  }
}
```

---

### 2. Products

#### Create Product
```graphql
mutation {
  createProduct(input: {
    name: "Laptop",
    price: 1500.50,
    stock: 10
  }) {
    product {
      productId
      name
      price
      stock
    }
    message
  }
}
```

#### Query All Products
```graphql
query {
  allProducts {
    productId
    name
    price
    stock
  }
}
```

---

### 3. Orders

#### Create Order
```graphql
mutation {
  createOrder(input: {
    customerId: "customer-uuid",
    productIds: ["product-uuid-1", "product-uuid-2"]
  }) {
    order {
      orderId
      customer {
        name
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
    message
  }
}
```

#### Query All Orders
```graphql
query {
  allOrders {
    orderId
    customer {
      name
    }
    products {
      name
      price
    }
    totalAmount
    orderDate
  }
}
```

---

## Postman Collection

You can also test the API using Postman:

 **Postman Documentation:** [https://documenter.getpostman.com/view/45172601/2sB34eH2J4](https://documenter.getpostman.com/view/45172601/2sB34eH2J4)

---

## Assumptions & Design Decisions

- Unique email is required for each customer.
- Price is stored as `Decimal` for accuracy.
- Orders are associated with customers and multiple products.
- `totalAmount` is computed on-the-fly and not stored in the database.

---

## Future Improvements

- Implement user authentication.
- Add pagination for list queries.
- Handle soft deletion of records.

---

