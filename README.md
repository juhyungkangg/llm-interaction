# LLM Interaction Project

The **LLM Interaction** project is a system that processes various data sources using OpenAI's large language models (LLMs) to perform sentiment analysis, filtering, and signal extraction. It interacts with a MySQL database to fetch data, runs batch jobs with the OpenAI API, processes responses, updates the database, and generates signals based on LLM outputs. The project is modular, consisting of components for data fetching, batch job management, result processing, and scheduling tasks.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running Manually](#running-manually)
  - [Scheduled Execution](#scheduled-execution)
- [Modules Overview](#modules-overview)
- [Dependencies](#dependencies)
- [License](#license)

## Features

- Fetches data from multiple sources (Benzinga, NASDAQ, Reddit, Seeking Alpha).
- Uses OpenAI GPT-4 model for filtering content and sentiment analysis.
- Manages and monitors batch jobs through the OpenAI API.
- Processes LLM responses, updates database records, and stores signal data.
- Aggregates and computes weighted sentiment signals.
- Schedules tasks to run at specified times using the `schedule` library.

## Project Structure

```
llm-interaction/
├── LLMInteraction/
│   ├── assets/
│   │   ├── prompts.py           # Prompt templates for various data sources
│   │   └── json_schema.py       # JSON schema definitions for responses
│   ├── run/
│   │   ├── batch.py             # Defines the Batch class for handling OpenAI batch interactions
│   │   ├── batch_runner.py      # Defines the BatchRunner class to execute and retrieve batch results
│   │   └── ...
│   └── ...
├── SQLInteraction/
│   ├── queries.py               # SQL query definitions for various tasks
│   ├── SQLResult.py             # SQLResult class to fetch database results
│   └── SQL_utils.py             # Utility functions for MySQL interactions
├── mainTasks/
│   ├── cancel_batch.py          # Script to cancel running batches
│   ├── get_signals.py           # Script to extract signals and save them to Dropbox
│   ├── llm_layer.py             # Functions to run filter and sentiment analysis workflows
│   ├── manual_upload.py         # Utility for manually uploading and processing batch results
│   └── main.py                  # Main entry point for scheduled tasks and manual execution
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/llm-interaction.git
   cd llm-interaction
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with the necessary environment variables:

```ini
# Database configuration
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_DATABASE=your_database_name

# OpenAI API key
OPENAI_API_KEY=your_openai_api_key

# Dropbox configuration if needed
DROPBOX_ACCESS_TOKEN=your_dropbox_access_token
```

Adjust database and API credentials as needed.

## Usage

### Running Manually

To run the main tasks manually without scheduling, execute:

```bash
python mainTasks/main.py
```

This script performs filtering, sentiment analysis, and signal retrieval sequentially.

### Scheduled Execution

The `main.py` script is set up to run tasks at specified times using the `schedule` library. To enable scheduling, uncomment the scheduling loop in `main.py`:

```python
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
```

Then run:

```bash
python mainTasks/main.py
```

The script will run the tasks at the scheduled times (e.g., 06:00, 07:00, 08:00 daily).

## Modules Overview

- **Batch and BatchRunner (`LLMInteraction/run/batch.py` & `batch_runner.py`):**  
  Manage creation, upload, monitoring, and retrieval of OpenAI batch jobs. They handle processing of responses from OpenAI for both filtering and sentiment analysis.

- **SQL Utilities (`SQLInteraction/SQL_utils.py`, `SQLResult.py`, `queries.py`):**  
  Provide functions to connect to MySQL, execute queries, update processed flags, and fetch specific query results based on data source requirements.

- **Main Tasks (`mainTasks/`):**  
  Scripts like `llm_layer.py`, `get_signals.py`, `manual_upload.py`, and `cancel_batch.py` orchestrate different parts of the workflow, such as running LLM filtering/sentiment pipelines, retrieving signals, manual batch result handling, and cancelling batches.

- **Signal Processing (`mainTasks/get_signals.py`):**  
  Retrieves signal data from the database, processes and aggregates sentiment information, and saves the results (e.g., to Dropbox).

## Dependencies

Dependencies are listed in `requirements.txt`. Major libraries include:
- `openai` for interacting with the OpenAI API.
- `mysql-connector-python` for MySQL database interactions.
- `pandas` for data manipulation.
- `schedule` for task scheduling.
- `python-dotenv` for environment variable management.
- `Jinja2` for templating prompts.
- Other utility libraries: `pydantic`, `dropbox`, `requests`.

Install them using:
```bash
pip install -r requirements.txt
```

---

Feel free to contribute, raise issues, or suggest improvements. For any questions, please contact jk8448@nyu.edu.

