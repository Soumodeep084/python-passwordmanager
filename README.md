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

### Screenshots:
Here are some of the screenshots of the project:

![image](https://github.com/user-attachments/assets/05b2cd97-6720-4670-879a-b2556336ea96)

![image](https://github.com/user-attachments/assets/b28320f4-44ba-4fa6-b769-4aa131170ef6)

![image](https://github.com/user-attachments/assets/c25e403e-26f8-47a8-ab38-8d85678e5488)

![image](https://github.com/user-attachments/assets/a4087b04-d62f-49ca-aa15-de2c5f8d680c)

![image](https://github.com/user-attachments/assets/3918b657-3670-4fbf-803a-57933008c763)


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

