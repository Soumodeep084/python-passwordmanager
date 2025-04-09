import customtkinter as ctk
import pyperclip
import random
import string
from tkinter import messagebox

from config.Encryption import decrypt_pass
from dbConfig.passwordFunctions import getPasswordForUpdate, updatePassword, deletePassword , addNewPassword

# Add Password Box
def addPasswordBox(parent , userId : int , userEmail : str):
    '''
        Displays a form to update the password details within the parent frame.
    '''
    # Clear the parent frame before adding new widgets
    for widget in parent.winfo_children():
        widget.destroy()
        
    # Title Label
    ctk.CTkLabel(parent, text="Add New Password Details", font=("Arial", 20, "bold")).pack(pady=10)

    # Title Field
    ctk.CTkLabel(parent, text="Title:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
    entry_title = ctk.CTkEntry(parent, width=300)
    entry_title.pack(pady=5)

    # Notes Field
    ctk.CTkLabel(parent, text="Notes:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
    entry_notes = ctk.CTkEntry(parent, width=300)
    entry_notes.pack(pady=5)

    # Identifier Field
    ctk.CTkLabel(parent, text="Identifier:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
    entry_identifier = ctk.CTkEntry(parent, width=300)
    entry_identifier.pack(pady=5)

    # Password Field
    password_var = ctk.StringVar()  # Store password initially
    show_password = False  # Track visibility state

    def toggle_password():
        """Toggles between showing and hiding the password."""
        nonlocal show_password
        if show_password:
            entry_password.configure(show="*")
            show_hide_button.configure(text="Show")
        else:
            entry_password.configure(show="")
            show_hide_button.configure(text="Hide")
        show_password = not show_password  # Toggle state

    ctk.CTkLabel(parent, text="Password:", font=("Arial", 14), anchor="w").pack(fill="x", padx=240)

    # Frame to hold password entry and button
    password_frame = ctk.CTkFrame(parent , fg_color="transparent")
    password_frame.pack(pady=5)

    entry_password = ctk.CTkEntry(password_frame, width=245, show="*")
    entry_password.pack(side="left", padx=(0, 5))

    show_hide_button = ctk.CTkButton(password_frame, text="Show", width=40, command=toggle_password)
    show_hide_button.pack(side="left")

    # Function to handle the "Update Password" button click
    def handle_add():
        # Get the updated values from the input fields
        title = entry_title.get()
        notes = entry_notes.get()
        identifier = entry_identifier.get()
        password = entry_password.get()

        # Call the backend function to update the password
        result = addNewPassword(userId, userEmail, title, notes, identifier, password)

        if result[0]:  # If update is successful
            messagebox.showinfo("Success", "Password Added Successfully!")
            
            # Clear input fields
            entry_title.delete(0, 'end')
            entry_notes.delete(0, 'end')
            entry_identifier.delete(0, 'end')
            entry_password.delete(0, 'end')
        
        else:
            messagebox.showerror("Error", result[1])
            
    # Function to handle the "Back" button click
    def handle_back():
        # To Prevent circular import
        from passwordList import password_List_OverviewBox
        
        for widget in parent.winfo_children():  # Clear the parent frame and show the password list again
            widget.destroy()
        password_List_OverviewBox(parent , userId, userEmail)  # Assuming this function exists

    # Frame to center buttons
    button_frame = ctk.CTkFrame(parent , fg_color="transparent")
    button_frame.pack(pady=20)

    # Back Button
    ctk.CTkButton(button_frame, text="Back", width=120, fg_color="#FF5733", hover_color="#e64a19",
                  command=handle_back).pack(side="left", padx=10)
    
    # Update Password Button
    ctk.CTkButton(button_frame, text="Add Password", width=120, fg_color="#4CAF50", hover_color="#45a049",
                  command=handle_add).pack(side="left", padx=10)


# Update Password Box
def updatePasswordBox(parent, userId: int, userEmail: str, pid: int):
    '''
        Displays a form to update the password details within the parent frame.
    '''
    # Clear the parent frame before adding new widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Fetch the current password details
    result = getPasswordForUpdate(userId, userEmail, pid)
    if not result[0]:  # If fetching details fails
        messagebox.showerror("Error", result[1])
        return

    password_data = result[1]  # Current password details

    # Title Label
    ctk.CTkLabel(parent, text="Update Password Details", font=("Arial", 20, "bold")).pack(pady=10)

    # Title Field
    ctk.CTkLabel(parent, text="Title:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
    entry_title = ctk.CTkEntry(parent, width=300)
    entry_title.insert(0, password_data[1])
    entry_title.pack(pady=5)

    # Notes Field
    ctk.CTkLabel(parent, text="Notes:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
    entry_notes = ctk.CTkEntry(parent, width=300)
    entry_notes.insert(0, password_data[2])
    entry_notes.pack(pady=5)

    # Identifier Field
    ctk.CTkLabel(parent, text="Identifier:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
    entry_identifier = ctk.CTkEntry(parent, width=300)
    entry_identifier.insert(0,password_data[3])
    entry_identifier.pack(pady=5)

    # Password Field
    password_var = ctk.StringVar(value= decrypt_pass(password_data[4]))  # Store password initially
    show_password = False  # Track visibility state

    def toggle_password():
        """Toggles between showing and hiding the password."""
        nonlocal show_password
        if show_password:
            entry_password.configure(show="*")
            show_hide_button.configure(text="Show")
        else:
            entry_password.configure(show="")
            show_hide_button.configure(text="Hide")
        show_password = not show_password  # Toggle state

    ctk.CTkLabel(parent, text="Password:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)

    # Frame to hold password entry and button
    password_frame = ctk.CTkFrame(parent , fg_color="transparent")
    password_frame.pack(pady=5)

    entry_password = ctk.CTkEntry(password_frame, width=245, show="*")
    entry_password.insert(0, password_var.get())  # Pre-fill with current password
    entry_password.pack(side="left", padx=(0, 5))

    show_hide_button = ctk.CTkButton(password_frame, text="Show", width=40, command=toggle_password)
    show_hide_button.pack(side="left")

    # Function to handle the "Update Password" button click
    def handle_update():
        # Get the updated values from the input fields
        updated_title = entry_title.get()
        updated_notes = entry_notes.get()
        updated_identifier = entry_identifier.get()
        updated_password = entry_password.get()

        # Call the backend function to update the password
        result = updatePassword(userId, userEmail, pid, updated_title, updated_notes, updated_identifier, updated_password)

        if result[0]:  # If update is successful
            messagebox.showinfo("Success", "Password updated successfully!")
        else:
            messagebox.showerror("Error", result[1])

    # Function to handle the "Back" button click
    def handle_back():
        # To Prevent circular import
        from passwordList import password_List_OverviewBox
        
        for widget in parent.winfo_children():  # Clear the parent frame and show the password list again
            widget.destroy()
        password_List_OverviewBox(parent , userId, userEmail)  # Assuming this function exists

    # Frame to center buttons
    button_frame = ctk.CTkFrame(parent , fg_color="transparent")
    button_frame.pack(pady=20)

    # Back Button
    ctk.CTkButton(button_frame, text="Back", width=120, fg_color="#FF5733", hover_color="#e64a19",
                  command=handle_back).pack(side="left", padx=10)
    
    # Update Password Button
    ctk.CTkButton(button_frame, text="Update Password", width=120, fg_color="#4CAF50", hover_color="#45a049",
                  command=handle_update).pack(side="left", padx=10)


# Delete Password Box
def deletePasswordBox(userId: int, userEmail: str, pid: int):
    """
    Displays a confirmation dialog to delete the password.
    If the user confirms, the password is deleted.
    """
    # Show a confirmation dialog
    confirm = messagebox.askyesno("Delete Password", "Are you sure you want to delete this password?")

    if confirm:  # If the user clicks "Yes"
        result = deletePassword(userId, userEmail, pid)
        if result[0]:  # If deletion is successful
            messagebox.showinfo("Success", "Password deleted successfully!")
        else:
            messagebox.showerror("Error", result[1])
            

# Generates a random password based on selected criteria.
def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    if not char_pool:
        return "Select at least one option!"

    return "".join(random.choice(char_pool) for _ in range(length))


# Function to Password Generator Box
def passwordGeneratorBox(parent):
    # Clear existing content
    for widget in parent.winfo_children():
        widget.destroy()

    # Configure CustomTkinter Theme
    ctk.set_appearance_mode("light")  # Light theme
    ctk.set_default_color_theme("blue")  # Blue theme

    # Main Frame
    main_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title Label
    title_label = ctk.CTkLabel(main_frame, text="🔑 Password Generator", font=("Arial", 20, "bold"), text_color="#1E90FF")
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Password Length Slider
    length_var = ctk.IntVar(value=12)
    length_label = ctk.CTkLabel(main_frame, text="Password Length:", font=("Arial", 14))
    length_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    length_slider = ctk.CTkSlider(main_frame, from_=4, to=32, number_of_steps=28, variable=length_var )
    length_slider.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Label to show selected password length
    length_value_label = ctk.CTkLabel(main_frame, text=f"Selected Length: {length_var.get()}", font=("Arial", 12))
    length_value_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

    # Update length value label when slider is moved
    def update_length_label(*args):
        length_value_label.configure(text=f"Selected Length: {length_var.get()}")

    length_var.trace("w", update_length_label)

    # Checkboxes for character inclusion
    options = {
        "Uppercase": ctk.BooleanVar(value=True),
        "Lowercase": ctk.BooleanVar(value=True),
        "Numbers": ctk.BooleanVar(value=True),
        "Symbols": ctk.BooleanVar(value=False),
    }

    checkboxes = []
    for i, (text, var) in enumerate(options.items()):
        checkbox = ctk.CTkCheckBox(main_frame, text=text, variable=var, font=("Arial", 14))
        checkbox.grid(row=3 + i, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        checkboxes.append(checkbox)

    # Password Display (Read-Only)
    password_var = ctk.StringVar(value="Your password will appear here")
    password_entry = ctk.CTkEntry(main_frame, textvariable=password_var, font=("Arial", 14), justify="center", width=300, state="readonly")
    password_entry.grid(row=7, column=0, columnspan=2, pady=(10, 5))

    # Generate Password Function
    def on_generate():
        password = generate_password(
            length_var.get(),
            options["Uppercase"].get(),
            options["Lowercase"].get(),
            options["Numbers"].get(),
            options["Symbols"].get()
        )
        password_var.set(password)

    generate_button = ctk.CTkButton(main_frame, text="🔄 Generate Password", font=("Arial", 14), command=on_generate)
    generate_button.grid(row=8, column=0, columnspan=2, pady=10)

    # Copy to Clipboard Function
    def copy_to_clipboard():
        if password_var.get() not in ("Your password will appear here" , "Select at least one option!"):
            pyperclip.copy(password_var.get())
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showinfo("Copied" , "Please Select options to Generate Password")
            

    copy_button = ctk.CTkButton(main_frame, text="📋 Copy to Clipboard", font=("Arial", 14), command=copy_to_clipboard)
    copy_button.grid(row=9, column=0, columnspan=2, pady=(0, 10))

    # Configure grid weights for responsive layout
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)