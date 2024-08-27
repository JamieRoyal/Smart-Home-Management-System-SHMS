import os
import sqlite3
import time
import tkinter as tk

import bcrypt
import customtkinter
from CTkMessagebox import CTkMessagebox
from PIL import ImageTk, Image

import LoginCheck as lc
from RegValCheck import val_check
from tapo_l530 import *

isLoginApp = False
isMainApp = True
isLoginSetup = True
isRegSetup = False
isTopWindowOpen = False
isButtonsDisabled = False
isDeviceSlotsEmpty = True
isScheduleSlotsEmpty = True
isPower = False
user = ""
time1 = ''
device_type = ""
btn_col = '#2b2b2b'
NumOfDevices = 0
devices = []


class LoginApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("S.H.M.S - Smart Home Management System")
        self.geometry('800x480')

        # show/hide icons
        self.show_icon = ImageTk.PhotoImage(file='images\\password_icon_show.png')
        self.hide_icon = ImageTk.PhotoImage(file='images\\password_icon_hide.png')

        # create login gui
        self.login_frame = customtkinter.CTkFrame(self)

        # main title
        self.login_title = customtkinter.CTkLabel(self.login_frame,
                                                  text='Login',
                                                  text_color="#317BCD",
                                                  font=('Bold', 46))
        self.login_title.configure(justify=tk.CENTER)
        self.login_title.place(x=335, y=40)

        # username label
        self.username_label = customtkinter.CTkLabel(self.login_frame,
                                                     text='Username',
                                                     font=('Bold', 20))
        self.username_label.place(x=249, y=120)

        # username entry
        self.username_entry = customtkinter.CTkEntry(self.login_frame,
                                                     font=('Bold', 20),
                                                     width=300)
        self.username_entry.place(x=249, y=166)

        # password label
        self.password_label = customtkinter.CTkLabel(self.login_frame,
                                                     text='Password',
                                                     font=('Bold', 20))
        self.password_label.place(x=249, y=218)

        # password entry
        self.password_entry = customtkinter.CTkEntry(self.login_frame,
                                                     font=('Bold', 20),
                                                     width=300,
                                                     show='*')
        self.password_entry.place(x=249, y=264)

        # password toggle feature
        self.toggle_hide_btn = customtkinter.CTkButton(self.login_frame,
                                                       image=self.hide_icon,
                                                       text='',
                                                       width=30,
                                                       height=30,
                                                       fg_color='#343638',
                                                       border_color='#565b5e',
                                                       hover=False,
                                                       command=self.show_toggle)
        self.toggle_hide_btn.place(x=555, y=264)

        # login button
        self.login_button = customtkinter.CTkButton(self.login_frame,
                                                    text='Login',
                                                    font=('Bold', 20),
                                                    command=self.account_check)
        self.login_button.place(x=329, y=324)

        # options dropbox
        self.combobox_options = customtkinter.CTkComboBox(self.login_frame,
                                                          width=85,
                                                          values=["Login", "Register", "Close"],
                                                          command=self.combobox_options)
        self.combobox_options.place(x=10, y=10)

        self.login_frame.pack(pady=5, padx=5)
        self.login_frame.pack_propagate(False)
        self.login_frame.configure(width=800, height=480)

    # def for LoginApp
    def reg_setup(self):
        global isLoginSetup
        global isRegSetup
        print("Setting Up Register Page")
        isLoginSetup = False
        isRegSetup = True
        self.login_title.configure(text="Register")
        self.login_title.place(x=310, y=40)
        self.login_button.configure(text="Register")
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def log_setup(self):
        global isLoginSetup
        global isRegSetup
        print("Setting Up Login Page")
        isLoginSetup = True
        isRegSetup = False
        self.login_title.configure(text="Login")
        self.login_title.place(x=355, y=40)
        self.login_button.configure(text="Login")
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def show_toggle(self):
        self.toggle_hide_btn.configure(self.login_frame,
                                       image=self.show_icon,
                                       text='',
                                       command=self.hide_toggle,
                                       width=30,
                                       height=30,
                                       fg_color='#343638',
                                       border_color='#565b5e',
                                       border_width=2,
                                       hover=False)
        self.toggle_hide_btn.place(x=555, y=264)
        self.password_entry.configure(show='')

    def hide_toggle(self):
        self.toggle_hide_btn.configure(self.login_frame,
                                       image=self.hide_icon,
                                       text='',
                                       command=self.show_toggle,
                                       width=30,
                                       height=30,
                                       fg_color='#343638',
                                       border_color='#565b5e',
                                       border_width=2,
                                       hover=False)
        self.toggle_hide_btn.place(x=555, y=264)
        self.password_entry.configure(show='*')

    def account_check(self):
        global isLoginApp
        global isMainApp
        global user
        if isLoginSetup:
            print("LoginCheck")
            if lc.login_check(self.username_entry.get(), self.password_entry.get()):
                print("Account Check: Succeeded")
                isLoginApp = False
                isMainApp = True
                user = self.username_entry.get()
                self.destroy()
                main()
            else:
                print("Account Check: Failed")
                return
        elif isRegSetup:
            if val_check(self.username_entry.get(), self.password_entry.get()):
                print("Registration Succeeded")
            else:
                print("Registration: Failed")

    def combobox_options(self, choice):
        print(f"combobox dropbox clicked: {choice}")
        if choice == "Login":
            self.log_setup()
        elif choice == "Register":
            self.reg_setup()
        elif choice == "Close":
            exit()


