import string
import secrets
import threading
from datetime import datetime, timedelta
from backend.email_service import send_otp_email
from dbConfig.userFunctions import checkUserExists, insertUser, getUserForLogin , insertSecurityLoginDetails

# Dictionary to store OTPs temporarily (in-memory storage)
otp_storage = {}                # Register User and Verification + Login User with Verification
otp_storage1 = {}               # Account Updates From Profile and Verification
otp_storage2 = {}               # User Account Delete Account and Verification
otp_storage3 = {}               # User Account Forgot Password For Profile and Verification
otp_storage4 = {}               # User Account Password Update From Profile and Verification
otp_lock = threading.Lock()


# Function to generate a random OTP
def generate_otp():
    return ''.join(secrets.choice(string.digits) for _ in range(6))  # Secure OTP


# Function to register a new user
def registerUser(name, username, email, password, confirm_password):
    # Check if passwords match
    if password != confirm_password:
        return False, "Passwords do not match."
    
    # Check if username/email already exists
    if checkUserExists(username, email):
        return False, "Username or email already exists."
    
    # Generate OTP
    otp = generate_otp()
    otp_expiry = datetime.now() + timedelta(minutes=2)  # OTP valid for 2 minutes
    
    # Normalize email (convert to lowercase)
    email = email.lower()
    
    # Store OTP temporarily
    with otp_lock:
        otp_storage[email] = {
            "otp": otp,
            "expiry": otp_expiry,
            "user_data": {
                "name": name,
                "username": username,
                "email": email,
                "password": password
            }
        }
    
    # Send OTP to the user's email
    subject = "OTP for Account Verification - EncryptPass The Password Manager"
    body = f"""
    <h2>Welcome to EncryptPass!</h2>
    <p>Thank you for registering with us. Below is your OTP for Account verification:</p>
    <h3 style="color:red;">{otp}</h3>
    <p><strong>Do not share this OTP with anyone.</strong></p>
    <p>This OTP is valid for 2 minutes. (120 seconds) </p>
    <p>If it was not you complain us at complaint.user@encryptpass.com</p>
    """
    
    send_otp_email(email, subject, body)
    
    return True, "OTP has been sent to your email for Account Verification."


# Function for Account Verification OTP
def verifyAccountOTP(email: str, otp: str):
    # Normalize email (convert to lowercase)
    email = email.lower()
    # Strip whitespace from OTP
    otp = otp.strip()
    
    with otp_lock:
        if email not in otp_storage:
            return False, "OTP has expired or the email is incorrect."

        stored_otp_data = otp_storage[email]

        if datetime.now() > stored_otp_data["expiry"]:
            del otp_storage[email]  # Remove expired OTP
            return False, "OTP has expired."

        if otp != stored_otp_data["otp"].strip():
            return False, "Invalid OTP."

        # Insert user into the database
        userData = stored_otp_data["user_data"]
        success, message = insertUser(userData["name"], userData["username"], userData["email"], userData["password"])

        # Remove OTP after successful verification
        if success:
            del otp_storage[email]

        return success, message


# Function for Account Login
def loginUser(username_or_email: str, password: str):
    # Fetch user details from the database
    user = getUserForLogin(username_or_email, password)
    if not user:
        return False, "Invalid username/email or password."
    
    # Generate OTP for login verification
    otp = generate_otp()
    otp_expiry = datetime.now() + timedelta(minutes=2)  # OTP valid for 2 minutes
    
    # Normalize email (convert to lowercase)
    email = user["email"].lower()
    
    # Store OTP temporarily
    with otp_lock:
        otp_storage[username_or_email] = {
            "otp": otp,
            "expiry": otp_expiry,
            "user_data": user
        }
    
    # Send OTP to the user's email
    subject = "OTP for Account Login - EncryptPass The Password Manager"
    body = f"""
    <h2>Welcome to EncryptPass!</h2>
    <p>Dear user , <br> Below is your OTP for account Login:</p>
    <h3 style="color:red;">{otp}</h3>
    <p><strong>Do not share this OTP with anyone.</strong></p>
    <p>This OTP is valid for 2 minutes. (120 seconds) </p>
    <p>If it was not you complain us at complaint.user@encryptpass.com</p>
    """
    send_otp_email(email, subject, body)
    
    return True, "OTP has been sent to your email for Login Verification."


