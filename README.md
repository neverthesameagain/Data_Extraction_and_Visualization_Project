
# Data Extraction and Visualization Project

## Introduction

This repository contains the code and resources for a project focused on extracting tables from HTML files and saving them in Excel or CSV format. The task involves analyzing HTML files to understand the data structure, sanitizing inputs, and dropping null values to maintain a coherent database.

The goal is to extract data for use in various data visualization purposes, including:

- Single entity visualization
- Multiple entity relationship visualization (e.g., two people working in the same department during the same time)

## Prerequisites

Ensure you have the following dependencies installed:

- Python (>=3.6)
- Selenium
- BeautifulSoup
- Pandas
- pg8000
- psycopg2
- webdriver-manager

You can install these dependencies using pip:

```bash
pip install selenium beautifulsoup4 pandas pg8000 psycopg2 webdriver-manager
```

## Setup

1. Clone this repository to your local machine.

```bash
git clone <repository_url>
```

2. Install the required dependencies as mentioned above.

## Usage

1. Navigate to the project directory.

```bash
cd Data_Extraction_and_Visualization_Project
```

2. Open the Python script containing the code.

```python
supremo.py
```

3. Run the script.

```bash
python supremo.py
```

## Files

- `supremo.py`: Contains the main Python script for the project.
- `tables/`: Directory containing sample HTML files of extracted tables.
- `README.md`: This file, providing instructions and information about the project.

## Contributing

Feel free to contribute to this repository by forking it and creating pull requests with your changes.
