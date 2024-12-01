# AttendanceManager
Attendance Manager

# Attendance Manager - Docker Setup Guide

This document provides a step-by-step guide to set up and run the Attendance Manager project using Docker.

---

## Requirements

Ensure that the following software is installed on your system before proceeding:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Setup Steps

Follow these steps to set up and run the project using Docker.

### 1. Clone the Project

Clone the project repository to your local machine:

```bash
git clone https://github.com/FurkanYazbahar/AttendanceManager.git
cd AttendanceManager
```

### 2. Build the Docker Image

Build the Docker image using the following command:

```bash
docker-compose build
```

This command uses the Dockerfile and `docker-compose.yml` file to create the required image.

### 3. Start the Containers

Start the containers using the following command:

```bash
docker-compose up
```

This command starts two services: the Django application and the PostgreSQL database.


### 4. Access the Application

When the project is initialized with Docker, two users are seeded into the database. You can use the following credentials to log in and test the system:

### Admin User
- **Username**: `admin`
- **Password**: `admin`

### Normal User
- **Username**: `user`
- **Password**: `user`



Once the application is running, you can access the login page in your browser at:

```
http://localhost:8000/login
```


