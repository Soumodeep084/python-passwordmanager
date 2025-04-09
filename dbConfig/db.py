import mysql.connector
from config.settings import DB_CONFIG

# Function to get a database connection
def get_dbConnection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )