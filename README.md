# 🏬 Inventory Management System (v1 → v3)

An evolving, scalable inventory management solution developed in three stages — from a basic single-store prototype to a real-time, production-ready, multi-store architecture using Docker, Redis, PostgreSQL replication, and Celery task processing.

![Stage 3 Docker Deployment](./Stage%203/Output/Docker/Docker.png)

---

## 📚 Table of Contents

- [🚀 Overview](#-overview)
- [🧩 Technologies Used](#-technologies-used)
- [🧠 Design Decisions](#-design-decisions)
- [📦 System Evolution (v1 → v3)](#-system-evolution-v1--v3)
- [🔐 Assumptions](#-assumptions)
- [📡 API Endpoints](#-api-endpoints)
- [📸 Output Proofs](#-output-proofs)

---

## 🚀 Overview

This project is a 3-stage Inventory Management System built using **Flask**. It progressively evolves into a **scalable, asynchronous, real-time** application ready for deployment. Each stage introduces architectural enhancements and feature expansions to support growing business requirements such as:

- Multi-store support  
- User authentication  
- Asynchronous processing  
- WebSocket-based real-time updates  
- Microservice deployment with Docker and Nginx  

---

## 🧩 Technologies Used

| Category            | Tools / Libraries                             |
|---------------------|-----------------------------------------------|
| **Backend**         | Flask, Flask-Login (Authentication), SQLAlchemy |
| **Database**        | SQLite (v1), PostgreSQL + Replication (v2-v3) |
| **Caching & Queue** | Redis (Rate limiting, caching), Celery (Async tasks) |
| **WebSockets**      | Flask-SocketIO (Real-time notifications)      |
| **Deployment**      | Docker, Docker Compose, Nginx (Reverse proxy, load balancer) |
| **Task Scheduling** | Celery (with Redis as broker)                 |
| **Security**        | HTTPS-ready architecture (assumed in prod)    |

---

## 🧠 Design Decisions

### 🔹 Stage 1 – Basic MVP
- ✅ **SQLite**: Simple, no-configuration DB for development.
- ✅ **Stock Movement**: Transactions stored for audit trails.
- ✅ **Single File**: All logic in `app.py` for quick prototyping.

### 🔹 Stage 2 – Business Expansion
- 🔄 **PostgreSQL**: Switched to support concurrency and scaling.
- 🔒 **Redis**: Implemented **rate-limiting** (2s/request) for API abuse protection.  
  *[Proof](./Stage%202/Output/Checking%20Throttling.png)*
- 🏪 **Multi-Store Support**: Introduced `Store`, `StoreInventory` tables for separation of store inventories.

### 🔹 Stage 3 – Production-Ready
- 🐳 **Dockerized**: Separated services (Flask, Redis, Celery, PostgreSQL) via Docker.
- 🌐 **Nginx Reverse Proxy**: For routing, load balancing.
- 📡 **WebSocket Notifications**: Real-time inventory updates across clients.
- 🧠 **Celery Tasks**: Async logging, stock sync, and report generation.
- 🔁 **PostgreSQL Replication**: Read-replica setup for high-performance queries.  
  *[Replication Proof](./Stage%203/Output/Database/data%20replicating.png)*

---

## 📦 System Evolution (v1 → v3)

### v1 → v2
- **Database Upgrade**: Moved from SQLite to PostgreSQL for better write concurrency.
- **Rate Limiting**: Redis used to throttle requests and mitigate misuse.
- **User Authentication**: Implemented via `Flask-Login`.

### v2 → v3
- **Containerization**: Simplified deployment using Docker Compose.
- **Load Balancing**: Handled via Nginx and potential horizontal scaling.
- **Real-Time UX**: Eliminated polling via WebSockets.
- **Async Workflows**: Handled stock updates and logs in background via Celery.

---

## 🔐 Assumptions

1. **Inventory cannot go negative** — enforced at the application layer.
2. **HTTPS assumed** for production environments (Nginx config-ready).
3. **Redis is critical** — required for throttling, WebSockets, and Celery.
4. **User permissions** — All authenticated users currently share the same access level (fine-grained roles can be a future enhancement).

---

## 📡 API Endpoints

### 📍 Stage 1

| Method | Endpoint                        | Description                  | Proof |
|--------|----------------------------------|------------------------------|-------|
| POST   | `/product`                      | Add a new product            | ![Add](./Stage%201/Output%20Images/Adding%20Product.png) |
| POST   | `/products/<id>/stock`          | Add stock movement           | ![Stock](./Stage%201/Output%20Images/Updating%20Product%20Movement.png) |
| GET    | `/inventory/products/<id>`      | View product inventory       | ![Inventory](./Stage%201/Output%20Images/View%20Inventory.png) |

---

### 📍 Stage 2

| Method | Endpoint        | Description              | Proof |
|--------|------------------|--------------------------|-------|
| POST   | `/register`     | User registration         | ![Register](./Stage%202/Output/Register%20User.png) |
| GET    | `/stores`       | List available stores     | ![Stores](./Stage%202/Output/View%20Stores.png) |
| GET    | `/reports`      | Generate inventory reports | ![Report](./Stage%202/Output/View%20Report%20By%20Date.png) |

---

### 📍 Stage 3

| Method | Endpoint        | Description              | Proof |
|--------|------------------|--------------------------|-------|
| POST   | `/api/stock`     | Async stock update        | ![Stock](./Stage%203/Output/Postman/Input%20Stock.png) |
| GET    | `/api/search`    | Real-time stock search    | ![Search](./Stage%203/Output/Postman/Searching%20Stock.png) |

---

## 📸 Output Proofs

### ✅ Stage 1
- [Full Inventory Lifecycle](./Stage%201/Output%20Images/View%20Inventory%20After%20Updating.png)

### ✅ Stage 2
- [Store-Specific Report](./Stage%202/Output/View%20Report%20By%20Store%20id.png)

### ✅ Stage 3
- [Post-API Data Replication](./Stage%203/Output/Database/After%20Api%20Data%20replicated.png)

---

## 🧭 Future Improvements

- 🔐 Implement user roles: Admin, Store Manager, Viewer.
- 📈 Add analytics dashboards.
- 📱 Build a responsive frontend using React/Vue + Bootstrap.
- 🚨 Alert system for low stock levels via email/SMS.

---

## 🙌 Contributing

Interested in contributing? Fork the repo, create a branch, and submit a PR.

