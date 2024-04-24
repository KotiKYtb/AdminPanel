# Import of all using library
import customtkinter as ctk
import tkinter as tk
import csv
import re
from PIL import Image

# Import all using external file/function
from Function.SRC.Account_System.register_verif import register_user_ext
from Function.SRC.Account_System.login_verif import login_user, verif_auto_login_or_not
from Function.SRC.Account_System.user_data import get_user_data
from Function.SRC.CSV.many_csv_function import clear_csv, csv_is_empty_or_full, search_auto_login_in_csv, return_list_of_data
from Function.SRC.Functionality.Get_Cam.get_cam_to_target import DisplayClient
from Function.System.get_target_ip import get_target_ip
from Function.SRC.Functionality.Mail_System.sending_mail import send_mail
from Function.SRC.Account_System.verif_new_user import verif_code_mail
from Function.SRC.Functionality.DDOS.ddos import fn_ddos
from Function.SRC.Account_System.update_user_information import update_user_info

# Main class with all properties of the App
class AdminPanelApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("1000x600")
        self.window.resizable(width=False, height=False)
        self.window.title("☠️ Admin Panel ☠️")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        font_family = ctk.CTkFont(family="customFont.ttf", size=30)

        # Register
        self.lastname_entry = None
        self.firstname_entry = None
        self.pseudo_entry = None
        self.email_entry = None
        self.phonenumber_entry = None
        self.password_entry = None
        self.confirmpassword_entry = None

        self.register_frame = ctk.CTkFrame(self.window, border_width=1, width=400, height=500)
        self.title_register_frame = ctk.CTkLabel(self.register_frame, text="REGISTER", font=font_family)

        self.lastame_txt = ctk.CTkLabel(self.register_frame, text="Lastname")
        self.lastname_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Enter your lastname...")
        self.firstname_txt = ctk.CTkLabel(self.register_frame, text="Firstname")
        self.firstname_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Enter your firstname...")
        self.pseudo_txt = ctk.CTkLabel(self.register_frame, text="Pseudo")
        self.pseudo_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Enter your pseudo...")
        self.email_txt = ctk.CTkLabel(self.register_frame, text="Email")
        self.email_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Enter your email...")
        self.phonenumber_txt = ctk.CTkLabel(self.register_frame, text="Phone Number")
        self.phonenumber_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Enter your phone number...")
        self.password_txt = ctk.CTkLabel(self.register_frame, text="Password")
        self.password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Enter your password...", show="*")
        self.confirmpassword_txt = ctk.CTkLabel(self.register_frame, text="Confirm password")
        self.confirmpassword_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Confirm your password...", show="*")

        self.register_button = ctk.CTkButton(self.register_frame, text="Register", command=lambda: self.register_user, width=75)
        self.have_account_button = ctk.CTkButton(self.register_frame, text="I have already an account", command=self.show_login_frame, fg_color="#3d3d3d")

        # Login
        self.login_frame = ctk.CTkFrame(self.window, border_width=1, width=400, height=300)

        self.title_login_frame = ctk.CTkLabel(self.login_frame, text="LOGIN", font=font_family)

        self.login_pseudo_txt = ctk.CTkLabel(self.login_frame, text="Pseudo")
        self.login_pseudo_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter your pseudo...")
        self.login_password_txt = ctk.CTkLabel(self.login_frame, text="Password")
        self.login_password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter your password...", show="*")

        self.auto_login_checkbox = ctk.CTkCheckBox(self.login_frame, text="Auto login", onvalue=1, offvalue=0)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.on_login_button_click, width=75)
        self.not_account_button = ctk.CTkButton(self.login_frame, text="I don't have an account", command=self.show_register_frame, fg_color="#3d3d3d")
        
        # Settings
        # Add function to save and load settings
        self.settings_frame = ctk.CTkFrame(self.window, border_width=1, width=400, height=425)

        self.settings_txt = ctk.CTkLabel(self.settings_frame, text="SETTINGS", font=font_family)

        # Switch for dark/light mode (Work !)
        self.switch_var = ctk.BooleanVar(value=True)
        self.switch_input_txt = ctk.CTkLabel(self.settings_frame, text=f"Switch to dark/light mode")
        self.switch_input = ctk.CTkSwitch(self.settings_frame, variable=self.switch_var, text=None)

        # Options for change language (Doesn't work !)
        self.different_language = ["French", "Spanish", "Chinese", "English", "German", "Italian", "Russian"]
        self.selected_language = ctk.StringVar(value=self.different_language[0])
        self.language_txt = ctk.CTkLabel(self.settings_frame, text="Language")
        self.language_option = ctk.CTkOptionMenu(self.settings_frame, values=self.different_language)

        self.panel_color_txt = ctk.CTkLabel(self.settings_frame, text="Panel Colors")
        
        self.bg_color_txt = ctk.CTkLabel(self.settings_frame, text="Background Color")
        
        self.text_color_txt = ctk.CTkLabel(self.settings_frame, text="Text Color")

        self.all_reset_settings = ["1000x600", "English", "add_panel_colors", "add_bg_colors", "add_text_colors"] # Doesn't work right now

        self.reset_default_button = ctk.CTkButton(self.settings_frame, text="Reset default", command=self.apply_settings, width=75) # Change to reset default
        self.apply_button = ctk.CTkButton(self.settings_frame, text="Apply", command=self.apply_settings, width=75) # You can press but not working

        # Main window
        self.main_window_frame = ctk.CTkFrame(self.window, border_width=1, width=1000, height=600, bg_color="transparent", fg_color="transparent")

        # Main verif new account
        self.window_verif_account_frame = ctk.CTkFrame(self.window, border_width=1, width=1000, height=600, bg_color="transparent", fg_color="transparent") 

        self.verif_account_box = ctk.CTkFrame(self.window_verif_account_frame, border_width=1, width=300, height=200, bg_color="transparent", fg_color="transparent")
        self.verif_account_label = ctk.CTkLabel(self.verif_account_box, text="Account Vérification", font=("Arial", 25))

        self.verif_code_label = ctk.CTkLabel(self.verif_account_box, text="Verification code")
        self.verif_code_input = ctk.CTkEntry(self.verif_account_box, placeholder_text="Enter vérification code...")
        self.verif_code_button = ctk.CTkButton(self.verif_account_box, command=lambda: self.account_is_verified(), text="Verify", width=120, height=40, fg_color="#ffffff", text_color="#000000")

        # Main window Get Cam
        self.main_window_frame_get_cam = ctk.CTkFrame(self.window, border_width=1, width=1000, height=600, bg_color="transparent", fg_color="transparent")

        self.get_cam_frame = ctk.CTkFrame(self.main_window_frame_get_cam, border_width=1, width=825, height=475, bg_color="transparent", fg_color="transparent")
        self.cam_frame = ctk.CTkFrame(self.get_cam_frame, border_width=1, width=660, height=475, bg_color="transparent", fg_color="#3d3d3d")

        self.target_ip_loader = get_target_ip()
        self.selected_target_ip = ctk.StringVar(value=self.target_ip_loader[0])
        self.target_txt = ctk.CTkLabel(self.get_cam_frame, text="Target IP", font=("Arial", 25))
        self.target_ip_option = ctk.CTkOptionMenu(self.get_cam_frame, values=self.target_ip_loader, dynamic_resizing=False)

        self.ip_cam_frame = ctk.CTkImage(light_image=Image.open("Images/no_video_error.jpg"), dark_image=Image.open("Images/no_video_error.jpg"), size=(635, 450))
        self.ip_cam_frame_label = ctk.CTkLabel(self.cam_frame, image=self.ip_cam_frame, width=635, height=450, text=None)
        self.close_conn_button = ctk.CTkButton(self.get_cam_frame, command=display_client.release_resources, text="Close connection", width=120, height=40, fg_color="#ffffff", text_color="#000000")
        self.show_cam_button = ctk.CTkButton(self.get_cam_frame, command=lambda: display_client.start_display(self.ip_cam_frame_label, self.target_ip_option.get()), text="Show", width=120, height=40, fg_color="#ffffff", text_color="#000000")

        # Main window Send Mail
        self.main_window_frame_send_mail = ctk.CTkFrame(self.window, border_width=1, width=1000, height=600, bg_color="transparent", fg_color="transparent")

        self.mail_preview_box = ctk.CTkFrame(self.main_window_frame_send_mail, border_width=1, width=300, height=475, bg_color="transparent", fg_color="transparent")
        self.mail_settings_label = ctk.CTkLabel(self.main_window_frame_send_mail, text="Mail Settings", font=("Arial", 25))
        
        self.to_label = ctk.CTkLabel(self.main_window_frame_send_mail, text="To")
        self.to_input = ctk.CTkEntry(self.main_window_frame_send_mail, placeholder_text="Enter mail target...")
        self.templates_label = ctk.CTkLabel(self.main_window_frame_send_mail, text="Templates")
        self.templates_list_loader = ["esaip", "credit agricole", "bouygues"]
        self.templates_options = ctk.CTkOptionMenu(self.main_window_frame_send_mail, values=self.templates_list_loader, dynamic_resizing=False)
        
        self.send_mail_button = ctk.CTkButton(self.main_window_frame_send_mail, command=lambda: send_mail(self.to_input.get(), self.templates_options.get()), text="Send", width=120, height=40, fg_color="#ffffff", text_color="#000000")
        
        # DDoS window
        self.ddos_frame = ctk.CTkFrame(self.window, width=1000, height=600)

        self.ddos_box = ctk.CTkFrame(self.ddos_frame, border_width=1, width=300, height=475, bg_color="transparent", fg_color="transparent")
        self.ddos_title_label = ctk.CTkLabel(self.ddos_box, text="DDoS", font=("Arial", 25))
        self.target_ip_loader_ddos = get_target_ip()
        self.selected_target_ip_ddos = ctk.StringVar(value=self.target_ip_loader_ddos[0])
        self.target_txt_ddos = ctk.CTkLabel(self.ddos_box, text="Target IP", font=("Arial", 20))
        self.target_ip_option_ddos = ctk.CTkOptionMenu(self.ddos_box, values=self.target_ip_loader_ddos, dynamic_resizing=False)
        self.nb_of_packet_txt = ctk.CTkLabel(self.ddos_box, text="Number of packets")
        self.nb_of_packet_input = ctk.CTkEntry(self.ddos_box, placeholder_text="Enter number of packets...")

        self.ddos_target_button = ctk.CTkButton(self.ddos_box, command=lambda: fn_ddos(self.target_ip_option.get(), self.nb_of_packet_input.get()), text="DDoS Target ", width=120, height=40, fg_color="#ffffff", text_color="#000000")

        # Account Window
        self.account_frame = ctk.CTkFrame(self.window, width=1000, height=600)

        self.id_card_frame = ctk.CTkFrame(self.account_frame, width=480, height=330)
        self.id_card_img = ctk.CTkImage(light_image=Image.open('Images/Admin Panel ID Card.png'), dark_image=Image.open('Images/Admin Panel ID Card.png'), size=(480,330))
        self.id_card_img_label = ctk.CTkLabel(self.id_card_frame, text="", image=self.id_card_img)
        self.id_card_change_user_info_button = ctk.CTkButton(self.account_frame, command=self.show_change_user_info_frame, text="Change Informations", width=120, height=40, fg_color="#ffffff", text_color="#000000")

        # Change User Informations Window
        self.change_user_info_frame = ctk.CTkFrame(self.window, border_width=1, width=1000, height=600)

        self.title_change_user_info = ctk.CTkLabel(self.change_user_info_frame, text="CHANGE USER INFORMATIONS", font=font_family)

        self.change_user_lastname_txt = ctk.CTkLabel(self.change_user_info_frame, text="Lastname")
        self.change_user_lastname_entry = ctk.CTkEntry(self.change_user_info_frame, placeholder_text="")
        self.change_user_firstname_txt = ctk.CTkLabel(self.change_user_info_frame, text="Firstname")
        self.change_user_firstname_entry = ctk.CTkEntry(self.change_user_info_frame, placeholder_text="")
        self.change_user_pseudo_txt = ctk.CTkLabel(self.change_user_info_frame, text="Pseudo")
        self.change_user_pseudo_entry = ctk.CTkEntry(self.change_user_info_frame, placeholder_text="")
        self.change_user_email_txt = ctk.CTkLabel(self.change_user_info_frame, text="Email")
        self.change_user_email_entry = ctk.CTkEntry(self.change_user_info_frame, placeholder_text="")
        self.change_user_password_txt = ctk.CTkLabel(self.change_user_info_frame, text="Password")
        self.change_user_password_entry = ctk.CTkEntry(self.change_user_info_frame, placeholder_text="", show="*")

        self.validate_change_user_info = ctk.CTkButton(self.change_user_info_frame, text="Validate", command=lambda: update_user_info(self.change_user_lastname_entry.get(), self.change_user_firstname_entry.get(), self.change_user_pseudo_entry.get(), self.change_user_email_entry.get(), self.change_user_password_entry.get()), width=75)

        # Everytime button
        ctk.CTkButton(self.window, text="❌", width=30, height=30, fg_color="#ff0000", hover_color="#8c1f1f", command=self.disconnect_when_quit).place(rely=0.99, relx=0.96, anchor="sw")
        ctk.CTkButton(self.window, text="⚙️", width=30, height=30, fg_color="#59ad05", hover_color="#4a751e", command=self.show_settings_frame).place(rely=0.99, relx=0.92, anchor="sw")
        ctk.CTkButton(self.window, text="👤", width=30, height=30, fg_color="#008bff", hover_color="#0467b9", command=self.show_account_data_frame).place(rely=0.99, relx=0.88, anchor="sw")
        ctk.CTkButton(self.window, text="🔙", width=30, height=30, fg_color="#e6dc09", hover_color="#c1b80a", command=self.show_last_frame).place(rely=0.99, relx=0.84, anchor="sw")
        ctk.CTkButton(self.window, text="Menu", width=120, height=40, fg_color="#ffffff", text_color="#000000", command=self.show_main_window_frame).place(rely=0.01, relx=0.01, anchor="nw")
        ctk.CTkButton(self.window, text="Get Webcam", width=120, height=40, fg_color="#ffffff", text_color="#000000", command=self.show_get_cam_window_frame).place(rely=0.01, relx=0.14, anchor="nw")
        ctk.CTkButton(self.window, text="DDOS", width=120, height=40, fg_color="#ffffff", text_color="#000000", command=self.show_ddos_window_frame).place(rely=0.01, relx=0.27, anchor="nw")
        # ctk.CTkButton(self.window, text="KeyLogger", width=120, height=40, fg_color="#ffffff", text_color="#000000").place(rely=0.01, relx=0.4, anchor="nw")
        ctk.CTkButton(self.window, text="Send Mail", width=120, height=40, fg_color="#ffffff", text_color="#000000", command=self.show_send_mail_window_frame).place(rely=0.01, relx=0.4, anchor="nw")


        # Initial frame
        self.current_frame = None

        if verif_auto_login_or_not():
            self.show_main_window_frame()
        else:
            file_path = "Data/in_use_account.csv"
            clear_csv(file_path)
            self.show_login_frame()

