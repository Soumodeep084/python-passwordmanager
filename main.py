import subprocess
import customtkinter as ctk
from datetime import datetime


date = datetime.now()
year = date.year

# Function to open the login page and close the current window
def open_login():
    subprocess.Popen(["python", "frontend/login.py"])
    root.destroy()  # Close the current window

# Function to open the registration page and close the current window
def open_register():
    subprocess.Popen(["python", "frontend/register.py"])
    root.destroy()  # Close the current window

# Initialize Tkinter Window
ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")  # Blue theme

root = ctk.CTk()
root.geometry("850x650+350+100")  # Slightly larger window size
root.title("encryptPass - Ultimate Password Manager")
root.resizable(False, False)

# Navbar Frame
navbar = ctk.CTkFrame(master=root, fg_color="#1E90FF", height=80 , corner_radius=0)  # Increased height
navbar.pack(fill="x", side="top")

# Company Name in Navbar
label_company = ctk.CTkLabel(master=navbar, text="EncryptPass", font=("Arial", 28, "bold"), text_color="white")
label_company.pack(side="left", padx=25, pady=10)

# Navbar Buttons Frame
navbar_buttons = ctk.CTkFrame(master=navbar, fg_color="transparent")
navbar_buttons.pack(side="right", padx=20)

# Login Button in Navbar (Slightly smaller)
btn_login_nav = ctk.CTkButton(master=navbar_buttons, text="Login", command=open_login, width=90, height=35, 
                               font=("Calibri", 14, "bold"), fg_color="#0077B6", hover_color="#005F8A")
btn_login_nav.pack(side="left", padx=8)

# Register Button in Navbar (Slightly smaller)
btn_register_nav = ctk.CTkButton(master=navbar_buttons, text="Register", command=open_register, width=90, height=35, 
                                  font=("Calibri", 14, "bold"), fg_color="#0077B6", hover_color="#005F8A")
btn_register_nav.pack(side="left", padx=8)

# Main Container Frame
container = ctk.CTkFrame(master=root, fg_color="white")
container.pack(fill="both", expand=True, padx=10, pady=8)

# Welcome Section
welcome_frame = ctk.CTkFrame(master=container, fg_color="white")
welcome_frame.pack(fill="x", pady=10 , padx=10)

label_welcome = ctk.CTkLabel(master=welcome_frame, text="Welcome to EncryptPass", font=("Arial", 26, "bold"), text_color="#1E90FF")
label_welcome.pack()

label_subtitle = ctk.CTkLabel(master=welcome_frame, text="Your Ultimate Secure Password Manager", font=("Arial", 16), text_color="#333333")
label_subtitle.pack()

# What is a Password Manager Section
what_is_frame = ctk.CTkFrame(master=container, fg_color="white")
what_is_frame.pack(fill="x", pady=8 , padx=20)

label_what_is = ctk.CTkLabel(master=what_is_frame, text="What is a Password Manager?", font=("Arial", 20, "bold"), text_color="orange")
label_what_is.pack(anchor="w", pady=2)

label_what_is_desc = ctk.CTkLabel(master=what_is_frame, 
                                  text="A password manager helps you securely store and manage passwords. "
                                        ""
                                       "It allows you to generate strong passwords and store them in an encrypted vault.",
                                  font=("Arial", 14), text_color="#333333", wraplength=750, justify="left")
label_what_is_desc.pack(anchor="w" , pady=2)

# Security Section
security_frame = ctk.CTkFrame(master=container, fg_color="white")
security_frame.pack(fill="x", pady=10 , padx=20)

label_security = ctk.CTkLabel(master=security_frame, text="Our Security", font=("Arial", 20, "bold"), text_color="purple")
label_security.pack(anchor="w", pady=2)

label_security_desc = ctk.CTkLabel(master=security_frame, 
                                   text="We use advanced encryption to protect your data. Your master password is never stored, "
                                        "ensuring complete security.",
                                   font=("Arial", 14), text_color="#333333", wraplength=750, justify="left")
label_security_desc.pack(anchor="w")

# Features Section
features_frame = ctk.CTkFrame(master=container, fg_color="white")
features_frame.pack(fill="x", pady=10 , padx=20)

label_features = ctk.CTkLabel(master=features_frame, text="Our Features", font=("Arial", 20, "bold"), text_color="#1E90FF")
label_features.pack(anchor="w", pady=2)

features_list = [
    "🔒 Inbuilt Password Generator - Create strong passwords.",
    "🔐 High-Security Encryption - Keep your passwords safe.",
    "📂 Secure Vault - Store all your passwords in one place.",
    "🌐 Multi-Device Access - Access from anywhere.",
    "🛡️Two-Factor Authentication - Extra security for your account."
]

for feature in features_list:
    ctk.CTkLabel(master=features_frame, text=feature, font=("Arial", 14), text_color="#333333", wraplength=750, justify="left").pack(anchor="w", pady=2)


# Create the label
bottom_label = ctk.CTkLabel(
    master=container, 
    text="Want to keep your passwords secure? Create an account and start accessing now!", 
    font=("Arial", 16, "bold"), 
    text_color="red"
)
bottom_label.pack(side="bottom", pady=10)  # Add padding to keep it above the footer

# Footer Frame
footer = ctk.CTkFrame(master=root, fg_color="#1E90FF", height=50)
footer.pack(fill="x", side="bottom" , pady=10)

# Footer Label
label_footer = ctk.CTkLabel(master=footer, text=f"© {year} EncryptPass. All rights reserved.", font=("Arial", 14), text_color="white")
label_footer.pack(pady=0)

label_footer1 = ctk.CTkLabel(master=footer, text="Created By Mr Soumodeep Dutta", font=("Arial", 14 , "bold"), text_color="black")
label_footer1.pack(pady=0)

# Run the Tkinter event loop
root.mainloop()
