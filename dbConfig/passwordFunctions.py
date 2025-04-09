from .db import get_dbConnection
from datetime import datetime
from config.Encryption import encrypt_pass

# Function to add a new Password
def addNewPassword(userId : int , userEmail : str , title : str , notes : str , identifier : str , password : str):
    createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')              # Ensure proper datetime format
    updatedAt = createdAt
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."
    
    result = checkUserBeforeInserting(userId , userEmail)
    if result == False:
        return False , "Following user doesn't Exist in Database"
    
    cursor = conn.cursor()
    conn.start_transaction()                # Start Transaction
    try:
        cursor.execute( "INSERT INTO passwordslists (title, notes, identifier , password , userId , createdAt , updatedAt) VALUES (%s, %s, %s, %s, %s , %s , %s)",
            (title , notes , identifier , encrypt_pass(password) , userId  , createdAt , updatedAt) )
        conn.commit()
        return True, "Password Details Added successfully."
    
    except Exception as e:
        conn.rollback()                                     # Rollback changes in case of error
        print(f"Error inserting Password Details: {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    
    finally:
        cursor.close()
        conn.close()
        

# Function to check user before inserting a new Password
def checkUserBeforeInserting(userId : int , userEmail : str ):
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s AND email = %s " , (userId , userEmail))
        user = cursor.fetchone()
        # password = (1, "Google Account", "Personal Gmail", "user1@gmail.com", "encrypted_password_1")
        
        if user:
            return user
        else:
            return False
            
    except Exception as e:
        print(f"Error checking user: {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()


# Function to get all the Passwords of a specific user
def getSpecificUserPasswords(userId : int , userEmail : str):
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM passwordslists WHERE userId = %s" , (userId , ))
        passwords = cursor.fetchall()
        
        if len(passwords) > 0:
            return True, passwords
        else:
            return False , "No Passwords are Added Till Now"
            
    except Exception as e:
        print(f"Error fetching User Specific Passwords : {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()
   
   
# Function to get the Password for Update
def getPasswordForUpdate(userId : int , userEmail : str , pid : int):
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT pid , title , notes , identifier , password FROM passwordslists WHERE userId = %s AND pid = %s" 
        , (userId  , pid))
        password = cursor.fetchone()

        if password:
            return True, password
        else:
            return False , "Invalid UserId or User Email or Password Id"
            
    except Exception as e:
        print(f"Error fetching password for update : {e}")                 # Log error for debugging
        return False, f"An error occurred: {str(e)}"        # Returning the status and message
    finally:
        cursor.close()
        conn.close()
        
        
# Function to update a Password     
def updatePassword(userId : int , userEmail : str , pid : int , title : str , notes : str , identifier : str , password : str):
    updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')              # Ensure proper datetime format
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        conn.start_transaction()  # Start transaction
        
        query = "UPDATE passwordslists SET title = %s, notes = %s, identifier = %s, password = %s , updatedAt = %s WHERE userId = %s AND pid = %s"
        cursor.execute(query, (title, notes, identifier, encrypt_pass(password) , updatedAt , userId, pid ))
        
        if cursor.rowcount == 0:
            conn.rollback()
            return (False, "No matching password entry found.")
        
        conn.commit()  # Commit transaction
        return (True, "Password Details updated successfully.")
    
    except Exception as e:
        conn.rollback()  # Rollback on error
        return (False, f"Error: {e}")
    
    finally:
        cursor.close()
        conn.close()


# Function to delete a  Password
def deletePassword(userId : int , userEmail : str , pid : int):
    conn = get_dbConnection()
    if conn is None:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        conn.start_transaction()  # Start transaction
        
        query = "DELETE FROM passwords WHERE userId = %s AND pid = %s"
        cursor.execute(query, (userId, pid))
        
        if cursor.rowcount == 0:
            conn.rollback()
            return (False, "No matching password entry found.")
        
        conn.commit()                           # Commit transaction
        return (True, "Password Details Deleted successfully.")
    
    except Exception as e:
        conn.rollback()  # Rollback on error
        return (False, f"Error: {e}")
    
    finally:
        cursor.close()
        conn.close()