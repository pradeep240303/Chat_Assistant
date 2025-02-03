# Chat_Assistant
DESCRIPTION:
This project is a Python-based chat assistant that interacts with an SQLite database to answer user queries. The assistant processes natural language queries, converts them into SQL, fetches relevant data, and provides a formatted response. The system is built using Flask for handling HTTP requests and SQLite3 as the database engine.
# Chat Assistant for SQLite Database

## Description

This project is a Python-based chat assistant that interacts with an SQLite database to answer user queries. The assistant processes natural language queries, converts them into SQL, fetches relevant data, and provides a formatted response. The system is built using Flask for handling HTTP requests and SQLite3 as the database engine.


Example Host:    lucky-babka-c4c18b.netlify.app


### Features:

- Retrieve employees based on their department.
- Find out the manager of a given department.
- List employees hired after a specific date.
- Calculate the total salary expense for a department.
- Handle incorrect inputs and provide meaningful error messages.

## How It Works

1. The application starts by creating (or checking for) an SQLite database (`company.db`).
2. Two tables are created:
   - `Employees` (ID, Name, Department, Salary, Hire\_Date)
   - `Departments` (ID, Name, Manager)
3. Sample data is inserted into these tables if they do not already exist.
4. A Flask API is set up to handle user queries via HTTP POST requests.
5. The assistant processes queries, converts them into SQL, executes them, and returns a response.

## Installation and Setup

### Prerequisites:

- Python 3.8+
- Flask library
- SQLite3 (comes with Python)


### Steps to Run Locally:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/chat-assistant-sqlite.git
   cd chat_assistant
   ```
2. **Install dependencies:**
   ```sh
   pip install flask
   ```
3. **Run the setup script to initialize the database:**
   ```sh
   python setup_database.py
   ```
4. **Start the Flask server:**
   ```sh
   python app.py
   

## Known Limitations

- Basic natural language processing (relies on simple keyword detection).
- Limited to pre-defined query formats.
- Does not support advanced search operations like fuzzy matching or complex filters.

## Suggestions for Improvement

- Implement NLP with a library like `spaCy` or `NLTK` for better query understanding.
- Add a front-end interface for user-friendly interaction.
- Expand the database with more employee attributes and query capabilities.
- Deploy on cloud services for broader access.
