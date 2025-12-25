# Project: PCHS FlexPass App

<!--toc:start-->
- [Project: PCHS FlexPass App](#project-pchs-flexpass-app)
  - [Setup Project](#setup-project)
    - [Prerequisites](#prerequisites)
    - [Notes](#notes)
    - [Setup](#setup)
    - [Database Migrations](#database-migrations)
  - [Running The Project](#running-the-project)
    - [Run the database](#run-the-database)
    - [Run the website](#run-the-website)
<!--toc:end-->

A system for managing students during flex times, and coordinating hall passes for students.

## Setup Project

### Prerequisites

- `docker` [https://docs.docker.com/compose/install/]
Used to easy run PostgreSQL consistently for testing.

- `uv` [https://docs.astral.sh/uv/getting-started/installation/]
Replaces default python package manager (pip) with a more consistent one.

- `npm` [https://nodejs.org/en/download/]
Needed for Tailwind CSS integration.

### Notes

On Windows Docker Desktop will need to be running in the background for Docker Compose to work.
All commands listed are expected to be run while navigated to the project directory.

### Setup

Tailwind CSS packages need to be installed.

```sh
uv run manage.py tailwind install
```

### Database Migrations

First ensure database is running.

```sh
docker compose up
```

Perform database migrations if any changes have been made to it since last pull.

```sh
uv run manage.py migrate
```

## Running The Project

### Run the database

Install `docker` [https://docs.docker.com/compose/install/]

Navigate to the project directory in a terminal, and run:

```sh
docker compose up
```

### Run the website

Install `uv` [https://docs.astral.sh/uv/getting-started/installation/]

In new a terminal, while navigated to the project directory, run:

```sh
uv run manage.py tailwind dev
```

Then in your browser navigate to `http://127.0.0.1:8000`.
