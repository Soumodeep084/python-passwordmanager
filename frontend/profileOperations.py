import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from dbConfig.userFunctions import getUserAccountDetails, updateUserAccount , checkAccountPassword, updateAccountPassword
from backend.auth import updateAccountUserFunc, verifyAccountUpdateOTP , changeAccountPasswordFunc, verifyChangeAccountPasswordOTP

from dashboard import open_dashboard

# Function to open OTP verification window
def open_otp_window(parent, userId: int, updated_name : str , updated_username : str, updatedEmail: str):
    # Verify Button Function
    
    def verify():
        otp = entry_otp.get()
        if not otp:
            messagebox.showerror("Error", "OTP is required")
            return

        success, message = verifyAccountUpdateOTP(updatedEmail, otp)
        if success:
            messagebox.showinfo("Success", message)
            otp_window.destroy()                    # Close OTP window
            updateUserAccount(userId, updated_name, updated_username, updatedEmail)
            messagebox.showinfo("Confirmation" , "Account Details Updated Successfully")
            parent.winfo_toplevel().destroy()
            open_dashboard(userId , updatedEmail)
            
        else:
            messagebox.showerror("Error", message)
    
    otp_window = ctk.CTkToplevel(parent)  # Corrected `root` to `parent`
    otp_window.geometry("300x200+250+150")
    otp_window.title("Verify OTP")
    otp_window.resizable(False, False)

    label_otp = ctk.CTkLabel(otp_window, text="Enter OTP:", font=("Arial", 16))
    label_otp.pack(pady=7)

    entry_otp = ctk.CTkEntry(otp_window, placeholder_text="OTP", width=200, height=40)
    entry_otp.pack(pady=7)

    btn_verify = ctk.CTkButton(otp_window, text="Verify", command=verify, width=200, height=40)
    btn_verify.pack(pady=7)


# Function to Edit Profile
def editProfileBox(parent, userId, userEmail):
    '''
    Displays a form to update user account details within the parent frame.
    '''
    # Clear the parent frame before adding new widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Fetch the current user account details
    result = getUserAccountDetails(userId, userEmail)
    if not result[0]:  # If fetching details fails
        messagebox.showerror("Error", result[1])
        return

    user_data = result[1]  # User details (dictionary)

    # Main container frame
    main_frame = ctk.CTkFrame(parent, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Left frame for user account update form
    form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    form_frame.pack(side="left", fill="both", expand=True, padx=10)

    # Right frame for user details (read-only)
    details_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    details_frame.pack(side="right", fill="y", padx=10)

    # Title Label for User Account Update Form
    ctk.CTkLabel(form_frame, text="Update User Account Details", font=("Arial", 20, "bold")).pack(pady=10)

    # Name Field
    ctk.CTkLabel(form_frame, text="Name:", font=("Arial", 14), anchor="w").pack(fill="x", padx=55)
    entry_name = ctk.CTkEntry(form_frame, width=300)
    entry_name.insert(0, user_data["name"])  # Access dictionary key "name"
    entry_name.pack(pady=5)

    # Username Field
    ctk.CTkLabel(form_frame, text="Username:", font=("Arial", 14), anchor="w").pack(fill="x", padx=55)
    entry_username = ctk.CTkEntry(form_frame, width=300)
    entry_username.insert(0, user_data["username"])  # Access dictionary key "username"
    entry_username.pack(pady=5)

    # Email Field
    ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 14), anchor="w").pack(fill="x", padx=55)
    entry_email = ctk.CTkEntry(form_frame, width=300)
    entry_email.insert(0, user_data["email"])  # Access dictionary key "email"
    entry_email.pack(pady=5)

    # User Details Section (Read-Only)
    ctk.CTkLabel(details_frame, text="User Details", font=("Arial", 20, "bold")).pack(pady=10)

    now = datetime.now()
    year = str(now.year)
    ID = "ENCP" + year + "0" + str(user_data['id'])
    ctk.CTkLabel(details_frame, text=f"ID: {ID}", font=("Arial", 14), anchor="w").pack(fill="x", padx=10, pady=5)

    # Verification Status (Read-Only)
    verification_status = "Verified" if user_data["isVerified"] else "Not Verified"
    ctk.CTkLabel(details_frame, text=f"Status: {verification_status}", font=("Arial", 14), anchor="w").pack(fill="x", padx=10, pady=5)

    # Created At (Read-Only)
    ctk.CTkLabel(details_frame, text=f"Created At: {user_data['createdAt']}", font=("Arial", 14), anchor="w").pack(fill="x", padx=10, pady=5)

    # Updated At (Read-Only, only show if not NULL)
    if user_data["updatedAt"]:  # If updatedAt is not None
        ctk.CTkLabel(details_frame, text=f"Updated At: {user_data['updatedAt']}", font=("Arial", 14), anchor="w").pack(fill="x", padx=10, pady=5)
        
    # Function to handle the "Update Account" button click
    def handle_update():
        updated_name = entry_name.get()
        updated_username = entry_username.get()
        updated_email = entry_email.get()

        username_changed = updated_username != user_data["username"]
        email_changed = updated_email != user_data["email"]

        otp_email = user_data["email"]
        if username_changed or email_changed:
            if email_changed:
                otp_email = updated_email
                messagebox.showinfo("Confirmation" , "OTP has been send successfully to your New Updated Registered Email")
            else:
                messagebox.showinfo("Confirmation" , "OTP has been send successfully to your Registered Email")
                
            success, message = updateAccountUserFunc(otp_email)
            if not success:
                messagebox.showerror("Error", message)
                return
            
            open_otp_window(parent, userId , updated_name, updated_username , otp_email)
            
        else:
            updateUserAccount(userId, updated_name, updated_username, otp_email)
            parent.winfo_toplevel().destroy()  # Close main edit profile window
            messagebox.showinfo("Updated", "Account Updated Successfully")
            open_dashboard(userId, otp_email)


    # Frame to center buttons
    button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    button_frame.pack(pady=20)

    # Update Account Button
    ctk.CTkButton(button_frame, text="Update Account", width=120, fg_color="#4CAF50", hover_color="#45a049",
                  command=handle_update).pack(side="left", padx=10)
    
    
