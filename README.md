# Sparkify ETL Pipeline

A PostgreSQL-based ETL pipeline for turning Sparkify music-streaming event data into an analysis-ready relational model.

The project reads song metadata and user activity logs stored as JSON, cleans and transforms the records with Python/Pandas, and loads them into a PostgreSQL star schema.

## What I built

- Designed a PostgreSQL schema around a central `songplays` fact table.
- Built separate `songs`, `artists`, `users`, and `time` dimensions.
- Added an ETL flow for both song metadata and streaming-event logs.
- Added duplicate-safe dimension inserts using PostgreSQL `ON CONFLICT`.
- Filtered event logs to `NextSong` activity before loading the fact table.
- Replaced hard-coded connection settings with environment-variable configuration.
- Added basic resource cleanup and clearer pipeline logging.

## Architecture

```text
JSON song data ───────┐
                      ├──> Python / Pandas ETL ───> PostgreSQL
JSON event logs ──────┘                                  │
                                                         ├── songs
                                                         ├── artists
                                                         ├── users
                                                         ├── time
                                                         └── songplays
```

## Data model

| Table | Type | Purpose |
|---|---|---|
| `songplays` | Fact | Streaming events associated with songs and users |
| `songs` | Dimension | Song title, artist, year, and duration |
| `artists` | Dimension | Artist identity and location |
| `users` | Dimension | User profile and subscription level |
| `time` | Dimension | Time attributes derived from event timestamps |

## Tech stack

- Python
- Pandas
- NumPy
- PostgreSQL
- psycopg2
- SQL
- Jupyter Notebook

## Project structure

```text
Sparkify-ETL/
├── create_tables.py
├── etl.py
├── sql_queries.py
├── requirements.txt
├── etl.ipynb
├── test.ipynb
├── README.md
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/prathameshtadas/Sparkify-ETL.git
cd Sparkify-ETL
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

The scripts use these environment variables:

```text
SPARKIFY_DB_HOST
SPARKIFY_DB_PORT
SPARKIFY_ADMIN_DB
SPARKIFY_DB_NAME
SPARKIFY_DB_USER
SPARKIFY_DB_PASSWORD
```

Defaults are provided for a local PostgreSQL setup, but credentials should be configured through environment variables for real deployments.

### 5. Create the database schema

```bash
python create_tables.py
```

### 6. Load the data

Place the Sparkify `song_data` and `log_data` directories under `data/`, then run:

```bash
python etl.py
```

## Engineering notes

The pipeline commits after each input file. This keeps individual file loads isolated and makes progress visible during a long-running local ETL job.

For production-scale data, the next step would be to replace row-by-row inserts with batched loading, add structured logging, introduce data-quality checks, and move connection management to a dedicated configuration module.

## Future improvements

- Add automated data-quality validation.
- Add pytest coverage for transformation logic.
- Add Docker Compose for PostgreSQL.
- Add batch inserts with `execute_values`.
- Add incremental ETL and audit logging.
- Add analytical SQL queries and a small Power BI/Tableau dashboard.

## Author

**Prathamesh Tadas**

Data Analyst | SQL • Python • ETL • Data Engineering

GitHub: [@prathameshtadas](https://github.com/prathameshtadas)
