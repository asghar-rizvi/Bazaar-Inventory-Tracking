# Inventory Management System (v1 → v3)

![Stage 3 Docker Deployment](./Stage%203/Output/Docker/Docker.png)

## Table of Contents
- [Design Decisions](#design-decisions)
- [Assumptions](#assumptions)
- [API Design](#api-design)
- [Evolution Rationale](#evolution-rationale-v1--v3)
- [Output Proofs](#output-proofs)

---

## Design Decisions

### Stage 1 (Basic)
- **SQLite Database**: Chosen for simplicity and zero-configuration during development.
- **Movement-Based Inventory**: Tracked stock changes via `StockMovement` records for auditability.
- **Single-File Architecture**: All logic in `app.py` for quick iteration.

### Stage 2 (Enhanced)
- **PostgreSQL**: Upgraded for production readiness and scalability.
- **Redis Rate Limiting**: Added throttling (2s/request) to prevent abuse ([Proof](./Stage%202/Output/Checking%20Throttling.png)).
- **Multi-Store Support**: Introduced `Store` and `StoreInventory` models for business expansion.

### Stage 3 (Production)
- **Microservices Architecture**: Dockerized with Nginx load balancing.
- **Real-Time Updates**: WebSocket notifications for inventory changes.
- **Master-Replica DB**: PostgreSQL read replicas for performance ([Replication Proof](./Stage%203/Output/Database/tables%20replicating.png)).
- **Async Processing**: Celery for background tasks (audit logs, stock updates).

---

## Assumptions
1. **Data Consistency**: 
   - Inventory quantities never go negative (enforced at application layer).
2. **Security**: 
   - Stage 2+ assumes HTTPS in production (not shown in tests).
3. **Performance**: 
   - Redis availability is critical for Stage 2+ throttling and Stage 3 WebSockets.
4. **User Roles**: 
   - Stage 2+ assumes all authenticated users have equal privileges.

---

## API Design

### Stage 1
| Endpoint | Method | Description | Proof |
|----------|--------|-------------|-------|
| `/product` | POST | Add product | [Add Product](./Stage%201/Output%20Images/Adding%20Product.png) |
| `/products/<id>/stock` | POST | Record movement | [Update Stock](./Stage%201/Output%20Images/Updating%20Product%20Movement.png) |
| `/inventory/products/<id>` | GET | View current stock | [View Inventory](./Stage%201/Output%20Images/View%20Inventory.png) |

### Stage 2
| Endpoint | Method | Description | Proof |
|----------|--------|-------------|-------|
| `/register` | POST | User registration | [Register User](./Stage%202/Output/Register%20User.png) |
| `/stores` | GET | List stores | [View Stores](./Stage%202/Output/View%20Stores.png) |
| `/reports` | GET | Filterable reports | [Date Filter](./Stage%202/Output/View%20Report%20By%20Date.png) |

### Stage 3
| Endpoint | Method | Description | Proof |
|----------|--------|-------------|-------|
| `/api/stock` | POST | Async stock update | [Input Stock](./Stage%203/Output/Postman/Input%20Stock.png) |
| `/api/search` | GET | Real-time stock query | [Search Stock](./Stage%203/Output/Postman/Searching%20Stock.png) |

---

## Evolution Rationale (v1 → v3)

### Stage 1 → Stage 2
- **Why PostgreSQL?**  
  SQLite lacked concurrency for multi-store operations ([DB Health](./Stage%203/Output/Postman/Checking%20Health%20Of%20DB.png)).
- **Why Redis?**  
  Needed request throttling to protect APIs ([Throttling Proof](./Stage%202/Output/Checking%20Throttling.png)).

### Stage 2 → Stage 3
- **Why Docker?**  
  Simplified deployment of complex services (Flask, Celery, Redis) ([Docker Proof](./Stage%203/Output/Docker/Docker.png)).
- **Why WebSockets?**  
  Eliminated polling for inventory updates (critical for multi-location dashboards).
- **Why Master-Replica?**  
  Improved read performance for reports ([Replication Proof](./Stage%203/Output/Database/data%20replicating.png)).

---

## Output Proofs
### Stage 1
- [Full Inventory Lifecycle](./Stage%201/Output%20Images/View%20Inventory%20After%20Updating.png)

### Stage 2
- [Store-Specific Report](./Stage%202/Output/View%20Report%20By%20Store%20id.png)

### Stage 3
- [Post-API Data Sync](./Stage%203/Output/Database/After%20Api%20Data%20replicated.png)