# Function for Account Login OTP Verification
def verifyLoginOTP(email: str, otp: str):
    # Normalize email (convert to lowercase)
    email = email.lower()
    # Strip whitespace from OTP
    otp = otp.strip()
    try:
        with otp_lock:
            if email not in otp_storage:
                return False, "OTP has expired or the email is incorrect."

            stored_otp_data = otp_storage[email]
            userData = stored_otp_data['user_data']

            if datetime.now() > stored_otp_data["expiry"]:
                del otp_storage[email]  # Remove expired OTP
                return False, "OTP has expired."

            if otp != stored_otp_data["otp"].strip():
                return False, "Invalid OTP."

            # Remove OTP after successful verification
            del otp_storage[email]
            
            userId = userData["id"]
            userEmail = userData["email"]
            
            insertSecurityLoginDetails(userId , userEmail)
            
            # print("stored_otp user : ", stored_otp_data['user_data'])
            return True, "Login successful!", userData
        
    except KeyError as e:
        # Handle the case where the email is not found in otp_storage2
        return False, "Error : ."
    except Exception as ex:
        return False , "Exception as verify Login OTP : "
    
    
# Function for Account Update
def updateAccountUserFunc(email: str):
    
    # Generate OTP for login verification
    otp = generate_otp()
    otp_expiry = datetime.now() + timedelta(minutes=2)  # OTP valid for 2 minutes
    
    # Normalize email (convert to lowercase)
    email = email.lower()
    
    # Store OTP temporarily
    with otp_lock:
        otp_storage1[email] = {
            "otp": otp,
            "expiry": otp_expiry,
        }
    
    # Send OTP to the user's email
    subject = "OTP for Account Update - EncryptPass The Password Manager"
    body = f"""
    <h2>Welcome to EncryptPass!</h2>
    <p>Dear user , <br> Below is your OTP for Account Update:</p>
    <h3 style="color:red;">{otp}</h3>
    <p><strong>Do not share this OTP with anyone.</strong></p>
    <p>This OTP is valid for 2 minutes. (120 seconds) </p>
    <p>If it was not you complain us at complaint.user@encryptpass.com</p>
    """
    send_otp_email(email, subject, body)
    
    return True, "OTP has been sent to your email for Account Update Verification."


# Function for Account Login OTP Verification
def verifyAccountUpdateOTP(email: str, otp: str):
    # Normalize email (convert to lowercase)
    email = email.lower()
    # Strip whitespace from OTP
    otp = otp.strip()
    try:
        with otp_lock:
            # print(email)
            # print(otp_storage)
            if email not in otp_storage1:
                return False, "OTP has expired or the email is incorrect."

            stored_otp_data = otp_storage1[email]

            if datetime.now() > stored_otp_data["expiry"]:
                del otp_storage1[email]  # Remove expired OTP
                return False, "OTP has expired."

            if otp != stored_otp_data["otp"].strip():
                return False, "Invalid OTP."

            # Remove OTP after successful verification
            del otp_storage1[email]

            return True , "OTP Verified Successfully"
    except KeyError as e:
            # Handle the case where the email is not found in otp_storage2
            return False, "Error : ."
    
    
# Function for Account Delete
def deleteAccountUserFunc(email: str):
    print("DeleteUserFunc Called")
    # Generate OTP for login verification
    otp = generate_otp()
    otp_expiry = datetime.now() + timedelta(minutes=2)  # OTP valid for 2 minutes
    
    # Normalize email (convert to lowercase)
    email = email.lower()
    
    # Store OTP temporarily
    with otp_lock:
        otp_storage2[email] = {
            "otp": otp,
            "expiry": otp_expiry,
        }
    
    # Send OTP to the user's email
    subject = "OTP for Account Update - EncryptPass The Password Manager"
    body = f"""
    <h2>Welcome to EncryptPass!</h2>
    <p>Dear user , <br> Below is your OTP for Account Deletion:</p>
    <h3 style="color:red;">{otp}</h3>
    <p><strong>Do not share this OTP with anyone.</strong></p>
    <p>This OTP is valid for 2 minutes. (120 seconds) </p>
    <p>If it was not you complain us at complaint.user@encryptpass.com</p>
    """
    send_otp_email(email, subject, body)
    
    return True, "OTP has been sent to your email for Account Update Verification."


