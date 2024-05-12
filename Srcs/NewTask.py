import tkinter as tk
import FetchInfo
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Toplevel, Label
import FrontEnd
import sys
import ConnectToDatabase

tasks = FetchInfo.fetch_info()

class NewTask:
    def __init__(self):
        self.root = tk.Tk()
        self.pressed_keys = set()
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.title("Full Screen")
        self.root.configure(bg='#303030')
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Key>', self.on_key_press)
        self.root.overrideredirect(True)  # Remove window border and title bar
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))  # Cover the entire screen
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.root.focus_force()  # Force focus onto the window

        # :::::::::::::::::::::::::::::::::::STYLING THE WINDOW:::::::::::::::::::::::::::::::::::::::::
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width}x{screen_height}')

        # Calculate the margins in pixels
        margin_pixels = 300

        # Calculate the width of the screen minus the margins
        screen_width = self.root.winfo_screenwidth()
        width_pixels = screen_width - 2 * margin_pixels

        # Calculate the relative width and margins
        relwidth = width_pixels / screen_width
        relx = margin_pixels / screen_width

        # ///////////////////////////////////// BACK BUTTON /////////////////////////////////////
        
        def close_and_run_frontend(self):
            # Create a new top-level window
            loading_window = Toplevel(self.root)
            loading_window.geometry('200x100')  # Adjust size as needed

            # Add a label with a loading message
            loading_label = Label(loading_window, text="Loading...")
            loading_label.pack()

            # Update the window to make sure it's displayed before the long-running task
            loading_window.update()

            # Destroy the current window and create the FrontEnd
            self.root.destroy()
            app = FrontEnd.FrontEnd()

            # Destroy the loading window
            loading_window.destroy()

        # Open the image file
        img = Image.open("Srcs\\Media\\back.png")
        # Resize the image
        img = img.resize((50, 50))
        # Convert the image to a PhotoImage
        image = ImageTk.PhotoImage(img)

        # Create a new style
        style = ttk.Style()
        style.configure("TButton", background="#303030")

        # Create the button with the new style
        button = ttk.Button(self.root, image=image, style="TButton", command=lambda: close_and_run_frontend(self))
        button.image = image  # Keep a reference to the image object to prevent it from being garbage collected
        button.place(x=25, y=25)  # Use place to position the button at coordinates (25, 25)

        # ////////////////////////////////////// Header //////////////////////////////////////
        
        self.header = tk.Label(self.root, text="New Task", bg='#303030', fg='white', font=('Cambria', 50), anchor='w', padx=20)
        self.header.place(relx=relx, relwidth=relwidth, height=125, rely=100/screen_height, anchor='nw')

        self.header_border = tk.Frame(self.root, bg='white', height=2)
        self.header_border.place(relx=relx, relwidth=relwidth, rely=(100+123)/screen_height, anchor='nw')

        # ////////////////////////////////////// Menu //////////////////////////////////////

        # create an input field for the task name
        self.task_name_label = tk.Label(self.root, text="Task Name", bg='#303030', fg='white', font=('Cambria', 25), anchor='w', padx=20)
        self.task_name_label.place(relx=relx, relwidth=relwidth, height=50, rely=(100+125+25)/screen_height, anchor='nw')

        self.task_name_entry = tk.Text(self.root, bg='#404040', fg='white', font=('Cambria', 25), insertbackground='white', bd=1, highlightbackground='white')
        self.task_name_entry.place(relx=relx, relwidth=relwidth, height=50, rely=(100+125+75)/screen_height, anchor='nw')

        # create an input field for the task description
        self.task_description_label = tk.Label(self.root, text="Task Description", bg='#303030', fg='white', font=('Cambria', 25), anchor='w', padx=20)
        self.task_description_label.place(relx=relx, relwidth=relwidth, height=50, rely=(100+125+125+25)/screen_height, anchor='nw')

        self.task_description_entry = tk.Text(self.root, bg='#404040', fg='white', font=('Cambria', 25), insertbackground='white', bd=1, highlightbackground='white')
        self.task_description_entry.place(relx=relx, relwidth=relwidth, height=450, rely=(100+125+125+75+50)/screen_height, anchor='nw')

        # //////////////////////////////////////  Footer ////////////////////////////////////// 
        self.footer = tk.Frame(self.root, bg='#303030')
        self.footer.place(relx=relx, relwidth=relwidth, height=125, rely=(screen_height-100-125)/screen_height, anchor='nw')
        
        # Create a canvas for the top border
        top_border = tk.Canvas(self.footer, bg='white', height=2, bd=0, highlightthickness=0)
        top_border.pack(fill='x', side='top')
        # Calculate the y-coordinate for the top of the footer
        footer_y = screen_height - 100 - 125

        # Calculate the y-coordinate for the center of the footer
        footer_center_y = footer_y + 12.5
        screen_middle_x = screen_width / 2  


        # Calculate the x and y coordinates for the buttons
        button_x1 = screen_middle_x - 310 
        button_x2 = screen_middle_x + 10
        button_y1 = footer_center_y - 100/screen_height
        button_y2 = footer_center_y + 100/screen_height
        
        # Create a new style

        style = ttk.Style()
        def on_enter(e):
            e.widget['background'] = '#636363'
            task_name_content = self.task_name_entry.get("1.0", 'end-1c')
            task_description_content = self.task_description_entry.get("1.0", 'end-1c')
            if task_name_content.strip() and task_description_content.strip():
                e.widget.config(cursor="hand2", activebackground="#88d404", activeforeground="white")
            else:
                e.widget.config(cursor="hand2", activebackground="red", activeforeground="white")

        def on_leave(e):
            e.widget['background'] = '#424242'
            task_name_content = self.task_name_entry.get("1.0", 'end-1c')
            task_description_content = self.task_description_entry.get("1.0", 'end-1c')
            if task_name_content.strip() and task_description_content.strip():
                e.widget.config(cursor="", activebackground="#88d404", activeforeground="white")
            else:
                e.widget.config(cursor="", activebackground="red", activeforeground="white")

        def on_button_click():
            self.root.destroy()
            frontend = FrontEnd.FrontEnd()
        
        def create_task():
            task_name_content = self.task_name_entry.get("1.0", 'end-1c')
            task_description_content = self.task_description_entry.get("1.0", 'end-1c')
            if task_name_content.strip() and task_description_content.strip():
                print(task_name_content)
                print(task_description_content)
                db = ConnectToDatabase.contodb()
                cursor = db.cursor()
                cursor.execute("USE DB")
                cursor.execute("INSERT INTO TASKS (NAME, DESCRIPTION, STATUS) VALUES (%s, %s, 'TODO')", (task_name_content, task_description_content))
                db.commit()
                on_button_click()
            else:
                print("Task name and description cannot be empty")

        help_button = tk.Button(self.root, text="Cancel", bg="#424242", fg="white", font=("Cambria", 20, "bold"), bd=0)
        help_button.place(x=button_x1, y=button_y1, width=300, height=100)
        help_button.bind("<Enter>", on_enter)
        help_button.bind("<Leave>", on_leave)
        help_button.bind("<Button-1>", lambda e: on_button_click())

        start_button = tk.Button(self.root, text="Add", bg="#424242", fg="white", font=("Cambria", 20, "bold"), bd=0)
        start_button.place(x=button_x2, y=button_y2, width=300, height=100)
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)
        start_button.bind("<Button-1>", lambda e: create_task())

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        self.root.mainloop()

    def on_closing(self):
        pass

    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)

        # Check if Control, Alt, L, O, C, K are pressed simultaneously
        if self.pressed_keys == {'Control_L', 'Alt_L', 'l', 'o', 'c', 'k'}:
            sys.exit(0)

    def on_key_release(self, event):
        self.pressed_keys.discard(event.keysym)