import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
import subprocess  
from PIL import Image 
from tkinter import messagebox

from backend.auth import registerUser, verifyAccountOTP

# Function to handle user registration
def register():
    name = entry_name.get()
    username = entry_username.get()
    email = entry_email.get()  # This should be the email address
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    
    # Validate fields
    if not name or not username or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
    # Register user
    success, message = registerUser(name, username, email, password, confirm_password)
    if success:
        messagebox.showinfo("Success", message)
        open_otp_window(email)  # Pass the correct email address
    else:
        messagebox.showerror("Error", message)

# Function to open OTP verification window
def open_otp_window(email):
    # Verify Button
    def verify():
        otp = entry_otp.get()
        if not otp:
            messagebox.showerror("Error", "OTP is required")
            return
        
        # Verify OTP
        success, message = verifyAccountOTP(email, otp)  
        if success:
            messagebox.showinfo("Success", message)
            otp_window.destroy()                # Close OTP window
            root.destroy()                      # Close register window
            subprocess.Popen(["python", "frontend/login.py"])
        else:
            messagebox.showerror("Error", message)
            

    otp_window = ctk.CTkToplevel(root)
    otp_window.geometry("300x200+200+150")
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

# Function to open the login page
def open_login():
    root.destroy()
    subprocess.Popen(["python", "frontend/login.py"])  # Open Login.py

# Initialize Tkinter Window
ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")  # Blue theme

root = ctk.CTk()
root.geometry("900x580+400+150")  # Wider window to accommodate the side image
root.title("Register Page")
root.resizable(False, False)

# Main Container Frame
container = ctk.CTkFrame(master=root, fg_color="white")
container.pack(fill="both", expand=True, padx=20, pady=20)

# Left Side: Image
left_frame = ctk.CTkFrame(master=container, fg_color="white", width=380, corner_radius=0)
left_frame.pack(side="left", fill="both", expand=True)

# Load and display the image
image_path = os.path.join("", "assets", "register_sideImage.jpg")  # Correct relative path
try:
    # Open the image using PIL
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((400, 600), Image.Resampling.LANCZOS)  # Resize image to fit the frame

    # Convert PIL image to CTkImage
    ctk_image = ctk.CTkImage(pil_image, size=(400, 600))

    # Display the image using CTkLabel
    image_label = ctk.CTkLabel(master=left_frame, image=ctk_image, text="")
    image_label.pack(fill="both", expand=True)
except FileNotFoundError:
    messagebox.showerror("Error", "Image file not found. Please check the path.")

# Right Side: Registration Form
right_frame = ctk.CTkFrame(master=container, fg_color="#a1f7f6", width=400, corner_radius=15)
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Title Label
label_title = ctk.CTkLabel(master=right_frame, text="Register", font=("Arial", 26, "bold"), text_color="#1E90FF")
label_title.pack(pady=20)

# Name Entry
entry_name = ctk.CTkEntry(master=right_frame, placeholder_text="Full Name", width=280, height=40, border_color="#1E90FF")
entry_name.pack(pady=7)

# Username Entry
entry_username = ctk.CTkEntry(master=right_frame, placeholder_text="Username", width=280, height=40, border_color="#1E90FF")
entry_username.pack(pady=7)

# Email Entry
entry_email = ctk.CTkEntry(master=right_frame, placeholder_text="Email", width=280, height=40, border_color="#1E90FF")
entry_email.pack(pady=7)

# Password Entry
entry_password = ctk.CTkEntry(master=right_frame, placeholder_text="Password", show="*", width=280, height=40, border_color="#1E90FF")
entry_password.pack(pady=7)

# Confirm Password Entry
entry_confirm_password = ctk.CTkEntry(master=right_frame, placeholder_text="Confirm Password", show="*", width=280, height=40, border_color="#1E90FF")
entry_confirm_password.pack(pady=8)

# Register Button
btn_register = ctk.CTkButton(master=right_frame, text="Register", command=register, width=220, height=40, 
                              font=("Calibri", 18, "bold"), fg_color="#1E90FF", hover_color="#0077B6")
btn_register.pack(pady=15)

# "Have an account? Login Now" Label
label_login = ctk.CTkLabel(master=right_frame, text="Have an account? ", font=("Arial", 12), text_color="black")
label_login.pack(pady=1)

# Clickable "Login Now" Button
btn_login = ctk.CTkButton(master=right_frame, text="Login Now", width=100, height=30, fg_color="transparent",
                           text_color="red", hover_color="#d2fcfc", command=open_login)
btn_login.pack()

# Run the Tkinter event loop
root.mainloop()