# Web Scraping and ETL Process for Largest Banks

This Python script conducts web scraping on a Wikipedia page listing the largest banks and performs an Extract, Transform, Load (ETL) process. The extracted data is transformed and loaded into both a CSV file and an SQLite database.

## Prerequisites

Ensure that you have Python installed, and install the required libraries using
pip install beautifulsoup4 requests pandas numpy

# Process Steps
## 1)Extraction (extract):

Web scraping extracts information about the largest banks from the Wikipedia page.
## 2)Transformation (transform):

## 3)Currency conversion is applied to the 'Market_Cap' column.
## 4)New columns for market cap in GBP, EUR, and INR are added.
## 5)Loading (load_to_csv and load_to_db):

## 6)Transformed data is loaded into a CSV file (banks.csv).
## 7)Data is loaded into an SQLite database (Banks.db) as a 'Largest_banks' table.
## 8)Querying (run_query):

Example SQL queries are executed on the database:
SELECT * FROM Largest_banks
SELECT AVG(MC_GBP_Billion) FROM Largest_banks
SELECT Bank_Name FROM Largest_banks LIMIT 5
Completion:

The process concludes, and the SQL connection is closed.
