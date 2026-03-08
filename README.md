# Dockerized RAG API with CI/CD

This project demonstrates how to take a functional RAG (Retrieval-Augmented Generation) API and prepare it for production by containerizing it with Docker and setting up an automated testing pipeline with GitHub Actions.

This repository is part of the "AI Engineer" learning path, specifically focusing on Week 4: MLOps & Containerization.

## Core Technologies

*   **Application:** FastAPI, LangChain, Google Gemini
*   **Database:** ChromaDB (Vector Store), Redis (Chat Memory)
*   **MLOps / DevOps:** Docker, Docker Compose, GitHub Actions

## Project Status

*   [x] **Day 22-23:** Application successfully containerized using a multi-stage `Dockerfile`.
*   [x] **Day 24:** Multi-service orchestration (API + Redis) set up with `docker-compose.yml`.
*   [x] **Day 25:** CI pipeline implemented with GitHub Actions to automate `pytest`.
*   [ ] **Day 26:** CI pipeline enhanced to run tests inside a Docker container.
*   [ ] **Day 27:** Docker image successfully pushed to a container registry.
*   [ ] **Day 28:** CD pipeline implemented to automate image publishing.

*(This README will be updated with full setup and usage instructions upon completion of the week's goals.)*