# Function for Account Delete OTP Verification
def verifyAccountDeleteOTP(email: str, otp: str):
    # Normalize email (convert to lowercase)
    email = email.lower()
    # Strip whitespace from OTP
    otp = otp.strip()
    
    with otp_lock:
        try:
            # Attempt to access the OTP data for the given email
            stored_otp_data = otp_storage2[email]

            if datetime.now() > stored_otp_data["expiry"]:
                del otp_storage2[email]  # Remove expired OTP
                return False, "OTP has expired."

            if otp != stored_otp_data["otp"].strip():
                return False, "Invalid OTP."

            # Remove OTP after successful verification
            del otp_storage2[email]

            return True, "OTP Verified Successfully"
        except KeyError as e:
                # Handle the case where the email is not found in otp_storage2
                return False, "Error : ."
            

# Function for Account Forgot password
def forgotPasswordUserFunc(email: str):
    # print("DeleteUserFunc Called")
    # Generate OTP for login verification
    otp = generate_otp()
    otp_expiry = datetime.now() + timedelta(minutes=2)  # OTP valid for 2 minutes
    
    # Normalize email (convert to lowercase)
    email = email.lower()
    
    # Store OTP temporarily
    with otp_lock:
        otp_storage3[email] = {
            "otp": otp,
            "expiry": otp_expiry,
        }
    
    # Send OTP to the user's email
    subject = "OTP for Account Password Recovery - EncryptPass The Password Manager"
    body = f"""
    <h2>Welcome to EncryptPass!</h2>
    <p>Dear user , <br> Below is your OTP for Account Password Recovery:</p>
    <h3 style="color:red;">{otp}</h3>
    <p><strong>Do not share this OTP with anyone.</strong></p>
    <p>This OTP is valid for 2 minutes. (120 seconds) </p>
    <p>If it was not you complain us at complaint.user@encryptpass.com</p>
    """
    send_otp_email(email, subject, body)
    
    return True, "OTP has been sent to your email for Account Password Reset Verification."


# Function for Account ForgotPassword OTP Verification
def verifyForgotPasswordOTP(email: str, otp: str):
    # Normalize email (convert to lowercase)
    email = email.lower()
    # Strip whitespace from OTP
    otp = otp.strip()
    
    with otp_lock:
        try:
            # Attempt to access the OTP data for the given email
            stored_otp_data = otp_storage3[email]

            if datetime.now() > stored_otp_data["expiry"]:
                del otp_storage3[email]  # Remove expired OTP
                return False, "OTP has expired."

            if otp != stored_otp_data["otp"].strip():
                return False, "Invalid OTP."

            # Remove OTP after successful verification
            del otp_storage3[email]

            return True, "OTP Verified Successfully"
        except KeyError as e:
                # Handle the case where the email is not found in otp_storage2
                return False, f"Error"
            
            
# Function for Account Forgot password
def changeAccountPasswordFunc(email: str):
    # Generate OTP for login verification
    otp = generate_otp()
    otp_expiry = datetime.now() + timedelta(minutes=2)  # OTP valid for 2 minutes
    
    # Normalize email (convert to lowercase)
    email = email.lower()
    
    # Store OTP temporarily
    with otp_lock:
        otp_storage4[email] = {
            "otp": otp,
            "expiry": otp_expiry,
        }
    
    # Send OTP to the user's email
    subject = "OTP for Account Password Change From Profile - EncryptPass The Password Manager"
    body = f"""
    <h2>Welcome to EncryptPass!</h2>
    <p>Dear user , <br> Below is your OTP for Account Password Change From Profile:</p>
    <h3 style="color:red;">{otp}</h3>
    <p><strong>Do not share this OTP with anyone.</strong></p>
    <p>This OTP is valid for 2 minutes. (120 seconds) </p>
    <p>If it was not you complain us at complaint.user@encryptpass.com</p>
    """
    send_otp_email(email, subject, body)
    
    return True, "OTP has been sent to your email for Account Password Reset Verification."


# Function for Account ForgotPassword OTP Verification
def verifyChangeAccountPasswordOTP(email: str, otp: str):
    # Normalize email (convert to lowercase)
    email = email.lower()
    # Strip whitespace from OTP
    otp = otp.strip()
    
    with otp_lock:
        try:
            # Attempt to access the OTP data for the given email
            stored_otp_data = otp_storage4[email]

            if datetime.now() > stored_otp_data["expiry"]:
                del otp_storage4[email]  # Remove expired OTP
                return False, "OTP has expired."

            if otp != stored_otp_data["otp"].strip():
                return False, "Invalid OTP."

            # Remove OTP after successful verification
            del otp_storage4[email]

            return True, "OTP Verified Successfully"
        except KeyError as e:
                # Handle the case where the email is not found in otp_storage2
                return False, f"Error"