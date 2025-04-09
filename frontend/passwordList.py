import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "venv", "Lib", "site-packages")))


import customtkinter as ctk
import pyperclip 
from tkinter import messagebox

from dbConfig.passwordFunctions import getSpecificUserPasswords
from config.Encryption import decrypt_pass

# Cards to show Passwords
def create_password_card(parent, userId: int, userEmail: str, cardIdx: int, pid: int, title: str, notes: str, identifier: str, password: str):
    # To prevent circular import
    from passwordOperations import updatePasswordBox, deletePasswordBox

    # Copy Password Function
    def copyPassword():
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password Copied to clipboard")

    # Card Frame
    card = ctk.CTkFrame(parent, fg_color="#F0F0F0", corner_radius=10)
    card.grid(row=cardIdx // 2, column=cardIdx % 2, padx=10, pady=10, sticky="nsew")  # Use grid for layout

    # Title
    ctk.CTkLabel(card, text=f"{pid}. {title}", font=("Arial", 16, "bold"), text_color="#1E90FF").pack(anchor="w", padx=10, pady=5)

    # Username
    ctk.CTkLabel(card, text=f"Identifier: {identifier}", font=("Arial", 14)).pack(anchor="w", padx=10)

    # Notes (if available)
    if notes:  # Only show notes if they exist
        ctk.CTkLabel(card, text=f"Notes: {notes}", font=("Arial", 14), wraplength=200).pack(anchor="w", padx=10, pady=5)

    # Password Section
    password_frame = ctk.CTkFrame(card, fg_color="transparent", width=400)
    password_frame.pack(anchor="w", padx=10, pady=5, fill="x")

    # Password (hidden by default)
    password_var = ctk.StringVar(value=password)

    def toggle_password():
        """Toggles between showing and hiding the password."""
        if entry_password.cget("show") == "*":  # If password is hidden
            entry_password.configure(show="")   # Show the password
            show_hide_button.configure(text="Hide")
        else:  # If password is visible
            entry_password.configure(show="*")  # Hide the password
            show_hide_button.configure(text="Show")

    # Password Entry Field
    entry_password = ctk.CTkEntry(password_frame, textvariable=password_var, font=("Arial", 14), width=200, show="*")
    entry_password.pack(side="left", padx=5)

    # Show/Hide Button
    show_hide_button = ctk.CTkButton(password_frame, text="Show", width=50, anchor="center" , command=toggle_password)
    show_hide_button.pack(side="left", padx=5)

    # Copy to Clipboard Button
    ctk.CTkButton(password_frame, text="📋", width=10, command=copyPassword).pack(side="left", padx=5)

    # Update and Delete Buttons
    button_frame = ctk.CTkFrame(card, fg_color="transparent")
    button_frame.pack(anchor="e", padx=10, pady=10, fill="x")

    # Update Button
    ctk.CTkButton(button_frame, text="Update", width=80, fg_color="#4CAF50", hover_color="#45a049",
                  command=lambda: updatePasswordBox(parent, userId, userEmail, pid)).pack(side="left", padx=5)

    # Delete Button
    ctk.CTkButton(button_frame, text="Delete", width=80, fg_color="#FF5733", hover_color="#e64a19",
                  command=lambda: deletePasswordBox(userId, userEmail, pid)).pack(side="left", padx=5)


# Password List Overview
def password_List_OverviewBox(parent_frame , userId: int, userEmail: str):
    # Fetches passwords for the given user and displays them as cards in the parent frame.
    result = getSpecificUserPasswords(userId, userEmail)
    success = result[0]
    if success:  # If passwords are fetched successfully
        passwords = result[1]  # List of passwords

        # Clear the parent frame before adding new cards
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Configure grid layout for the parent frame
        parent_frame.grid_columnconfigure(0, weight=1)  # Column 0
        parent_frame.grid_columnconfigure(1, weight=1)  # Column 1

        # Iterate over the passwords and create cards
        for idx, password_data in enumerate(passwords):
            pid = password_data[0]
            title = password_data[1]
            notes = password_data[2]
            identifier = password_data[3]
            password = password_data[4]

            # Create a card for each password
            create_password_card(parent_frame, userId , userEmail , idx, pid, title, notes, identifier, decrypt_pass(password))
    else:
        # If no passwords are found or an error occurs, display a message
        ctk.CTkLabel(parent_frame, text=result[1], font=("Arial", 14), text_color="red").pack(pady=20)