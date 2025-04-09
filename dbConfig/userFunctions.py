from typing import Tuple
from .db import get_dbConnection
from datetime import datetime
from config.PasswordHasher import hashPassword , verifyPassword
import requests
import platform

# Function to check if username/email already exists in the database
def checkUserExists(username: str, email: str) -> bool:
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        print(f"Error inserting user: {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()
        

# Function to insert a new user into the database
def insertUser(name: str, username: str, email: str, password: str) -> Tuple[bool, str]:
    currentDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Ensure proper datetime format
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."
        
    cursor = conn.cursor()
    
    # Start Transaction
    conn.start_transaction()
    try:
        cursor.execute(
            "INSERT INTO users (name, username, email, password, isVerified, createdAt) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, username, email, hashPassword(password), 1, currentDateTime)  # Convert True → 1
        )
        conn.commit()
        return True, "Registration successful! You can now log in."
    except Exception as e:
        conn.rollback()                                     # Rollback changes in case of error
        print(f"Error inserting user: {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()
   

# Function to user details from database
def getUserForLogin(username_or_email: str, entered_password: str):
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."
        
    cursor = conn.cursor(dictionary=True)                                                       # Return results as a dictionary
    try:
        cursor.execute("SELECT id, email, password FROM users WHERE username = %s OR email = %s", (username_or_email, username_or_email))
        user = cursor.fetchone()
        if user:
            # Verify the entered password against the hashed password from the database
            if verifyPassword(user["password"] , entered_password):
                return {"id": user["id"], "email": user["email"]}           # Return ID and email if passwords match
            else:
                return False                                                # Return False if passwords do not match
        else:
            return None                                                     # Return None if user is not found
    finally:
        cursor.close()
        conn.close()     


# Function to user details from database
def getUserAccountDetails(userId : int, userEmail: str):
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."
        
    cursor = conn.cursor(dictionary=True)                                                       # Return results as a dictionary
    try:
        cursor.execute("SELECT id, name , username , email , isVerified , createdAt ,  updatedAt FROM users WHERE id = %s OR email = %s", (userId, userEmail))
        user = cursor.fetchone()
        if user:
            return True , user                                               # Return False if passwords do not match
        else:
            return False , "Invalid User"
    finally:
        cursor.close()
        conn.close() 
        

# Function to update user details
def updateUserAccount(userId : int , newName : str , newUsername : str , newUserEmail : str):
    updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."
        
    cursor = conn.cursor()
    
    # Start Transaction
    conn.start_transaction()
    try:
        cursor.execute(
            "UPDATE users SET name = %s , username = %s , email = %s , updatedAt = %s WHERE id = %s" , (newName , newUsername , newUserEmail , updatedAt , userId))
        conn.commit()
        return True, "Registration successful! You can now log in."
    except Exception as e:
        conn.rollback()                                     # Rollback changes in case of error
        print(f"Error inserting user: {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()


# Function to delete User from database
def deleteUser(userId : int):
    try:
        conn = get_dbConnection()
        cursor = conn.cursor()

        # Start transaction
        conn.start_transaction()

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (userId,))
        user = cursor.fetchone()
        if not user:
            return False, "User does not exist"

        cursor.execute("DELETE FROM users WHERE id = %s", (userId,))
        conn.commit()

        return True, "User deleted successfully"

    except Exception as e:
        conn.rollback()  # Rollback if any error occurs
        return False, f"Error: {e}"

    finally:
        cursor.close()
        conn.close()


# Function to get Password For Password Update
def checkUserForgotPassword(email: str):
    try:
        # Connect to the database (replace with your database connection logic)
        conn = get_dbConnection()
        cursor = conn.cursor()

        query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            return True, result[0]
        else:
            return False, None

    except Exception as e:
        print(f"Error checking user: {str(e)}")
        return False, None

    finally:
        cursor.close()
        conn.close()


# Function to check current password and grant permission to change password from profile
def checkAccountPassword(userId : int , currentPassword : str):
    try:
        # Connect to the database (replace with your database connection logic)
        conn = get_dbConnection()
        cursor = conn.cursor()
        
        # Start Transaction
        conn.start_transaction()

        # SQL query to retrieve the password
        cursor.execute("SELECT Password FROM users WHERE id = %s", (userId , ))
        userPass = cursor.fetchone()                # Returns a Tuple so access userPass[0]

        if not userPass:
            return False, "Wrong UserId!"

        status = verifyPassword(userPass[0] , currentPassword)
        if status == True:
            return True, "Correct Current Password."
        else:
            return False, "Incorrect Current Password"

    except Exception as e:
        return False, f"Error updating password: {str(e)}"

    finally:
        cursor.close()
        conn.close()

# Function to delete User from database
def updateAccountPassword(userId: int, newPassword: str):
    updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    try:
        # Connect to the database (replace with your database connection logic)
        conn = get_dbConnection()
        cursor = conn.cursor()
        
        # Start Transaction
        conn.start_transaction()

        # SQL query to update the password
        query = "UPDATE users SET password = %s , updatedAt = %s WHERE id = %s"
        cursor.execute(query, (hashPassword(newPassword) , updatedAt , userId))

        conn.commit()

        if cursor.rowcount > 0:
            return True, "Password updated successfully!"
        else:
            return False, "No user found with the provided ID."

    except Exception as e:
        cursor.rollback()
        return False, f"Error updating password: {str(e)}"

    finally:
        cursor.close()
        conn.close()


# Function to insert security details
def insertSecurityLoginDetails(userId : int , userEmail : str):
    loginTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Ensure proper datetime format
    
    try:
        public_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
        os_name = f"{platform.system()} {platform.release()}"  # Extract OS name and version
        architecture = "64-bit" if platform.architecture()[0] == "64bit" else "32-bit"
        device_info = f"{os_name} | {architecture}"  # Concise device info
    except requests.RequestException:
        public_ip = "Unavailable"
        device_info = "Unknown"
    
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."
        
    cursor = conn.cursor()
    
    # Start Transaction
    conn.start_transaction()
    try:
        cursor.execute( "INSERT INTO securitydetails (userId , ip_address , device_info , login_time ) VALUES (%s, %s, %s, %s)", (userId, public_ip , device_info ,loginTime) )
        conn.commit()
        return True, "Registration successful! You can now log in."
    except Exception as e:
        conn.rollback()                                     # Rollback changes in case of error
        print(f"Error inserting SecurityDetails: {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()
        
        
# Function to fetch security Details
def fetchSecurityDetails(userId : int , userEmail : str):
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM securitydetails WHERE userId = %s" , (userId,))
        securityDetails = cursor.fetchall()
        if len(securityDetails) > 0:
            return True, securityDetails
        else:
            return False , "No Security Details"
            
    except Exception as e:
        print(f"Error fetching security Details: {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()