class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("S.H.M.S - Smart Home Management System")
        self.geometry('800x480')
        self.resizable(False, False)

        # text for credits on every page
        self.credits_text = "Credits: Jamie A Bestford, Bailey Westbury, " \
                            "Hussain Zaheer, Moses Harazi"

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # icon for logo (with and without text)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.shms_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(164, 69))
        self.shms_wt_logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_with_text.png")),
                                                   size=(200, 200))

        # icons for sidebar
        self.device_icon = ImageTk.PhotoImage(file="images\\devices_button_icon.png")
        self.schedules_icon = ImageTk.PhotoImage(file="images\\schedule_button_icon.png")
        self.camera_icon = ImageTk.PhotoImage(file="images\\camera_button_icon.png")
        self.temperature_icon = ImageTk.PhotoImage(file="images\\temperature_button_icon.png")
        self.settings_icon = ImageTk.PhotoImage(file="images\\settings_button_icon.png")
        self.logout_icon = ImageTk.PhotoImage(file="images\\logout_button_icon.png")

        # icons for device and schedule slots
        self.empty_slot = customtkinter.CTkImage(Image.open(os.path.join(image_path, "empty_slot.png")),
                                                 size=(175, 175))
        self.light_slot = customtkinter.CTkImage(Image.open(os.path.join(image_path, "light_slot.png")),
                                                 size=(175, 175))
        self.unknown_slot = customtkinter.CTkImage(Image.open(os.path.join(image_path, "unknown_slot.png")),
                                                   size=(175, 175))

        # create sidebar
        self.sidebar = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        self.sidebar_label = customtkinter.CTkLabel(self.sidebar, text="", image=self.shms_logo,
                                                    compound="left",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=20)

        self.device_button = customtkinter.CTkButton(self.sidebar, corner_radius=0, height=40, border_spacing=10,
                                                     text="Device", image=self.device_icon,
                                                     fg_color="transparent", text_color=("gray10", "gray90"),
                                                     hover_color=("gray70", "gray30"),
                                                     anchor="w", command=self.device_button_event)
        self.device_button.grid(row=1, column=0, sticky="ew")

        self.schedules_button = customtkinter.CTkButton(self.sidebar, corner_radius=0, height=40, border_spacing=10,
                                                        text="Schedule", image=self.schedules_icon,
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        anchor="w", command=self.schedules_button_event)
        self.schedules_button.grid(row=2, column=0, sticky="ew")

        # self.camera_button = customtkinter.CTkButton(self.sidebar, corner_radius=0, height=40, border_spacing=10,
        #                                             text="Camera", image=self.camera_icon,
        #                                             fg_color="transparent", text_color=("gray10", "gray90"),
        #                                             hover_color=("gray70", "gray30"),
        #                                             anchor="w", command=self.camera_button_event)
        # self.camera_button.grid(row=3, column=0, sticky="ew")

        self.temperature_button = customtkinter.CTkButton(self.sidebar, corner_radius=0, height=40,
                                                          border_spacing=10,
                                                          text="Temperature", image=self.temperature_icon,
                                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                                          hover_color=("gray70", "gray30"),
                                                          anchor="w", command=self.temperature_button_event)
        self.temperature_button.grid(row=3, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.sidebar, corner_radius=0, height=40, border_spacing=10,
                                                       text="Settings", image=self.settings_icon,
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=4, column=0, sticky="ew")

        self.logout_button = customtkinter.CTkButton(self.sidebar, corner_radius=0, height=40, border_spacing=10,
                                                     text="Logout", image=self.logout_icon,
                                                     fg_color="transparent", text_color=("gray10", "gray90"),
                                                     hover_color=("gray70", "gray30"),
                                                     anchor="w", command=self.logout_button_event)
        self.logout_button.grid(row=5, column=0, sticky="ew")

        self.clock = customtkinter.CTkLabel(self.sidebar, font=('', 20), fg_color="transparent")
        self.clock.place(x=10, y=445)
        self.tick()

        # create welcome frame
        self.welcome_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.welcome_frame.grid_columnconfigure(0, weight=1)

        self.welcome_frame_large_image_label = customtkinter.CTkLabel(self.welcome_frame, image=self.shms_wt_logo,
                                                                      text="")
        self.welcome_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.welcome_frame_text_1 = customtkinter.CTkLabel(self.welcome_frame, text=f"Welcome {user}! \n\n"
                                                                                    "To get started, "
                                                                                    "click onto another page",
                                                           font=(customtkinter.CTkFont, 18))
        self.welcome_frame_text_1.grid(row=1, column=0, padx=20, pady=20)

        self.credits = customtkinter.CTkLabel(self.welcome_frame,
                                              text=self.credits_text,
                                              font=('Bold', 10))  # Creator Credits for the end of the page
        self.credits.place(x=125, y=450)

        # create device frame
        self.device_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.device_frame.grid_columnconfigure(0, weight=1)

        self.connect_device_button = customtkinter.CTkButton(self.device_frame, text="+",
                                                             fg_color=btn_col, width=45, height=25,
                                                             command=self.connect_new_device_event)
        self.connect_device_button.place(x=540, y=10)

        # Device Slots
        self.device_slot_1 = customtkinter.CTkButton(self.device_frame, text="", image=self.empty_slot,
                                                     fg_color="transparent", hover=False)
        self.device_slot_1.place(x=10, y=50)
        self.device_slot_1_label = customtkinter.CTkLabel(self.device_frame, text="", width=175, bg_color="#2b2b2b")
        self.device_slot_1_label.place(x=18, y=195)

        self.device_slot_2 = customtkinter.CTkButton(self.device_frame, text="", image=self.empty_slot,
                                                     fg_color="transparent", hover=False)
        self.device_slot_2.place(x=200, y=50)
        self.device_slot_2_label = customtkinter.CTkLabel(self.device_frame, text="", width=175, bg_color="#2b2b2b")
        self.device_slot_2_label.place(x=208, y=195)

        self.device_slot_3 = customtkinter.CTkButton(self.device_frame, text="", image=self.empty_slot,
                                                     fg_color="transparent", hover=False)
        self.device_slot_3.place(x=390, y=50)
        self.device_slot_3_label = customtkinter.CTkLabel(self.device_frame, text="", width=175, bg_color="#2b2b2b")
        self.device_slot_3_label.place(x=398, y=195)

        self.device_slot_4 = customtkinter.CTkButton(self.device_frame, text="", image=self.empty_slot,
                                                     fg_color="transparent", hover=False)
        self.device_slot_4.place(x=10, y=240)
        self.device_slot_4_label = customtkinter.CTkLabel(self.device_frame, text="", width=175, bg_color="#2b2b2b")
        self.device_slot_4_label.place(x=18, y=385)

        self.device_slot_5 = customtkinter.CTkButton(self.device_frame, text="", image=self.empty_slot,
                                                     fg_color="transparent", hover=False)
        self.device_slot_5.place(x=200, y=240)
        self.device_slot_5_label = customtkinter.CTkLabel(self.device_frame, text="", width=175, bg_color="#2b2b2b")
        self.device_slot_5_label.place(x=208, y=385)

        self.device_slot_6 = customtkinter.CTkButton(self.device_frame, text="", image=self.empty_slot,
                                                     fg_color="transparent", hover=False)
        self.device_slot_6.place(x=390, y=240)
        self.device_slot_6_label = customtkinter.CTkLabel(self.device_frame, text="", width=175, bg_color="#2b2b2b")
        self.device_slot_6_label.place(x=398, y=385)

        # Shows if there is no connected Devices
        self.ifNoDevices_label = customtkinter.CTkLabel(self.device_frame,
                                                        text="Press the '+' button to connect your first device",
                                                        font=('Bold', 25))
        self.ifNoDevices_label.place(x=35, y=222)

        self.device_slot_check()

        self.credits = customtkinter.CTkLabel(self.device_frame,
                                              text=self.credits_text,
                                              font=('Bold', 10))  # Creator Credits for the end of the page
        self.credits.place(x=125, y=450)

        # create schedule frame
        self.schedule_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.connect_schedule_button = customtkinter.CTkButton(self.schedule_frame, text="+",
                                                               fg_color=btn_col, width=45, height=25,
                                                               command=self.schedule_event)
        self.connect_schedule_button.place(x=540, y=10)

        # Schedule Slots
        self.schedule_slot_1 = customtkinter.CTkButton(self.schedule_frame, text="", image=self.empty_slot,
                                                       fg_color="transparent", hover=False)
        self.schedule_slot_1.place(x=10, y=50)
        self.schedule_slot_1_label = customtkinter.CTkLabel(self.schedule_frame, text="", width=175, bg_color="#2b2b2b")
        self.schedule_slot_1_label.place(x=18, y=195)

        self.schedule_slot_2 = customtkinter.CTkButton(self.schedule_frame, text="", image=self.empty_slot,
                                                       fg_color="transparent", hover=False)
        self.schedule_slot_2.place(x=200, y=50)
        self.schedule_slot_2_label = customtkinter.CTkLabel(self.schedule_frame, text="", width=175, bg_color="#2b2b2b")
        self.schedule_slot_2_label.place(x=208, y=195)

        self.schedule_slot_3 = customtkinter.CTkButton(self.schedule_frame, text="", image=self.empty_slot,
                                                       fg_color="transparent", hover=False)
        self.schedule_slot_3.place(x=390, y=50)
        self.schedule_slot_3_label = customtkinter.CTkLabel(self.schedule_frame, text="", width=175, bg_color="#2b2b2b")
        self.schedule_slot_3_label.place(x=398, y=195)

        self.schedule_slot_4 = customtkinter.CTkButton(self.schedule_frame, text="", image=self.empty_slot,
                                                       fg_color="transparent", hover=False)
        self.schedule_slot_4.place(x=10, y=240)
        self.schedule_slot_4_label = customtkinter.CTkLabel(self.schedule_frame, text="", width=175, bg_color="#2b2b2b")
        self.schedule_slot_4_label.place(x=18, y=385)

        self.schedule_slot_5 = customtkinter.CTkButton(self.schedule_frame, text="", image=self.empty_slot,
                                                       fg_color="transparent", hover=False)
        self.schedule_slot_5.place(x=200, y=240)
        self.schedule_slot_5_label = customtkinter.CTkLabel(self.schedule_frame, text="", width=175, bg_color="#2b2b2b")
        self.schedule_slot_5_label.place(x=208, y=385)

        self.schedule_slot_6 = customtkinter.CTkButton(self.schedule_frame, text="", image=self.empty_slot,
                                                       fg_color="transparent", hover=False)
        self.schedule_slot_6.place(x=390, y=240)
        self.schedule_slot_6_label = customtkinter.CTkLabel(self.schedule_frame, text="", width=175, bg_color="#2b2b2b")
        self.schedule_slot_6_label.place(x=398, y=385)

        # Shows if there is no connected Devices
        self.ifNoSchedules_label = customtkinter.CTkLabel(self.schedule_frame,
                                                          text="Press the '+' button to create your first schedule",
                                                          font=('Bold', 25))
        self.ifNoSchedules_label.place(x=35, y=222)

        self.schedule_slot_check()

        self.credits = customtkinter.CTkLabel(self.schedule_frame,
                                              text=self.credits_text,
                                              font=('Bold', 10))  # Creator Credits for the end of the page
        self.credits.place(x=125, y=450)

        # create camera frame
        self.camera_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.credits = customtkinter.CTkLabel(self.camera_frame,
                                              text=self.credits_text,
                                              font=('Bold', 10))  # Creator Credits for the end of the page
        self.credits.place(x=125, y=450)
        # create temperature frame
        self.temperature_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.open_temperature_button = customtkinter.CTkButton(self.temperature_frame,
                                                               text="Click to Open Temperature GUI",
                                                               fg_color=btn_col, height=25,
                                                               command=self.temperature_event)
        self.open_temperature_button.pack(padx=5, pady=5)

        self.credits = customtkinter.CTkLabel(self.temperature_frame,
                                              text=self.credits_text,
                                              font=('Bold', 10))  # Creator Credits for the end of the page
        self.credits.place(x=125, y=450)

        # create settings frame
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.settings_device_main_label = customtkinter.CTkLabel(self.settings_frame,
                                                                 text="Device",
                                                                 font=('Bold', 18))
        self.settings_device_main_label.place(x=5, y=5)
        self.settings_device_name_label = customtkinter.CTkLabel(self.settings_frame,
                                                                 text="SHMS-3Q67JPL",
                                                                 font=('', 16),
                                                                 text_color='#999999')
        self.settings_device_name_label.place(x=5, y=30)

        self.settings_user_main_label = customtkinter.CTkLabel(self.settings_frame,
                                                               text="Account Username",
                                                               font=('', 18))
        self.settings_user_main_label.place(x=5, y=70)
        self.settings_username_label = customtkinter.CTkLabel(self.settings_frame,
                                                              text=user,
                                                              font=('', 16),
                                                              text_color='#999999')
        self.settings_username_label.place(x=5, y=95)

        self.settings_pass_main_label = customtkinter.CTkLabel(self.settings_frame,
                                                               text="Account Username",
                                                               font=('', 18))
        self.settings_pass_main_label.place(x=5, y=135)
        self.settings_password_label = customtkinter.CTkLabel(self.settings_frame,
                                                              text="********",
                                                              font=('', 16),
                                                              text_color='#999999')
        self.settings_password_label.place(x=5, y=160)
        self.change_pass_button = customtkinter.CTkButton(self.settings_frame, text="Change Password",
                                                          fg_color=btn_col, height=25,
                                                          command=self.change_password_event)
        self.change_pass_button.place(x=450, y=160)

        self.credits = customtkinter.CTkLabel(self.settings_frame,
                                              text=self.credits_text,
                                              font=('Bold', 10))  # Creator Credits for the end of the page
        self.credits.place(x=125, y=450)
        # create logout frame
        self.logout_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("welcome")

    # def for MainApp
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.device_button.configure(fg_color=("gray75", "gray25") if name == "device" else "transparent")
        self.schedules_button.configure(fg_color=("gray75", "gray25") if name == "schedules" else "transparent")
        # self.camera_button.configure(fg_color=("gray75", "gray25") if name == "camera" else "transparent")
        self.temperature_button.configure(fg_color=("gray75", "gray25") if name == "temperature" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        self.logout_button.configure(fg_color=("gray75", "gray25") if name == "logout" else "transparent")

        # show selected frame
        if name == "welcome":
            self.welcome_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.welcome_frame.grid_forget()
        if name == "device":
            self.device_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.device_frame.grid_forget()
        if name == "schedules":
            self.schedule_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.schedule_frame.grid_forget()
        if name == "camera":
            self.camera_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.camera_frame.grid_forget()
        if name == "temperature":
            self.temperature_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.temperature_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
        if name == "logout":
            self.logout_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.logout_frame.grid_forget()

    def device_button_event(self):
        self.select_frame_by_name("device")

    def schedules_button_event(self):
        self.select_frame_by_name("schedules")

    def camera_button_event(self):
        self.select_frame_by_name("camera")

    def temperature_button_event(self):
        self.select_frame_by_name("temperature")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def logout_button_event(self):
        global isMainApp
        global isLoginApp
        msg = CTkMessagebox(title="Logout?", message="Are you sure?", icon="question", option_1="Logout",
                            option_2="Cancel")
        if msg.get() == "Logout":
            isMainApp = False
            isLoginApp = True
            self.destroy()
            main()
        else:
            self.select_frame_by_name("welcome")

    def tick(self):
        global time1
        time2 = time.strftime('%H:%M')
        if time2 != time1:
            time1 = time2
            self.clock.configure(text=time2)
        self.clock.after(200, self.tick)

    def device_slot_check(self):
        global isDeviceSlotsEmpty
        if isDeviceSlotsEmpty:
            self.ifNoDevices_label.configure(text="Press the '+' button to connect your first device")
        if not isDeviceSlotsEmpty:
            self.ifNoDevices_label.configure(text="")
        self.ifNoDevices_label.after(200, self.device_check)
        self.ifNoDevices_label.after(200, self.device_slot_check)

    def schedule_slot_check(self):
        global isScheduleSlotsEmpty
        if isScheduleSlotsEmpty:
            self.ifNoSchedules_label.configure(text="Press the '+' button to create your first schedule")
        if not isScheduleSlotsEmpty:
            self.ifNoSchedules_label.configure(text="")
        self.ifNoSchedules_label.after(200, self.schedule_slot_check)

    def device_check(self):
        global isDeviceSlotsEmpty
        if isTopWindowOpen == False:
            try:
                conn = sqlite3.connect(f'{user}_devices.db')
                conn.execute(f"CREATE TABLE IF NOT EXISTS {user}_devices_info(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                             "device_name TEXT UNIQUE NOT NULL, "
                             "device_type TEXT NOT NULL, "
                             "ip TEXT, "
                             "account_name TEXT, "
                             "password TEXT)")
                cursor = conn.cursor()
                select_query = f"SELECT * from {user}_devices_info"
                cursor.execute(select_query)
                records = cursor.fetchall()
                for row in records:
                    id = row[0]
                    device_name = row[1]
                    device_type = row[2]

                    if id == 1:
                        isDeviceSlotsEmpty = False
                        self.device_slot_1_label.configure(text=device_name)
                        self.device_slot_1.configure(command=lambda: self.control_device_event(id))
                        if device_type == "Tapo L530":
                            self.device_slot_1.configure(image=self.light_slot)
                        else:
                            self.device_slot_1.configure(image=self.unknown_slot)
                    if id == 2:
                        isDeviceSlotsEmpty = False
                        self.device_slot_2_label.configure(text=device_name)
                        self.device_slot_2.configure(command=lambda: self.control_device_event(id))
                        if device_type == "Tapo L530":
                            self.device_slot_2.configure(image=self.light_slot)
                        else:
                            self.device_slot_2.configure(image=self.unknown_slot)
                    if id == 3:
                        isDeviceSlotsEmpty = False
                        self.device_slot_3_label.configure(text=device_name)
                        self.device_slot_3.configure(command=lambda: self.control_device_event(id))
                        if device_type == "Tapo L530":
                            self.device_slot_3.configure(image=self.light_slot)
                        else:
                            self.device_slot_3.configure(image=self.unknown_slot)
                    if id == 4:
                        isDeviceSlotsEmpty = False
                        self.device_slot_4_label.configure(text=device_name)
                        self.device_slot_4.configure(command=lambda: self.control_device_event(id))
                        if device_type == "Tapo L530":
                            self.device_slot_4.configure(image=self.light_slot)
                        else:
                            self.device_slot_4.configure(image=self.unknown_slot)
                    if id == 5:
                        isDeviceSlotsEmpty = False
                        self.device_slot_5_label.configure(text=device_name)
                        self.device_slot_5.configure(command=lambda: self.control_device_event(id))
                        if device_type == "Tapo L530":
                            self.device_slot_5.configure(image=self.light_slot)
                        else:
                            self.device_slot_5.configure(image=self.unknown_slot)
                    if id == 6:
                        isDeviceSlotsEmpty = False
                        self.device_slot_6_label.configure(text=device_name)
                        self.device_slot_6.configure(command=lambda: self.control_device_event(id))
                        if device_type == "Tapo L530":
                            self.device_slot_6.configure(image=self.light_slot)
                        else:
                            self.device_slot_6.configure(image=self.unknown_slot)

            except sqlite3.Error as error:
                print("Failed to read data from table", error)
            finally:
                if conn:
                    conn.close()
        else:
            return

    def connect_new_device_event(self):
        cdw = ConnectDeviceWindow()
        cdw.mainloop()

    def control_device_event(self, identification):
        cdw = ControlDeviceWindow(identification)
        cdw.mainloop()

    def change_password_event(self):
        pcw = PasswordChangeWindow()
        pcw.mainloop()

    def schedule_event(self):
        sw = ScheduleWindow()
        sw.mainloop()

    def temperature_event(self):
        import hygrometergui


class ConnectDeviceWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        global isTopWindowOpen
        isTopWindowOpen = True

        self.conn = sqlite3.connect(f'{user}_devices.db')
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {user}_devices_info(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "device_num INTEGER NOT NULL, device_name TEXT NOT NULL, "
                          "device_type TEXT NOT NULL, ip TEXT, account_name TEXT, password TEXT)")
        cursor = self.conn.cursor()

        # Images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.details_background = customtkinter.CTkImage(Image.open(os.path.join(image_path, "empty_slot.png")),
                                                         size=(309, 280))

        # Creating Top Window
        self.app_width = 329
        self.app_height = 466
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.x = (self.screenwidth / 2) - (self.app_width / 2)
        self.y = (self.screenheight / 2) - (self.app_height / 2)
        self.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
        self.title("Connect New Device")
        self.resizable(False, False)
        self.attributes('-topmost', 'true')

        # Main Title
        self.main_title = customtkinter.CTkLabel(self, text="Add Your Device", font=('Bold', 20), )
        self.main_title.pack(padx=5, pady=5)

        # Name Title
        self.name_title = customtkinter.CTkLabel(self, text="Device Name:")
        # Name Entry
        self.name_entry = customtkinter.CTkEntry(self, corner_radius=0, fg_color=btn_col, border_width=0)
        # Name Title & Entry Placement
        x_name_placement = 45
        y_name_placement = 30
        self.name_title.place(x=10 + x_name_placement, y=10 + y_name_placement)
        self.name_entry.place(x=100 + x_name_placement, y=10 + y_name_placement)

        # Select Device Title
        self.device_type_title = customtkinter.CTkLabel(self, text="Device Type:")
        # Select Device ComboBox
        self.device_type_combo = customtkinter.CTkComboBox(self, corner_radius=0, fg_color=btn_col, border_width=0,
                                                           values=["(Select Device Type)", "Smart Bulb", "Smart Plug"])
        # Select Device Title & Entry Placement
        x_device_placement = 45
        y_device_placement = 60
        self.device_type_title.place(x=10 + x_device_placement, y=10 + y_device_placement)
        self.device_type_combo.place(x=100 + x_device_placement, y=10 + y_device_placement)

        # Select Device Title
        self.device_title = customtkinter.CTkLabel(self, text="Select Device:")
        # Select Device ComboBox
        self.device_combo = customtkinter.CTkComboBox(self, corner_radius=0, fg_color=btn_col, border_width=0,
                                                      values=["(Select Device)"])
        # Select Device Title & Entry Placement
        x_device_placement = 45
        y_device_placement = 90
        self.device_title.place(x=10 + x_device_placement, y=10 + y_device_placement)
        self.device_combo.place(x=100 + x_device_placement, y=10 + y_device_placement)

        # Background for Settings
        self.background_label = customtkinter.CTkLabel(self, text="", image=self.details_background)
        self.background_label.place(x=10, y=135)

        # Options for Settings
        self.option1_label = customtkinter.CTkLabel(self, text="", bg_color="#2b2b2b")
        self.option1_entry = customtkinter.CTkEntry(self, corner_radius=0, fg_color=btn_col, border_width=1)
        self.option2_label = customtkinter.CTkLabel(self, text="", bg_color="#2b2b2b")
        self.option2_entry = customtkinter.CTkEntry(self, corner_radius=0, fg_color=btn_col, border_width=1)
        self.option3_label = customtkinter.CTkLabel(self, text="", bg_color="#2b2b2b")
        self.option3_entry = customtkinter.CTkEntry(self, corner_radius=0, fg_color=btn_col, border_width=1)

        # Close Button
        self.close_button = customtkinter.CTkButton(self, text="Submit", fg_color=btn_col,
                                                    command=self.close_button_event)
        self.close_button.place(x=100, y=425)

        self.combo_box_check()
        self.device_settings()

    def combo_box_check(self):
        global device_type
        device_check = self.device_type_combo.get()
        if device_check != device_type:
            device_type = device_check
            self.device_combo.set("(Select Device)")
            if device_type == "(Select Device Type)":
                self.device_combo.configure(values=["(Select Device)"])
            if device_type == "Smart Bulb":
                self.device_combo.configure(values=["(Select Device)", "Tapo L530", "Example2"])
            if device_type == "Smart Plug":
                self.device_combo.configure(values=["(Select Device)", "Example1", "Example2"])
        self.device_combo.after(10, self.combo_box_check)

    def device_settings(self):

        device_selected = self.device_combo.get()
        if device_selected == "Tapo L530":
            # Configures
            self.option1_label.configure(text="IP Address:")
            self.option2_label.configure(text="Tapo Account Email:")
            self.option3_label.configure(text="Tapo Account Password:")
            self.option3_entry.configure(show='*')
            self.details_background.configure(size=(309, 120))

            # Places
            self.option1_label.place(x=15, y=140)
            self.option1_entry.place(x=82.5, y=140)
            self.option2_label.place(x=15, y=180)
            self.option2_entry.place(x=135, y=180)
            self.option3_label.place(x=15, y=220)
            self.option3_entry.place(x=160, y=220)
        else:
            self.option1_label.place_forget()
            self.option1_entry.place_forget()
            self.option2_label.place_forget()
            self.option2_entry.place_forget()
            self.option3_label.place_forget()
            self.option3_entry.place_forget()
            self.details_background.configure(size=(309, 280))

        self.device_combo.after(10, self.device_settings)

    def close_button_event(self):
        global NumOfDevices
        global isTopWindowOpen
        device_name = self.name_entry.get()
        device_selected = self.device_combo.get()

        if device_selected == "Tapo L530":
            ip_address = self.option1_entry.get()
            account = self.option2_entry.get()
            password = self.option3_entry.get()
            self.store_tapo_l530(device_name, device_selected, ip_address, account, password)
        isTopWindowOpen = False
        self.destroy()

    def store_tapo_l530(self, device_name, device_selected, ip, account_name, password):
        try:
            self.conn.execute(
                f"INSERT INTO {user}_devices_info (device_name, device_type, ip, account_name, password) VALUES (?,?,?,?,?)",
                (device_name, device_selected, ip, account_name, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("DEVICE STORE FAILED: DEVICE ALREADY STORED")
            return False


class ControlDeviceWindow(customtkinter.CTkToplevel):
    def __init__(self, identification):
        super().__init__()

        global isTopWindowOpen
        isTopWindowOpen = True

        # images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.power_off_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "power_off.png")),
                                                    size=(150, 150))
        self.power_on_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "power_on.png")),
                                                   size=(150, 150))
        self.saturation = customtkinter.CTkImage(Image.open(os.path.join(image_path, "brightness_bar.png")),
                                                 size=(200, 16))
        self.hue = customtkinter.CTkImage(Image.open(os.path.join(image_path, "hue_bar.png")),
                                          size=(200, 16))
        self.temperature = customtkinter.CTkImage(Image.open(os.path.join(image_path, "temperature_bar.png")),
                                                  size=(200, 16))

        try:
            conn = sqlite3.connect(f'{user}_devices.db')
            conn.execute(f"CREATE TABLE IF NOT EXISTS {user}_devices_info(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "device_name TEXT UNIQUE NOT NULL, "
                         "device_type TEXT NOT NULL, "
                         "ip TEXT, "
                         "account_name TEXT, "
                         "password TEXT)")
            cursor = conn.cursor()
            select_query = f"SELECT * from {user}_devices_info WHERE id=?"
            cursor.execute(select_query, (identification,))
            records = cursor.fetchall()
            for row in records:
                print("Current ID: ", row[0])
                id = row[0]
                print("Current Name: ", row[1])
                name = row[1]
                print("Current Type: ", row[2])
                type = row[2]
                print("Current IP: ", row[3])
                ip = row[3]
                print("Current Account Name: ", row[4])
                account_name = row[4]
                print("Current Account Password: ", row[5])
                account_pass = row[5]

        except sqlite3.Error as error:
            print("Failed to read data from table", error)
        finally:
            if conn:
                conn.close()

        # Creating Top Window
        self.app_width = 329
        self.app_height = 466
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.x = (self.screenwidth / 2) - (self.app_width / 2)
        self.y = (self.screenheight / 2) - (self.app_height / 2)
        self.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
        self.title("Control Device")
        self.resizable(False, False)
        self.attributes('-topmost', 'true')

        # Control & ID Title
        self.control_title = customtkinter.CTkLabel(self, text=f"Controls: {name}", font=('Bold', 20))
        self.control_title.pack(padx=5, pady=5)
        self.id_label = customtkinter.CTkLabel(self, text=f"ID: {id}", font=('', 12))
        self.id_label.place(x=5, y=5)

        # Tapo
        self.segmented_button_var = customtkinter.StringVar(value="White Light")
        self.segmented_button = customtkinter.CTkSegmentedButton(self, values=["White Light", "Colour Light"],
                                                                 variable=self.segmented_button_var)
        self.power_btn = customtkinter.CTkButton(self, text="", image=self.power_off_img, fg_color="#242424",
                                                 hover=False, command=self.l530_power_on)
        self.saturation_image = customtkinter.CTkLabel(self, text="", image=self.saturation)
        self.saturation_slider = customtkinter.CTkSlider(self, from_=1, to=100, bg_color="transparent")
        self.colour_image = customtkinter.CTkLabel(self, text="", image=self.hue)
        self.colour_slider = customtkinter.CTkSlider(self, from_=1, to=360)
        self.temperature_image = customtkinter.CTkLabel(self, text="", image=self.temperature)
        self.temperature_slider = customtkinter.CTkSlider(self, from_=6500, to=2500)
        self.submit_btn = customtkinter.CTkButton(self, text="Submit Changes", fg_color=btn_col,
                                                  command=self.submit_event)
        self.close_btn = customtkinter.CTkButton(self, text="Close", fg_color=btn_col, width=30,
                                                 command=self.close_event)

        if type == "Tapo L530":
            try:
                l530_login(ip, account_name, account_pass)
                # Toggle Light Temp/Colour
                self.segmented_button.place(x=88, y=50)
                # Power on/off button
                self.power_btn.place(x=84, y=110)
                # Saturation slider
                self.saturation_image.place(x=170, y=310, anchor=tk.CENTER)
                self.saturation_slider.place(x=170, y=300, anchor=tk.CENTER)
                # Colour slider
                self.colour_image.place(x=170, y=360, anchor=tk.CENTER)
                self.colour_slider.place(x=170, y=350, anchor=tk.CENTER)
                # Temp slider
                self.temperature_image.place(x=170, y=410, anchor=tk.CENTER)
                self.temperature_slider.place(x=170, y=400, anchor=tk.CENTER)
                # Submit Changes Button
                self.submit_btn.place(x=70, y=425)
                # Close Button
                self.close_btn.place(x=220, y=425)
            except:
                CTkMessagebox(title="An Error has Occurred", message="Error: Unable to connect to device.",
                              icon="cancel")
                self.close_event()

    def l530_power_off(self):
        global isPower
        self.power_btn.configure(image=self.power_off_img, command=self.l530_power_on)
        isPower = False
        l530_off()

    def l530_power_on(self):
        global isPower
        self.power_btn.configure(image=self.power_on_img, command=self.l530_power_off)
        isPower = True
        l530_on()

    def submit_event(self):
        brightness = self.saturation_slider.get().__round__()
        temperature = self.temperature_slider.get().__round__()
        colour = self.colour_slider.get().__round__()
        if self.segmented_button.get() == "White Light":
            l530_colour_sat(brightness)
            l530_colour_temp_change(temperature)
        if self.segmented_button.get() == "Colour Light":
            l530_huechange(colour, brightness)

    def close_event(self):
        global isTopWindowOpen
        isTopWindowOpen = False
        self.destroy()


class ScheduleWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        global isTopWindowOpen
        isTopWindowOpen = True

        temp_commands = []

        # Icons
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.add_slot = customtkinter.CTkImage(Image.open(os.path.join(image_path, "add_box.png")),
                                               size=(309, 280))

        # Creating Top Window
        self.app_width = 329
        self.app_height = 466
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.x = (self.screenwidth / 2) - (self.app_width / 2)
        self.y = (self.screenheight / 2) - (self.app_height / 2)
        self.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
        self.title("New Schedule")
        self.resizable(False, False)
        self.attributes('-topmost', 'true')

        # Scrollable Bar
        self.schedule_scrollbar = customtkinter.CTkScrollbar(self)
        self.schedule_scrollbar.pack(padx=5, pady=5)


class PasswordChangeWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        global isTopWindowOpen
        isTopWindowOpen = True

        # Creating Top Window
        self.app_width = 329
        self.app_height = 466
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.x = (self.screenwidth / 2) - (self.app_width / 2)
        self.y = (self.screenheight / 2) - (self.app_height / 2)
        self.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
        self.title("Change Password")
        self.resizable(False, False)
        self.attributes('-topmost', 'true')

        # Title
        self.main_title = customtkinter.CTkLabel(self, text="Change Password", font=('Bold', 20))
        self.main_title.pack(padx=5, pady=5)

        # Username, Current Password, New Password
        self.username_label = customtkinter.CTkLabel(self, text="Username")
        self.username_second_label = customtkinter.CTkLabel(self, text=user, text_color='#999999')
        self.current_pass_label = customtkinter.CTkLabel(self, text="Current Password")
        self.current_pass_entry = customtkinter.CTkEntry(self, corner_radius=0, fg_color=btn_col, border_width=1,
                                                         show='*')
        self.new_pass_label = customtkinter.CTkLabel(self, text="New Password")
        self.new_pass_entry = customtkinter.CTkEntry(self, corner_radius=0, fg_color=btn_col, border_width=1, show='*')

        # Placing
        self.username_label.place(x=15, y=40)
        self.username_second_label.place(x=15, y=65)
        self.current_pass_label.place(x=15, y=100)
        self.current_pass_entry.place(x=15, y=125)
        self.new_pass_label.place(x=15, y=160)
        self.new_pass_entry.place(x=15, y=185)

        # Submit and Close Button
        self.submit_button = customtkinter.CTkButton(self, text="Submit", fg_color=btn_col,
                                                     command=self.change_password)
        self.close_button = customtkinter.CTkButton(self, text="Exit", fg_color=btn_col, command=self.close_event)

        # Submit Changes Button
        self.submit_button.place(x=20, y=425)
        # Close Button
        self.close_button.place(x=170, y=425)

    def change_password(self):

        conn = sqlite3.connect('user.db')
        conn.execute(
            "CREATE TABLE IF NOT EXISTS user_info(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
        cursor = conn.cursor()

        username = user
        current_pass = self.current_pass_entry.get()
        new_pass = self.new_pass_entry.get()

        query = "SELECT password FROM user_info WHERE username=?"
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if row:
            password = row[0]
            print(f"Password for user {username}: {password}")
            if bcrypt.checkpw(current_pass.encode('utf-8'), password):
                encrypt_pass = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
                print(encrypt_pass)
                pass_query = "UPDATE user_info SET password=? WHERE username=?"
                data = (encrypt_pass, username)
                cursor.execute(pass_query, data)
                conn.commit()
                CTkMessagebox(title="Succeeded", message="Password has been Successfully Changed", icon="check")
                self.close_event()
            else:
                CTkMessagebox(title="Failed", message="Password incorrect", icon="cancel")
        else:
            print("No User found")

    def close_event(self):
        global isTopWindowOpen
        isTopWindowOpen = False
        self.destroy()


def main():
    if isLoginApp:
        login = LoginApp()
        login.mainloop()
    if isMainApp:
        mainapp = MainApp()
        mainapp.mainloop()


# mainloop - DO NOT CHANGE
if __name__ == "__main__":
    main()
