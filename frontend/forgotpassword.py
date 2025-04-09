import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
import subprocess
from tkinter import messagebox
from PIL import Image
import random
from dbConfig.userFunctions import checkUserForgotPassword, updateAccountPassword
from backend.auth import forgotPasswordUserFunc , verifyForgotPasswordOTP

# Global variables to simulate OTP and email storage

current_email = ""
current_user_id = None  # To store the user ID for password update

# Function to clear the right frame and display new content
def update_right_frame(frame, content):
    for widget in frame.winfo_children():
        widget.destroy()
    content(frame)

# Function to go back to the login window
def go_back_to_login():
    root.destroy()  # Close the current window
    subprocess.Popen(["python", "frontend/login.py"])  # Open the login window

# Email Content
def email_content(frame):
    def sendOTPtoEmail():
        global current_email, current_user_id
        email = entry_email.get()
        if not email:
            messagebox.showerror("Error", "Please enter your registered email")
            return

        # Check if the user exists in the database
        user_exists, user_id = checkUserForgotPassword(email)  # user_exists : bool , user_id : int
        if not user_exists:
            messagebox.showerror("Error", "No user found with this email")
            return

        # Store the email and user ID for later use
        current_email = email
        current_user_id = user_id

        success , message = forgotPasswordUserFunc(email)
        if success:
            messagebox.showinfo("OTP Sent", "OTP has been sent to your email. Please check your inbox.")
        else:
            messagebox.showinfo(message)
            
        update_right_frame(frame, otp_content)  # Update to OTP content

    # Email Label
    label_email = ctk.CTkLabel(frame, text="Enter Registered Email:", font=("Arial", 16), text_color="#1E90FF")
    label_email.pack(pady=10)

    # Email Entry
    global entry_email
    entry_email = ctk.CTkEntry(frame, placeholder_text="Email", width=280, height=40, border_color="#1E90FF")
    entry_email.pack(pady=10)

    # Send OTP Button
    btn_send_otp = ctk.CTkButton(frame, text="Send OTP", command=sendOTPtoEmail, width=220, height=40, 
                                 font=("Calibri", 18, "bold"), fg_color="#1E90FF", hover_color="#0077B6")
    btn_send_otp.pack(pady=10)

    # Back Button
    btn_back = ctk.CTkButton(frame, text="Back", command=go_back_to_login, width=220, height=30, 
                             fg_color="gray", hover_color="#555555")
    btn_back.pack(pady=5)

# OTP Content
def otp_content(frame):
    def verifyOTP():
        otp = entry_otp.get()
        if not otp:
            messagebox.showerror("Error", "OTP is required")
            return

        # Verify OTP
        success , message = verifyForgotPasswordOTP(current_email, otp)
        if success:
            messagebox.showinfo("Success", "OTP verified successfully!")
            update_right_frame(frame, reset_password_content)  # Update to password reset content
        else:
            messagebox.showerror("Error", "Invalid OTP")

    # OTP Label
    label_otp = ctk.CTkLabel(frame, text="Enter OTP:", font=("Arial", 16), text_color="#1E90FF")
    label_otp.pack(pady=10)

    # OTP Entry
    global entry_otp
    entry_otp = ctk.CTkEntry(frame, placeholder_text="OTP", width=280, height=40, border_color="#1E90FF")
    entry_otp.pack(pady=10)

    # Verify OTP Button
    btn_verify = ctk.CTkButton(frame, text="Verify", command=verifyOTP, width=220, height=40, 
                               font=("Calibri", 18, "bold"), fg_color="#1E90FF", hover_color="#0077B6")
    btn_verify.pack(pady=10)

    # Back Button
    btn_back = ctk.CTkButton(frame, text="Back", command=go_back_to_login, width=220, height=30, 
                             fg_color="gray", hover_color="#555555")
    btn_back.pack(pady=5)

# Password Reset Content
def reset_password_content(frame):
    def resetPassword():
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()

        if not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Update the password in the database
        success, message = updateAccountPassword(current_user_id, new_password)
        if success:
            messagebox.showinfo("Success", "Password reset successfully!")
            root.destroy()  # Close the application
            subprocess.Popen(["python", "frontend/login.py"])
        else:
            messagebox.showerror("Error", message)

    # New Password Label
    label_new_password = ctk.CTkLabel(frame, text="New Password:", font=("Arial", 16), text_color="#1E90FF")
    label_new_password.pack(pady=10 , anchor="w", fill="x")

    # New Password Entry
    global entry_new_password
    entry_new_password = ctk.CTkEntry(frame, placeholder_text="New Password", show="*", width=280, height=40, border_color="#1E90FF")
    entry_new_password.pack(pady=10)

    # Confirm Password Label
    label_confirm_password = ctk.CTkLabel(frame, text="Confirm Password:", font=("Arial", 16), text_color="#1E90FF")
    label_confirm_password.pack(pady=10 , anchor="w", fill="x")

    # Confirm Password Entry
    global entry_confirm_password
    entry_confirm_password = ctk.CTkEntry(frame, placeholder_text="Confirm Password", show="*", width=280, height=40, border_color="#1E90FF")
    entry_confirm_password.pack(pady=10)

    # Reset Password Button
    btn_reset = ctk.CTkButton(frame, text="Reset Password", command=resetPassword, width=220, height=40, 
                              font=("Calibri", 18, "bold"), fg_color="#1E90FF", hover_color="#0077B6")
    btn_reset.pack(pady=10)

    # Back Button
    btn_back = ctk.CTkButton(frame, text="Back to Login Page", command=go_back_to_login, width=220, height=30, 
                             fg_color="gray", hover_color="#555555")
    btn_back.pack(pady=5)

# Initialize Tkinter Window
ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")  # Blue theme

root = ctk.CTk()
root.geometry("700x450+500+200")  # Same size as login.py
root.title("Forgot Password")
root.resizable(False, False)

# Main Container Frame
container = ctk.CTkFrame(master=root, fg_color="white")
container.pack(fill="both", expand=True, padx=20, pady=20)

# Left Side: Image
left_frame = ctk.CTkFrame(master=container, fg_color="white", width=300, corner_radius=0)
left_frame.pack(side="left", fill="both", expand=True)

# Load and display the image
image_path = os.path.join("", "assets", "forgotPassword_sideImage.jpg")  # Correct relative path
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

# Right Side: Interactive Content
right_frame = ctk.CTkFrame(master=container, fg_color="lightblue", width=300, corner_radius=15)
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Start with the email content
update_right_frame(right_frame, email_content)

# Run the Tkinter event loop
if __name__ == "__main__":
    root.mainloop()