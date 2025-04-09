import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import subprocess
import customtkinter as ctk
from tkinter import messagebox

from passwordList import password_List_OverviewBox  
from passwordOperations import addPasswordBox , passwordGeneratorBox
from dashboardOperations import dashboard_overview
   
# Function to show Dashboard
def open_dashboard(userId: int, userEmail: str):

    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("blue")  

    dashboard_window = ctk.CTk()
    dashboard_window.geometry("1000x500+300+50")
    dashboard_window.title("Dashboard")
    dashboard_window.resizable(False, False)

    # Sidebar
    sidebar = ctk.CTkFrame(dashboard_window, width=250, fg_color="#2C3E50")
    sidebar.pack(side="left", fill="y", padx=5, pady=5)
    sidebar.pack_propagate(False)  # Prevents shrinking

    # Content Frame
    content_frame = ctk.CTkFrame(dashboard_window, fg_color="white")
    content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    # Function to overview
    def dashboardOverview():
        close_dropdown()
        for widget in content_frame.winfo_children():
            widget.destroy()
        dashboard_overview(content_frame , userId , userEmail)
    
    # Function to load password generator             
    def dashboard_password_generator(): 
        close_dropdown(); 
        passwordGeneratorBox(content_frame)

    
    # Function to load password adding form
    def password_add():
        close_dropdown()
        for widget in content_frame.winfo_children():
            widget.destroy()
        addPasswordBox(content_frame, userId, userEmail)

    
    # Function to load the password List
    def password_list():
        close_dropdown()
        for widget in content_frame.winfo_children():
            widget.destroy()
        password_List_OverviewBox(content_frame, userId, userEmail)

    
    # Function to load profile editing form
    def profile_edit(): 
        from profileOperations import editProfileBox
        close_dropdown(); 
        for widget in content_frame.winfo_children():
            widget.destroy()
            
        editProfileBox(content_frame , userId , userEmail)
    
    
    # Function to Load Update Account Password From Profile
    def updateAccountPasswordOverview():
        from profileOperations import changeAccountPasswordBox
        close_dropdown(); 
        for widget in content_frame.winfo_children():
            widget.destroy()
        changeAccountPasswordBox(content_frame , userId , userEmail)
    
    # Function to load account password update
    def deleteAccount(): 
        from dashboardOperations import deleteAccountBox
        close_dropdown(); 
        for widget in content_frame.winfo_children():
            widget.destroy()
        deleteAccountBox(content_frame , userId , userEmail)
        
    
    # Dictionary to track open dropdowns
    open_dropdowns = {}

    
    # Function to close all dropdowns
    def close_dropdown():
        for dropdown in open_dropdowns.values():
            if dropdown and dropdown.winfo_exists():
                dropdown.destroy()
        open_dropdowns.clear()

    
    # Function to create dropdown directly below the button
    def show_dropdown(parent, button, options, functions):
        # Close all dropdowns first
        close_dropdown()

        # Create a new dropdown frame
        dropdown_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=5 , width=160)
        dropdown_frame.place(x=button.winfo_x()-10, y=button.winfo_y())
        
        open_dropdowns[button] = dropdown_frame  # Store the dropdown reference

        selected_option = ctk.StringVar(value="")  # No default selection

        for i, option in enumerate(options):
            radio = ctk.CTkRadioButton(dropdown_frame, text=option, variable=selected_option, value=option,
                                       command=lambda func=functions[i]: (func(), close_dropdown()))
            radio.pack(anchor="w", padx=8, pady=2)
               
    
    # Function to Logout User
    def logoutUser():
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to proceed?")
        if confirm:
            dashboard_window.after_cancel(dashboard_window)
            dashboard_window.destroy()
            subprocess.Popen(["python", "frontend/login.py"])  
    
    
    # Label On Sidebar
    sidebar_label = ctk.CTkLabel(sidebar , text="Contents" , text_color="red" , font=('Arial' , 20))
    sidebar_label.pack(pady=20)

    # Sidebar Buttons with Dropdowns
    btn_dashboard = ctk.CTkButton(sidebar, text="Dashboard", width=150, 
                                  command=lambda: show_dropdown(sidebar, btn_dashboard, 
                                                                ["Overview" , "Password Generator"], 
                                                                [ dashboardOverview , dashboard_password_generator]))
    btn_dashboard.pack(pady=20, padx=10)

    btn_add_password = ctk.CTkButton(sidebar, text="Password Entries", width=150, 
                                     command=lambda: show_dropdown(sidebar, btn_add_password, 
                                                                   ["Add Password", "Password List"], 
                                                                   [password_add, password_list]))
    btn_add_password.pack(pady=20, padx=10)

    btn_profile_settings = ctk.CTkButton(sidebar, text="Profile Settings", width=150, 
                                        command=lambda: show_dropdown(sidebar, btn_profile_settings, 
                                                                       ["Edit Profile", "Update Account Password" , "Delete Account"], 
                                                                       [profile_edit, updateAccountPasswordOverview , deleteAccount]))
    btn_profile_settings.pack(pady=20, padx=10)
    
    btn_logout = ctk.CTkButton(sidebar, text="Logout", fg_color="red"  , hover_color="green" , width=150, command=logoutUser)
    btn_logout.pack(pady=20, padx=10)

    dashboard_overview(content_frame , userId , userEmail)
    dashboard_window.mainloop()


if __name__ == "__main__":
    open_dashboard(3, "lance@gmail.com")