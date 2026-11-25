# Daily Weather ETL Pipeline — Python, PostgreSQL & Docker

## 1. Project Overview

This project implements a daily Extract, Transform, Load (ETL) pipeline using Python, PostgreSQL, and Docker.

The pipeline retrieves weather forecast data from the Open-Meteo API, transforms hourly weather observations into a daily average temperature, validates the transformed data, and loads the results into PostgreSQL.

The project demonstrates practical data engineering concepts, including API integration, data transformation, data quality checks, relational database loading, logging, automation, and version control.

## 2. Architecture

```text
Open-Meteo Weather API
          |
          v
     EXTRACTION
          |
          v
   Raw JSON Data
          |
          v
   TRANSFORMATION
          |
          v
   DATA VALIDATION
          |
          v
    Clean CSV Data
          |
          v
       LOADING
          |
          v
     PostgreSQL
          |
          v
   Warehouse Tables
```

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL development |
| Pandas | Data transformation |
| Requests | API integration |
| PostgreSQL | Data warehouse |
| SQLAlchemy | Database connectivity |
| Psycopg | PostgreSQL driver |
| Docker | Database containerization |
| Docker Compose | Container management |
| python-dotenv | Environment variable management |
| Windows Task Scheduler | Pipeline automation |
| Git & GitHub | Version control |

## 4. Project Structure

```text
project2-daily-etl/
│
├── data/
│   ├── raw/
│   │   └── weather_2026-11-24.json
│   │
│   └── clean/
│       └── weather_today.csv
│
├── logs/
│
├── output/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── checks.py
│   ├── load.py
│   └── run_pipeline.py
│
├── tests/
│
├── .env
├── .gitignore
├── docker-compose.yml
├── schema.sql
└── README.md
```

## 5. ETL Pipeline Components

### Extraction — `src/extract.py`

- Connects to the Open-Meteo API.
- Retrieves hourly temperature forecast data.
- Saves the original API response as JSON.
- Uses a request timeout and checks for HTTP errors.

### Transformation — `src/transform.py`

- Reads the raw JSON data.
- Converts the hourly observations into a Pandas DataFrame.
- Parses timestamps.
- Removes missing temperature observations.
- Calculates the daily average temperature.
- Exports the transformed data as CSV.

### Data Quality — `src/checks.py`

The validation module checks:

- The dataset is not empty.
- Temperature values are not missing.
- Duplicate city/date records do not exist.
- Temperatures fall within the configured acceptable range.

Invalid data raises an exception before database loading.

### Loading — `src/load.py`

- Reads the clean CSV file.
- Connects to PostgreSQL through SQLAlchemy.
- Inserts date information into the date dimension.
- Loads weather records into the fact table.
- Uses PostgreSQL UPSERT logic to prevent duplicate city/date records.

### Orchestration — `src/run_pipeline.py`

Coordinates the ETL process:

1. Extraction
2. Transformation and validation
3. Database loading

The pipeline also records execution events and errors in a log file.

## 6. Database Design

The PostgreSQL database contains three tables.

| Table | Description |
|---|---|
| `raw_weather` | Defined for storing origninal JSON payloads; not yet populated by the current pipeline |
| `dim_date` | Stores date-related attributes |
| `fact_weather` | Stores daily weather measurements |

The fact table uses a composite primary key consisting of:

- `city`
- `date_key`

This prevents duplicate records for the same city and date.

## 7. Installation and Setup

### Prerequisites

Install the following:

- Python 3.10 or later
- Docker Desktop
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the repository

```cmd
git clone https://github.com/VicProjects12/project2-daily-etl.git
cd project2-daily-etl
```

### Step 2: Create a virtual environment

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

### Step 3: Install dependencies

```cmd
pip install requests pandas sqlalchemy "psycopg[binary]" python-dotenv
```

### Step 4: Configure environment variables

Create a `.env` file in the project root directory.

Add:

```text
POSTGRES_PASSWORD=your_local_password
DATABASE_URL=postgresql+psycopg://warehouse:your_local_password@localhost:5432/warehouse
```

Replace `your_local_password` with the same password used for PostgreSQL.

**Security:** Never commit your `.env` file or expose database credentials in public repositories.

### Step 5: Start PostgreSQL

Make sure Docker Desktop is running.

```cmd
docker compose up -d
```

Verify the container:

```cmd
docker ps
```

### Step 6: Create database tables

```cmd
docker compose exec -T postgres psql -U warehouse -d warehouse < schema.sql
```

### Step 7: Run the ETL pipeline

```cmd
python -m src.run_pipeline
```

The pipeline should extract weather data, transform and validate it, and load the results into PostgreSQL.

## 8. Verify Database Records

Connect to PostgreSQL:

```cmd
docker compose exec postgres psql -U warehouse -d warehouse
```

Query the fact table:

```sql
SELECT city, date_key, temp_c
FROM fact_weather;
```

Check the total number of records:

```sql
SELECT COUNT(*)
FROM fact_weather;
```

Exit PostgreSQL:

```sql
\q
```

## 9. Logging

The pipeline writes execution logs to:

```text
logs/pipeline.log
```

The log records:

- Pipeline start and completion.
- Extraction events.
- Transformation events.
- Database loading events.
- Pipeline failures.

## 10. Automation

Windows Task Scheduler can execute the pipeline automatically.

The configured task uses:

**Program:**

```text
C:\path\to\project2-daily-etl\venv\Scripts\python.exe
```

**Arguments:**

```text
-m src.run_pipeline
```

**Start in:**

```text
C:\path\to\project2-daily-etl
```

The task can be configured to execute daily.

## 11. Engineering Concepts Demonstrated

This project demonstrates practical experience with:

- Building modular Python applications.
- Extracting data from REST APIs.
- Working with JSON and CSV.
- Data cleaning and aggregation.
- Implementing data quality validation.
- Designing relational warehouse tables.
- Managing database transactions.
- Implementing idempotent database loading.
- Containerizing PostgreSQL with Docker.
- Managing application configuration through environment variables.
- Logging pipeline execution.
- Automating scheduled workflows.
- Using Git and GitHub for version control.

## 12. Current Scope and Future Improvements

The current implementation is a working learning pipeline configured for one weather location.

Planned improvements include:

- Expanding extraction to multiple cities.
- Adding humidity and wind measurements.
- Implementing historical data backfills.
- Adding automated unit and integration tests.
- Improving operational monitoring and failure reporting.
- Adding a dependency requirements file.
- Improving the project documentation and operational runbook.

## 13. Author

**GitHub:** [VicProjects12](https://github.com/VicProjects12)

**Repository:** [project2-daily-etl](https://github.com/VicProjects12/project2-daily-etl)