#################################### BACKEND ####################################
    
    # Save all settings
    def apply_settings(self):
        # Change Language
        # selected_language = self.selected_size.get()
        # Change Mode
        switch_value = self.switch_var.get()
        if switch_value:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        # Save to CSV
        self.settings_frame.place_forget()
        self.show_last_frame()

    # Reset all default settings
    def reset_settings(self):
        pass

    # Register function (ID/Lastname/Firstname/Pseudo/Mail/Phone Number/Password)
    def register_user(self):
        lastname = self.lastname_entry.get()
        firstname = self.firstname_entry.get()
        pseudo = self.pseudo_entry.get()
        email = self.email_entry.get()
        phonenumber = self.phonenumber_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirmpassword_entry.get()

        if register_user_ext(lastname, firstname, pseudo, email, phonenumber, password, confirm_password):
            self.lastname_entry.delete(0, ctk.END)
            self.firstname_entry.delete(0, ctk.END)
            self.pseudo_entry.delete(0, ctk.END)
            self.email_entry.delete(0, ctk.END)
            self.phonenumber_entry.delete(0, ctk.END)
            self.password_entry.delete(0, ctk.END)
            self.confirmpassword_entry.delete(0, ctk.END)
            self.show_verif_window_frame()

    # Login function (Pseudo/Password)
    def on_login_button_click(self):
        if login_user(self.login_pseudo_entry.get(), self.login_password_entry.get(), self.auto_login_checkbox.get()):
            self.show_main_window_frame()
        self.login_pseudo_entry.delete(0, ctk.END)
        self.login_password_entry.delete(0, ctk.END)

    # Disconnect when quit function
    def disconnect_when_quit(self):
        file_path = "Data/in_use_account.csv"
        if search_auto_login_in_csv(file_path):
            clear_csv(file_path)
        else:
            pass
        quit()

    def account_is_verified(self):
        if verif_code_mail(self.verif_code_input) == True:
            print("connecté")
            self.show_login_frame()
        else:
            print("Le code de vérification n'est pas bon")
        print(verif_code_mail(self.verif_code_input))

