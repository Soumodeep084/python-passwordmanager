# 🔐 Password Manager

A secure and user-friendly **Password Manager** built with **Python**, **CustomTkinter** for GUI, and **MySQL** for backend database storage. This application also supports **email notification** features using your Gmail account.

---

## 🚀 Features

- Modern GUI using CustomTkinter  
- Secure password storage with MySQL  
- Email functionality for password recovery or verification  
- Configurable database and email credentials  
- Easy-to-use interface  

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/password-manager.git
cd password-manager
```

### 2. Configure Database and Email Credentials

Open the file `settings.py` and add your credentials:

```python
DB_USERNAME = "your_mysql_username"
DB_PASSWORD = "your_mysql_password"
EMAIL_USERNAME = "your_gmail_username"
EMAIL_PASSWORD = "your_gmail_app_password"
```

> ⚠️ For Gmail, make sure "Less secure app access" is enabled or use App Passwords of Google and it will be present if 2-step verification is on.

### 3. Enable Real Email Sending

In the `email_service.py` file:  
- **Uncomment** the Gmail email sending code  
- **Comment out** the Mailtrap (testing) email code  

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python main.py
```

---

## 🧾 Requirements

- Python 3.8 or higher  
- MySQL server installed and running  
- Internet connection for email sending  
- Modules listed in `requirements.txt` (CustomTkinter, mysql-connector-python, etc.)

---

## ⚙️ Notes

- Ensure your MySQL server is running before starting the app 

---

## 📧 Email Feature

This app sends real emails using your Gmail account for:

- Verification codes  
- Password recovery  
- Alerts (if implemented)  

To enable this:  
- Make sure `email_service.py` is using the Gmail code block  
- Your Gmail credentials must be valid and app-access enabled  

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

