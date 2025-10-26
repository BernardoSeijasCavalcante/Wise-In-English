import os

DB_CONFIG = {
    "server": os.getenv("DB_SERVER", "restdb.database.windows.net"),
    "database": os.getenv("DB_NAME", "Wise-Englishman-Database"),
    "username": os.getenv("DB_USER", "boss"),
    "password": os.getenv("DB_PASS", "STUDY!english"),
    "driver": "ODBC Driver 18 for SQL Server"
}