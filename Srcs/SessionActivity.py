import datetime
import tkinter as tk
import FetchInfo
import NewTask
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import ConnectToDatabase
import StartScreenTime

class SessionActivity:  # replace with your actual class name

    def __init__(self):
        self.screen_time = FetchInfo.do_i_get_screen_time()
        self.init_screen_time = self.screen_time
        self.root = tk.Tk()
        self.pressed_keys = set()
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.title("Full Screen")
        self.root.configure(bg='#303030')
        self.root.resizable(False, False)  # Make the window not resizable
        self.root.overrideredirect(True)  # Remove window border and title bar
        self.root.protocol("WM_DELETE_WINDOW", self.do_nothing)  # Disable closing the window
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.root.geometry("250x50")
        self.screen_time_frame = tk.Frame(self.root)
        self.screen_time_frame.pack()

        self.screen_time_label = tk.Label(self.screen_time_frame, bg='#303030', fg='white', font=('Cambria', 30), padx=15)
        self.screen_time_label.pack(side='left', anchor='w', expand=True)

        # Open the image file
        img = Image.open("Srcs\\Media\\pause.png")
        # Resize the image
        img = img.resize((45, 45))  # Resize the image to 50x50 pixels
        # Convert the image to a PhotoImage
        image = ImageTk.PhotoImage(img)

        # Create a style object
        style = ttk.Style()

        # Set the button size to 50x50 pixels
        style.configure('TButton', background="#303030")

        # Create the button
        self.button = ttk.Button(self.screen_time_frame, image=image, style='TButton' ,command=self.on_button_press, cursor='hand2')
        self.button.image = image
        self.button.pack(side='right', anchor='e', expand=True)

        self.update_countdown()

        if self.screen_time == 0:
            self.on_button_press()


        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()

        # Calculate position x and y coordinates
        x = screen_width - 250 - 30
        y = 30

        self.root.geometry(f"{250}x{50}+{x}+{y}")  # Set the dimension of the window and position it at the top right

    def do_nothing(self):
        pass

    def update_countdown(self):
        if self.screen_time > 0:
            self.screen_time -= 1
            time_str = "{:02}:{:02}:{:02}".format(self.screen_time // 3600, (self.screen_time // 60) % 60, self.screen_time % 60)
            self.screen_time_label.config(text=time_str)
            self.root.after(1000, self.update_countdown)

    def insert_screen_time(self):
        timeconsumed = self.init_screen_time - self.screen_time
        db = ConnectToDatabase.contodb()
        cursor = db.cursor()
        cursor.execute("USE DB")
        cursor.execute(f"INSERT INTO USED_SCREEN_TIME (TIME) VALUES ({timeconsumed});")
        db.commit()

        # Update the screen_time_label with the time consumed
        timeconsumed_str = "{:02}:{:02}:{:02}".format(timeconsumed // 3600, (timeconsumed // 60) % 60, timeconsumed % 60)
        self.screen_time_label.config(text=timeconsumed_str)
    
    
    def on_button_press(self):
        # Insert the time consumed into the database
        self.insert_screen_time()
        self.root.destroy()
        StartScreenTime.StartScreenTime()

    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)

    def on_key_release(self, event):
        if self.pressed_keys == {'Control_L', 'Alt_L', 'l', 'o', 'c', 'k'}:
            self.pressed_keys.clear()

            # Insert the time consumed into the database and update the screen_time_label
            self.insert_screen_time()

            # Exit the program
            sys.exit(0)
        else:
            self.pressed_keys.discard(event.keysym)