#################################### FRONTEND ####################################
        
    # Function for place object and frame
    def place_object(self, object, posx=None, posy=None, relposx=None, relposy=None, anchor_txt=None):
        object.place(x=posx, y=posy, relx=relposx, rely=relposy, anchor=f"{anchor_txt}")
        
    # All function to show wich frame user want
    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.place_forget()
        self.window.title(f"☠️ Admin Panel ☠️")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.last_frame = self.current_frame
        self.current_frame = frame

    def show_last_frame(self):
        file_path = "Data/in_use_account.csv"
        if not csv_is_empty_or_full(file_path):
            if self.last_frame == self.login_frame:
                pass
            else:
                if self.last_frame:
                    self.show_frame(self.last_frame)
        else:
            self.show_frame(self.last_frame)

    def show_register_frame(self):
        self.show_frame(self.register_frame)
        self.place_object(self.title_register_frame, posx=0, posy=50, relposx=0.5, relposy=0, anchor_txt="center")
        self.place_object(self.lastame_txt, posx=0, posy=120, relposx=0.20, relposy=0, anchor_txt="w")
        self.place_object(self.lastname_entry, posx=0, posy=120, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.firstname_txt, posx=0, posy=155, relposx=0.20, relposy=0, anchor_txt="w")
        self.place_object(self.firstname_entry, posx=0, posy=155, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.pseudo_txt, posx=0, posy=190, relposx=0.20, relposy=0, anchor_txt="w")
        self.place_object(self.pseudo_entry, posx=0, posy=190, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.email_txt, posx=0, posy=225, relposx=0.20, relposy=0, anchor_txt="w")
        self.place_object(self.email_entry, posx=0, posy=225, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.phonenumber_txt, posx=0, posy=260, relposx=0.20, relposy=0, anchor_txt="w")
        self.place_object(self.phonenumber_entry, posx=0, posy=260, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.password_txt, posx=0, posy=295, relposx=0.20, relposy=0, anchor_txt="w")
        self.place_object(self.password_entry, posx=0, posy=295, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.confirmpassword_txt, posx=0, posy=330, relposx=0.20, relposy=0, anchor_txt="w")
        self.place_object(self.confirmpassword_entry, posx=0, posy=330, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.register_button, posx=0, posy=425, relposx=0.5, relposy=0, anchor_txt="center")
        self.place_object(self.have_account_button, posx=0, posy=460, relposx=0.5, relposy=0, anchor_txt="center")

    def show_login_frame(self):
        self.show_frame(self.login_frame)
        self.place_object(self.title_login_frame, posx=0, posy=50, relposx=0.5, relposy=0, anchor_txt="center")
        self.place_object(self.login_pseudo_txt, posx=0, posy=125, relposx=0.2, relposy=0, anchor_txt="w")
        self.place_object(self.login_pseudo_entry, posx=0, posy=125, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.login_password_txt, posx=0, posy=160, relposx=0.2, relposy=0, anchor_txt="w")
        self.place_object(self.login_password_entry, posx=0, posy=160, relposx=0.52, relposy=0, anchor_txt="w")
        self.place_object(self.auto_login_checkbox, posx=0, posy=280, relposx=0.872, relposy=0, anchor_txt="center")
        self.place_object(self.login_button, posx=0, posy=215, relposx=0.5, relposy=0, anchor_txt="center")
        self.place_object(self.not_account_button, posx=0, posy=250, relposx=0.5, relposy=0, anchor_txt="center")

    def show_settings_frame(self):
        self.show_frame(self.settings_frame)
        self.place_object(self.settings_txt, posx=0, posy=50, relposx=0.5, relposy=0, anchor_txt="center")

        # A modifier les pos (+ vers le haut)
        self.place_object(self.switch_input_txt, posx=0, posy=155, relposx=0.2, relposy=0, anchor_txt="w")
        self.place_object(self.switch_input, posx=0, posy=155, relposx=0.6, relposy=0, anchor_txt="w")
        self.place_object(self.language_txt, posx=0, posy=190, relposx=0.2, relposy=0, anchor_txt="w")
        self.place_object(self.language_option, posx=0, posy=190, relposx=0.5, relposy=0, anchor_txt="w")
        self.place_object(self.panel_color_txt, posx=0, posy=225, relposx=0.2, relposy=0, anchor_txt="w")
        self.place_object(self.bg_color_txt, posx=0, posy=260, relposx=0.2, relposy=0, anchor_txt="w")
        self.place_object(self.text_color_txt, posx=0, posy=295, relposx=0.2, relposy=0, anchor_txt="w")
        self.place_object(self.reset_default_button, posx=0, posy=375, relposx=0.38, relposy=0, anchor_txt="center")
        self.place_object(self.apply_button, posx=0, posy=375, relposx=0.62, relposy=0, anchor_txt="center")

    def show_main_window_frame(self):
        self.show_frame(self.main_window_frame)

    def show_get_cam_window_frame(self):
        self.show_frame(self.main_window_frame_get_cam)

        # display cam
        self.place_object(self.get_cam_frame, posx=0, posy=0, relposx=0.5, relposy=0.5, anchor_txt="center")
        self.place_object(self.cam_frame, posx=0, posy=0, relposx=0, relposy=0, anchor_txt="nw")
        self.place_object(self.close_conn_button, posx=745, posy=390, relposx=0, relposy=0, anchor_txt="center")
        self.place_object(self.show_cam_button, posx=745, posy=440, relposx=0, relposy=0, anchor_txt="center")
        self.place_object(self.target_txt, posx=745, posy=30, relposx=0, relposy=0, anchor_txt="center")
        self.place_object(self.target_ip_option, posx=745, posy=65, relposx=0, relposy=0, anchor_txt="center")
        self.place_object(self.ip_cam_frame_label, posx=12.5, posy=12.5, relposx=0, relposy=0, anchor_txt="nw")

    def show_send_mail_window_frame(self):
        self.show_frame(self.main_window_frame_send_mail)
        # Onglet
        # Display mail system
        self.place_object(self.mail_preview_box, posx=0, posy=0, relposx=0.5, relposy=0.5, anchor_txt="center")
        self.place_object(self.send_mail_button, posx=0, posy=500, relposx=0.5, relposy=0, anchor_txt="center")
        self.place_object(self.mail_settings_label, posx=0, posy=100, relposx=0.5, relposy=0, anchor_txt="center")
        
        self.place_object(self.to_label, posx=0, posy=0, relposx=0.5, relposy=0.35, anchor_txt="center")
        self.place_object(self.to_input, posx=0, posy=0, relposx=0.5, relposy=0.4, anchor_txt="center")
        self.place_object(self.templates_label, posx=0, posy=0, relposx=0.5, relposy=0.5, anchor_txt="center")
        self.place_object(self.templates_options, posx=0, posy=0, relposx=0.5, relposy=0.55, anchor_txt="center")
    
    def show_verif_window_frame(self):
        self.show_frame(self.window_verif_account_frame)
        self.place_object(self.verif_account_box, posx=0, posy=0, relposx=0.5, relposy=0.5, anchor_txt="center")
        self.place_object(self.verif_account_label, posx=0, posy=0, relposx=0.5, relposy=0.15, anchor_txt="center")
        self.place_object(self.verif_code_label, posx=0, posy=0, relposx=0.5, relposy=0.40, anchor_txt="center")
        self.place_object(self.verif_code_input, posx=0, posy=0, relposx=0.5, relposy=0.55, anchor_txt="center")
        self.place_object(self.verif_code_button, posx=0, posy=0, relposx=0.5, relposy=0.85, anchor_txt="center")

    def show_ddos_window_frame(self):
        self.show_frame(self.ddos_frame)

        #Onglets

        self.place_object(self.ddos_box, posx=0, posy=0, relposx=0.5, relposy=0.5, anchor_txt="center")
        self.place_object(self.ddos_title_label, posx=0, posy=0, relposx=0.5, relposy=0.15, anchor_txt="center")
        self.place_object(self.target_txt_ddos, posx=0, posy=0, relposx=0.5, relposy=0.30, anchor_txt="center")
        self.place_object(self.target_ip_option_ddos, posx=0, posy=0, relposx=0.5, relposy=0.37, anchor_txt="center")
        self.place_object(self.nb_of_packet_txt, posx=0, posy=0, relposx=0.5, relposy=0.45, anchor_txt="center")
        self.place_object(self.nb_of_packet_input, posx=0, posy=0, relposx=0.5, relposy=0.52, anchor_txt="center")
        self.place_object(self.ddos_target_button, posx=0, posy=0, relposx=0.5, relposy=0.85, anchor_txt="center")

    def show_change_user_info_frame(self):
        self.show_frame(self.change_user_info_frame)
        self.place_object(self.title_change_user_info, posx=0, posy=0, relposx=0.5, relposy=0.15, anchor_txt="center")
        self.place_object(self.change_user_lastname_txt, posx=0, posy=0, relposx=0.40, relposy=0.3, anchor_txt="w")
        self.place_object(self.change_user_lastname_entry, posx=0, posy=0, relposx=0.5, relposy=0.3, anchor_txt="w")
        self.place_object(self.change_user_firstname_txt, posx=0, posy=0, relposx=0.40, relposy=0.37, anchor_txt="w")
        self.place_object(self.change_user_firstname_entry, posx=0, posy=0, relposx=0.5, relposy=0.37, anchor_txt="w")
        self.place_object(self.change_user_pseudo_txt, posx=0, posy=0, relposx=0.40, relposy=0.44, anchor_txt="w")
        self.place_object(self.change_user_pseudo_entry, posx=0, posy=0, relposx=0.5, relposy=0.44, anchor_txt="w")
        self.place_object(self.change_user_email_txt, posx=0, posy=0, relposx=0.40, relposy=0.51, anchor_txt="w")
        self.place_object(self.change_user_email_entry, posx=0, posy=0, relposx=0.5, relposy=0.51, anchor_txt="w")
        self.place_object(self.change_user_password_txt, posx=0, posy=0, relposx=0.40, relposy=0.58, anchor_txt="w")
        self.place_object(self.change_user_password_entry, posx=0, posy=0, relposx=0.5, relposy=0.58, anchor_txt="w")

        self.place_object(self.validate_change_user_info, posx=0, posy=0, relposx=0.5, relposy=0.9, anchor_txt="center")
        

    def show_account_data_frame(self):
        file_path = "Data/in_use_account.csv"
        self.show_frame(self.account_frame)
        if csv_is_empty_or_full(file_path):
            display_error(self.account_frame, "You need to be login to see your account informations", 0.5, 0.5, "center")
        else:
            self.id_card_frame.place(rely=0.5, relx=0.5, anchor="center")
            user_data = get_user_data()
            self.id_card_img_label.place(rely=0.5, relx=0.5, anchor="center")
            self.account_txt = ctk.CTkLabel(self.id_card_frame, text="Account Informations", bg_color="#3c3cd1").place(y=25, relx=0.5, anchor="center")
            self.lastname_txt = ctk.CTkLabel(self.id_card_frame, text=f"Lastname : {user_data[1]}", bg_color="#f8f8f6", text_color="#000000").place(y=75, relx=0.47, anchor="w")
            self.firstname_txt = ctk.CTkLabel(self.id_card_frame, text=f"Firstname : {user_data[2]}", bg_color="#f8f8f6", text_color="#000000").place(y=110, relx=0.47, anchor="w")
            self.pseudo_txt = ctk.CTkLabel(self.id_card_frame, text=f"Pseudo : {user_data[3]}", bg_color="#f8f8f6", text_color="#000000").place(y=145, relx=0.47, anchor="w")
            self.email_txt = ctk.CTkLabel(self.id_card_frame, text=f"Email : {user_data[4]}", bg_color="#f8f8f6", text_color="#000000").place(y=180, relx=0.47, anchor="w")
            self.phone_txt = ctk.CTkLabel(self.id_card_frame, text=f"Phone Number : {user_data[5]}", bg_color="#f8f8f6", text_color="#000000").place(y=215, relx=0.47, anchor="w")
            self.place_object(self.id_card_change_user_info_button, posx=0, posy=0, relposx=0.5, relposy=0.9, anchor_txt="center")

    # Function to run app
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    display_client = DisplayClient()
    app = AdminPanelApp()
    app.run()