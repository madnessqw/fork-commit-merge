# P2P API Service - DAG Playbook

## Project Goals
Develop a FastAPI-based data scraping/analysis service with Direct P2P monetization via PayPal and Akbank IBAN.

## DAG Execution Plan (Parallel)

The following tasks are to be executed in parallel by the specialized agents.

### Task 1: `database-architect`
- **Goal:** Design and implement the database schema.
- **Actions:**
  - Choose PostgreSQL or SQLite.
  - Create tables for `api_keys` (key_hash, user_email, credits, status), `transactions` (reference, method, status), and `usage_logs`.
  - Provide initial migration scripts or SQLAlchemy models in the `workdir`.
- **Outputs:** Database schema SQL/Models.

### Task 2: `backend-engineer`
- **Goal:** Build the FastAPI application.
- **Actions:**
  - Setup FastAPI app structure.
  - Implement `X-API-Key` dependency for protected endpoints.
  - Create dummy scraping/analysis endpoints to demonstrate functionality.
  - Create a `/billing/notify` endpoint where users can submit their payment transaction reference (PayPal or IBAN) to request key activation.
  - Write a comprehensive `README.md` explicitly instructing users to pay to `chaotikss@gmail.com` (PayPal) or `TR38 0004 6002 0088 8000 1791 88` (Akbank IBAN) to receive an API key.
- **Outputs:** FastAPI application code, `README.md`.

### Task 3: `devops-engineer`
- **Goal:** Containerize and prepare deployment.
- **Actions:**
  - Create a `Dockerfile` for the FastAPI app.
  - Create a `docker-compose.yml` that spins up the app and the database (if PostgreSQL is chosen by DB architect).
  - Write a `deploy.sh` script.
- **Outputs:** Docker configuration and deployment scripts.

## Inter-Agent Dependencies
- `backend-engineer` depends on the data models defined by `database-architect`. However, they can start in parallel using mock data or the data contract defined in `hive_mind.md`.
- `devops-engineer` can prepare the Dockerfile based on standard FastAPI structure while the backend is being built.

## Next Steps
Once these parallel tasks are completed, the `qa-reviewer` will be triggered to verify the implementation, specifically checking if the README and billing logic correctly enforce the P2P payment rules.