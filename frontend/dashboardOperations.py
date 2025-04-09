import customtkinter as ctk
import subprocess
from tkinter import messagebox
from dbConfig.userFunctions import deleteUser
from backend.auth import deleteAccountUserFunc, verifyAccountDeleteOTP


# Function to show previous Login Details
def show_security_table(parent, security_data):
    """Displays security details in a table format."""
    from tkinter import ttk  # Import ttk for tables

    # Create Treeview Table
    table = ttk.Treeview(parent, columns=("SrNo", "login_time", "ip_address", "device_info"), show="headings")
    
    # Define column headings
    table.heading("SrNo", text="Sr.No")
    table.heading("login_time", text="Last Login Time")
    table.heading("ip_address", text="IP Address")
    table.heading("device_info", text="Device Info")

    # Set column widths
    table.column("SrNo", width=50, anchor="center")
    table.column("login_time", width=150, anchor="center")
    table.column("ip_address", width=120, anchor="center")
    table.column("device_info", width=200, anchor="center")

    # Insert data into the table with an index
    for idx, row in enumerate(security_data, start=1):
        table.insert("", "end", values=(
            idx, 
            row["login_time"], 
            row["ip_address"], 
            row["device_info"]
        ))

    # Pack the table into the parent frame
    table.pack(fill="both", expand=True, padx=10, pady=10)
    
    

# Functions for dashboard starting
def dashboard_overview(parent, userId : int , userEmail : str):
    from dbConfig.userFunctions import fetchSecurityDetails  

    # Create frame for dashboard content
    dashboard_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
    dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Welcome Label
    welcome_label = ctk.CTkLabel(dashboard_frame, text=f"Welcome, {userEmail}", 
                                font=("Arial", 18, "bold"), text_color="#1E90FF")
    welcome_label.pack(anchor="w", padx=10, pady=10)

    # Fetch security details
    result , security_data = fetchSecurityDetails(userId, userEmail)

    if result and security_data:
        security_table_frame = ctk.CTkFrame(dashboard_frame, fg_color="white")
        security_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        show_security_table(security_table_frame, security_data)  # Table function
    else:
        ctk.CTkLabel(dashboard_frame, text="No security details found.", 
                    font=("Arial", 14), text_color="gray").pack(pady=10)

    
    
# Functions for dashboard Delete Account Option
def deleteAccountBox(parent, userId, userEmail):
    """
    Displays a form to delete the user account after confirmation and OTP verification.
    """
    # Confirmation dialog
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the account?")
    if not confirm:
        return  # Exit if the user cancels

    # Clear the parent frame before adding new widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Main container frame
    deleteAccount_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
    deleteAccount_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Heading Label
    textbox = ctk.CTkTextbox(deleteAccount_frame, width=400, height=40, font=("Arial", 18, "bold"), wrap="word")
    textbox.pack()
    textbox.insert("1.0", "Enter ")
    textbox.insert("end", "'Delete Account'", "red")  # 'Delete Account' in red
    textbox.insert("end", " to proceed")
    textbox.tag_config("red", foreground="red")
    textbox.configure(state="disabled")

    # Input Box for "Delete Account"
    entry_delete_text = ctk.CTkEntry(deleteAccount_frame, placeholder_text="Type 'Delete Account'", 
                                     width=300, height=40)
    entry_delete_text.pack(pady=10)

    # Function to handle the "Proceed" button click
    def handle_proceed():
        entered_text = entry_delete_text.get().strip()
        if entered_text != "Delete Account":
            messagebox.showerror("Error", "Please type 'Delete Account' exactly to proceed.")
            return
        btn_proceed.configure(state="disabled")
        # Send OTP to the user's email
        success, message = deleteAccountUserFunc(userEmail)
        if not success:
            messagebox.showerror("Error", message)
            btn_proceed.configure(state="normal")
            return

        # Open OTP verification window
        openOTPWindow(parent, userId, userEmail)

    # Proceed Button
    btn_proceed = ctk.CTkButton(deleteAccount_frame, text="Proceed", command=handle_proceed, 
                                width=120, height=40, fg_color="#4CAF50", hover_color="#45a049")
    btn_proceed.pack(pady=10)

# Function to open OTP verification window
def openOTPWindow(parent, userId, userEmail):
    """
    Opens a window for the user to enter the OTP for account deletion.
    """
    def verifyOTP():
        otp = entry_otp.get()
        if not otp:
            messagebox.showerror("Error", "OTP is required")
            return

        # Verify the OTP
        success, message = verifyAccountDeleteOTP(userEmail, otp)
        if not success:
            messagebox.showerror("Error", message)
            return

        # OTP verified, delete the user
        success, message = deleteUser(userId)
        if success:
            messagebox.showinfo("Success", "Account deleted successfully!")
            root_window = parent.master  # Assuming parent is a frame inside the main window
            while root_window.master:
                root_window = root_window.master  # Keep going up to the main root window
            
            root_window.destroy()  # Close the main application window
            subprocess.Popen(["python", "frontend/register.py"])  
            
        else:
            messagebox.showerror("Error", message)

    otp_window = ctk.CTkToplevel(parent)
    otp_window.geometry("300x200+250+150")
    otp_window.title("Verify OTP")
    otp_window.resizable(False, False)

    # OTP Label
    ctk.CTkLabel(otp_window, text=f"Enter OTP sent to {userEmail}", font=("Arial", 14)).pack(pady=10)

    # OTP Entry
    entry_otp = ctk.CTkEntry(otp_window, placeholder_text="OTP", width=200, height=40)
    entry_otp.pack(pady=10)

    # Verify OTP Button
    btn_verify = ctk.CTkButton(otp_window, text="Verify", command=verifyOTP, width=200, height=40)
    btn_verify.pack(pady=10)