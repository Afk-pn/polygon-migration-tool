# Polygon Migration Tool

A Django-based tool for migrating competitive programming problems from **Polygon** into a local **PostgreSQL** database and uploading test-case files to **Amazon S3**.

## Architecture

```text
Polygon
   │
   │ Polygon API
   ▼
Django Application
   │
   ├──────────────► PostgreSQL
   │                 Problem metadata
   │                 Test-case metadata
   │
   ├──────────────► Redis
   │                 Temporary test-case cache
   │
   └──────────────► Amazon S3
                     Test-case input/output files
```

## Tech Stack

* Python
* Django
* PostgreSQL
* Redis
* Amazon S3
* Polygon API
* boto3

## Features

* Fetch problems from Polygon using a Polygon problem ID
* Display problem statement, solution and test cases
* Store migrated problem data in PostgreSQL
* Use Redis as a temporary cache for test cases
* Upload test-case inputs and expected outputs to Amazon S3
* Store test cases using the structure:

```text
test_cases/{problem_id}/{test_number}
test_cases/{problem_id}/{test_number}.a
```

* Support problem difficulty and tags
* Keep cloud-storage operations isolated in a dedicated S3 manager

## Demo Problem

The walkthrough uses:

**Problem:** Sum of Two Numbers
**Polygon ID:** 596823
**Database Problem ID:** 1
**Difficulty:** Easy
**Tags:** Math, Implementation

The problem contains 13 test cases covering positive, negative and zero values.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Afk-pn/polygon-migration-tool.git
cd polygon-migration-tool
```

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure the required Polygon, PostgreSQL, Redis and AWS S3 credentials in `.env`.

**Do not commit `.env` or any credentials to GitHub.**

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Start the Django server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Storage Implementation

The starter application contained an Azure-oriented migration entry point. For this implementation, the cloud-storage functionality was adapted to use Amazon S3.

S3-specific operations are contained in:

```text
problems/S3Testcase.py
```

The manager provides operations for:

* Uploading test-case input/output files
* Removing existing objects for a problem before migration

This keeps storage-specific logic separate from the main migration flow.

## Test Case Storage

For database problem ID `1`, the migrated S3 objects follow this structure:

```text
test_cases/1/01
test_cases/1/01.a
test_cases/1/02
test_cases/1/02.a
...
test_cases/1/13
test_cases/1/13.a
```

The files without `.a` contain test inputs, while `.a` files contain the corresponding expected outputs.

## Security

Credentials are provided through environment variables and are excluded from version control using `.gitignore`.

Never commit:

```text
.env
AWS credentials
Polygon API secrets
Database passwords
```

## Walkthrough

The accompanying walkthrough demonstrates:

1. Fetching a problem from Polygon
2. Reviewing the statement, solution and test cases
3. Setting difficulty and tags
4. Migrating the problem to PostgreSQL
5. Using Redis as a temporary test-case cache
6. Uploading test cases to Amazon S3
7. Verifying the resulting S3 objects
8. Reviewing the storage implementation

## Author

**Rani**
NITK Surathkal — Electronics and Communication Engineering
