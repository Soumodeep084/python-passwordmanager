# Database configuration
DB_CONFIG = {
    "host": "<host>",
    "user": "",
    "password": "",
    "database": "python_passwordmanager"
}

# Email configuration
EMAIL_CONFIG = {
    "sender_email": "",
    "sender_password": "",
    "smtp_server": "",            # For Gmail
    "smtp_port": 
}

# Mailtrap.io SMTP configuration
MAILTRAP_CONFIG = {
    "smtp_server": "",                  # Mailtrap SMTP server
    "smtp_port": ,                                          # Mailtrap SMTP port
    "sender_email": "",   # Sender email (can be anything)
    "sender_password": ""                 # Mailtrap password
}


'''
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);


CREATE TABLE PasswordsLists (
    pid INT AUTO_INCREMENT PRIMARY KEY,  -- Primary key for the PasswordsLists table
    title VARCHAR(255) NOT NULL,         -- Title of the password entry
    notes TEXT,                          -- Optional notes about the password
    identifier VARCHAR(255) NOT NULL,    -- Identifier (e.g., username or email)
    password VARCHAR(5000) NOT NULL,      -- Encrypted or hashed password
    userId INT,                          -- Foreign key referencing users.id
    createdAt VARCHAR(100),
    updatedAt VARCHAR(100),
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE,  -- Cascade delete if user is deleted
);


CREATE TABLE securitydetails (
    securityid INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    ip_address VARCHAR(50),
    device_info TEXT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
);
'''
