import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
import subprocess 
from tkinter import messagebox
from PIL import Image  

from backend.auth import loginUser, verifyLoginOTP
from dashboard import open_dashboard

# Function to handle user login
def login():
    username_or_email = entry_username_or_email.get()
    password = entry_password.get()
    
    # Validate fields
    if not username_or_email or not password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    # Login user
    success, message = loginUser(username_or_email, password)
    if success:
        messagebox.showinfo("Success", message)
        open_otp_window(username_or_email)  # Open OTP window for verification
    else:
        messagebox.showerror("Error", message)


# Function to open OTP verification window
def open_otp_window(username_or_email: str):
    # Verify Button Function
    def verify():
        otp = entry_otp.get()
        if not otp:
            messagebox.showerror("Error", "OTP is required")
            return
        
        # Verify OTP
        result = verifyLoginOTP(username_or_email, otp)

        if len(result) == 2:  # If only success and message are returned
            success, message = result
            user = None  # No user data available
        else:
            success, message, user = result
        # print("success , message : "  , success , message)    
        if success:
            messagebox.showinfo("Success", message)
            otp_window.destroy()  # Close OTP window
            root.destroy()        # Close login window
            open_dashboard(int(user["id"]), user["email"])  # Open dashboard (replace with actual user data)
        else:
            messagebox.showerror("Error", message)

    otp_window = ctk.CTkToplevel(root)
    otp_window.geometry("300x200+250+150")
    otp_window.title("Verify OTP")
    otp_window.resizable(False, False)

    # OTP Label
    label_otp = ctk.CTkLabel(otp_window, text="Enter OTP:", font=("Arial", 16))
    label_otp.pack(pady=7)

    # OTP Entry
    entry_otp = ctk.CTkEntry(otp_window, placeholder_text="OTP", width=200, height=40)
    entry_otp.pack(pady=7)

    btn_verify = ctk.CTkButton(otp_window, text="Verify", command=verify, width=200, height=40)
    btn_verify.pack(pady=7)

# Function to open the Register page
def open_register():
    root.destroy()
    subprocess.Popen(["python", "frontend/register.py"])  # Open Register.py

# Function to open the Forgot Password page
def open_forgot_password():
    root.destroy()
    subprocess.Popen(["python", "frontend/forgotpassword.py"])  # Open ForgotPassword.py

# Initialize Tkinter Window
ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")  # Blue theme

root = ctk.CTk()
root.geometry("700x450+500+200")  # Wider window to accommodate the side image
root.title("Login Page")
root.resizable(False, False)

# Main Container Frame
container = ctk.CTkFrame(master=root, fg_color="white")
container.pack(fill="both", expand=True, padx=20, pady=20)

# Left Side: Image
left_frame = ctk.CTkFrame(master=container, fg_color="white", width=300, corner_radius=0)
left_frame.pack(side="left", fill="both", expand=True)

# Load and display the image
image_path = os.path.join("", "assets", "login_sideImage.jpg")  # Correct relative path
try:
    # Open the image using PIL
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((400, 500), Image.Resampling.LANCZOS)  # Resize image to fit the frame

    # Convert PIL image to CTkImage
    ctk_image = ctk.CTkImage(pil_image, size=(250, 250))

    # Display the image using CTkLabel
    image_label = ctk.CTkLabel(master=left_frame, image=ctk_image, text="")
    image_label.pack(fill="both", expand=True)
except FileNotFoundError:
    messagebox.showerror("Error", "Image file not found. Please check the path.")

# Right Side: Login Form
right_frame = ctk.CTkFrame(master=container, fg_color="lightblue", width=300, corner_radius=15)
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Title Label
label_title = ctk.CTkLabel(master=right_frame, text="Login", font=("Arial", 26, "bold"), text_color="#1E90FF")
label_title.pack(pady=10)

# Username/Email Entry
entry_username_or_email = ctk.CTkEntry(master=right_frame, placeholder_text="Username or Email", width=280, height=40, border_color="#1E90FF")
entry_username_or_email.pack(pady=10)

# Password Entry
entry_password = ctk.CTkEntry(master=right_frame, placeholder_text="Password", show="*", width=280, height=40, border_color="#1E90FF")
entry_password.pack(pady=10)

# Forgot Password Label (Clickable)
label_forgot_password = ctk.CTkLabel(master=right_frame, text="Forgot Password? Click Here", font=("Arial", 12), text_color="red", cursor="hand2")
label_forgot_password.pack(pady=5)
label_forgot_password.bind("<Button-1>", lambda event: open_forgot_password())  # Make it clickable

# Login Button
btn_login = ctk.CTkButton(master=right_frame, text="Login", command=login, width=220, height=40, 
                           font=("Calibri", 18, "bold"), fg_color="#1E90FF", hover_color="#0077B6")
btn_login.pack(pady=10)

# "Don't have an account? Register Now" Label
label_register = ctk.CTkLabel(master=right_frame, text="Don't have an account? ", font=("Arial", 12), text_color="black")
label_register.pack(pady=5)

# Clickable "Register Now" Button
btn_register = ctk.CTkButton(master=right_frame, text="Register Now", width=100, height=30, fg_color="transparent",
                             text_color="red", hover_color="#d2fcfc", command=open_register)
btn_register.pack()

# Run the Tkinter event loop
root.mainloop()