# Function To Update Account Password
def changeAccountPasswordBox(parent, userId: int, userEmail: str):
    """
    Displays a form to change the account password within the parent frame.
    """
    # Clear the parent frame before adding new widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Title Label
    ctk.CTkLabel(parent, text="Change Account Password", font=("Arial", 20, "bold")).pack(pady=10)

    # Current Password Field
    currentPassLabel =  ctk.CTkLabel(parent, text="Current Password:", font=("Arial", 14), anchor="w")
    currentPassLabel.pack(fill="x", padx=210)
    entry_current_password = ctk.CTkEntry(parent, width=300, show="*")
    entry_current_password.pack(pady=5)

    # Function to handle the "Next" button click for current password verification
    def handle_next():
        current_password = entry_current_password.get()

        success , message = checkAccountPassword(userId, current_password)
        # Verify the current password
        if success:
            # Send OTP to the user's email
            otp_result = changeAccountPasswordFunc(userEmail)
            if otp_result[0]:
                messagebox.showinfo("OTP Sent", "An OTP has been sent to your email.")
                show_otp_box()  # Show the OTP input box
            else:
                messagebox.showerror("Error", otp_result[1])
        else:
            messagebox.showerror("Error", "Incorrect current password.")

    # Function to show the OTP input box
    def show_otp_box():
        # Clear the current password field and button
        currentPassLabel.destroy()
        entry_current_password.destroy()
        next_button.destroy()

        # OTP Field
        ctk.CTkLabel(parent, text="Enter OTP:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
        entry_otp = ctk.CTkEntry(parent, width=300)
        entry_otp.pack(pady=5)

        # Function to handle the "Verify OTP" button click
        def handle_verify_otp():
            otp = entry_otp.get()

            # Verify the OTP
            otp_verification_result = verifyChangeAccountPasswordOTP(userEmail, otp)
            if otp_verification_result[0]:
                messagebox.showinfo("OTP Verified", "OTP verification successful.")
                show_new_password_box()  # Show the new password input box
            else:
                messagebox.showerror("Error", otp_verification_result[1])

        # Verify OTP Button
        verify_otp_button = ctk.CTkButton(parent, text="Verify OTP", width=120, fg_color="#4CAF50", hover_color="#45a049",
                                          command=handle_verify_otp)
        verify_otp_button.pack(pady=10)

    # Function to show the new password input box
    def show_new_password_box():
        # Clear the OTP field and button
        for widget in parent.winfo_children():
            widget.destroy()

        # New Password Field
        ctk.CTkLabel(parent, text="Change Account Password", font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(parent, text="New Password:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
        entry_new_password = ctk.CTkEntry(parent, width=300, show="*")
        entry_new_password.pack(pady=5)

        # Confirm New Password Field
        ctk.CTkLabel(parent, text="Confirm New Password:", font=("Arial", 14), anchor="w").pack(fill="x", padx=210)
        entry_confirm_new_password = ctk.CTkEntry(parent, width=300, show="*")
        entry_confirm_new_password.pack(pady=5)

        # Function to handle the "Update Password" button click
        def handle_update_password():
            new_password = entry_new_password.get()
            confirm_new_password = entry_confirm_new_password.get()

            if new_password == confirm_new_password:
                # Update the account password
                update_result = updateAccountPassword(userId, new_password)
                if update_result[0]:
                    messagebox.showinfo("Success", "Password updated successfully!")
                    # Clear the parent frame and show the dashboard
                    for widget in parent.winfo_children():
                        widget.destroy()
                    from dashboard import dashboard_overview
                    dashboard_overview(parent, userId, userEmail)
                else:
                    messagebox.showerror("Error", update_result[1])
            else:
                messagebox.showerror("Error", "New passwords do not match.")

        # Update Password Button
        update_password_button = ctk.CTkButton(parent, text="Update Password", width=120, fg_color="#4CAF50", hover_color="#45a049",
                                               command=handle_update_password)
        update_password_button.pack(pady=10)

    # Next Button (for current password verification)
    next_button = ctk.CTkButton(parent, text="Next", width=120, fg_color="#4CAF50", hover_color="#45a049",
                                command=handle_next)
    next_button.pack(pady=10)