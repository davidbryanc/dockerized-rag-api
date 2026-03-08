# Project: Dockerized RAG API with a Full CI/CD Pipeline

This repository is the capstone project for a week-long, intensive study on MLOps, focusing on containerization and automation. It demonstrates the process of taking a functional AI application (a RAG API built with FastAPI) and transforming it into a production-ready, portable, and automatically-tested artifact.

The core achievement of this project is the implementation of two distinct **GitHub Actions workflows**:
1.  **Continuous Integration (CI):** Automatically runs `pytest` inside a Docker container on every push, ensuring code quality and environment consistency.
2.  **Continuous Delivery (CD):** Automatically builds and publishes a new Docker image to the GitHub Container Registry (GHCR) on every push to the `main` branch.

## Core Technologies & Concepts Mastered

*   **Application:** FastAPI, LangChain, Google Gemini
*   **Containerization:** Docker, Docker Compose, Multi-stage Dockerfiles
*   **Automation (CI/CD):** GitHub Actions, YAML Workflows
*   **Services:** Redis for stateful chat memory
*   **Observability:** Securely managing secrets and environment variables for CI/CD pipelines.

## Final Architecture

This project runs as a multi-service application orchestrated by Docker Compose, consisting of:
1.  **`api` service:** Our Python FastAPI application, serving the RAG endpoints.
2.  **`redis` service:** A Redis database container for persisting conversational memory.

The entire system is designed to be built and run via a single command: `docker-compose up`.

---

## How It Works: The CI/CD Pipelines

This repository contains two critical workflows located in `.github/workflows/`.

### 1. `ci.yml` - The Quality Gatekeeper

*   **Trigger:** Runs on every `push` to any branch and on every `pull_request` to `main`.
*   **Process:**
    1.  Checks out the source code.
    2.  Builds a Docker image based on the `Dockerfile`.
    3.  Creates a temporary `.env.ci` file using encrypted GitHub Secrets (`secrets.GOOGLE_API_KEY`).
    4.  Runs a new container from the image, injects the secrets, and executes `pytest` inside it.
*   **Purpose:** To guarantee that no code that breaks the existing tests or fails in a production-like Docker environment can be merged.

### 2. `release.yml` - The Automated Factory

*   **Trigger:** Runs **only** on `push` events to the `main` branch.
*   **Process:**
    1.  Checks out the source code.
    2.  Securely logs into the GitHub Container Registry (GHCR) using a temporary `GITHUB_TOKEN`.
    3.  Intelligently generates version tags for the Docker image (e.g., `:latest`, `:main`).
    4.  Builds the final Docker image and **pushes** it to the repository's Packages tab.
*   **Purpose:** To ensure that every version of the `main` branch has a corresponding, deployable Docker image stored securely and ready for production.

---

## Local Development & Usage

### 1. Prerequisites

*   Docker Desktop installed and running.
*   An `.env` file in the root directory with your `GOOGLE_API_KEY`.

### 2. Building and Running with Docker Compose

This is the recommended method for running the entire application stack locally.

```bash
# Build the images and start the services (api and redis)
docker-compose up --build
```
The API will be available at `http://localhost:8000`. The interactive documentation can be accessed at `http://localhost:8000/docs`.

### 3. Running Tests Manually Inside Docker

You can also replicate the CI testing step locally:

```bash
# Build the image first (if not already built)
docker build -t rag-api-local .

# Run pytest inside a new container
docker run --env-file .env rag-api-local python -m pytest
```
