import datetime
import tkinter as tk
import FetchInfo
import NewTask
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import ConnectToDatabase
import FrontEnd
import SessionActivity

global tasks

class StartScreenTime:
    def __init__(self):
        screen_time = FetchInfo.do_i_get_screen_time()
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

        # ///////////////////////////////////// TIME /////////////////////////////////////

        # Get the current time
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # ////////////////////////////////////// Header //////////////////////////////////////
        
        self.header = tk.Label(self.root, text="Start Screen Time!", bg='#303030', fg='white', font=('Cambria', 50), anchor='w', padx=20)
        self.header.place(relx=relx, relwidth=relwidth, height=125, rely=100/screen_height, anchor='nw')

        # Create a label to display the time
        time_label = tk.Label(self.root, text=current_time, bg='#303030', fg='white', font=('Cambria', 45), anchor='e', padx=15)
        time_label.place(relx=1-relx, rely=100/screen_height + 0.5*125/screen_height, anchor='e')

        # Update the time every second
        def update_time():
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            time_label.config(text=current_time)
            self.root.after(1000, update_time)

        update_time()

        self.header_border = tk.Frame(self.root, bg='white', height=2)
        self.header_border.place(relx=relx, relwidth=relwidth, rely=(100+123)/screen_height, anchor='nw')

        # ////////////////////////////////////// Menu //////////////////////////////////////

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self.root, bg='#303030', highlightthickness=0)    
        # Create a new style
        style = ttk.Style()
        style.configure("TScrollbar", background="#303030")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)

        # Create a frame inside the canvas
        self.menu = tk.Frame(canvas, bg='#303030')

        # Update the scrollregion of the canvas to match the size of the frame
        self.menu.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Make the canvas scrollable with the scrollbar
        canvas.create_window((0, 0), window=self.menu, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Update the width of self.menu to match the width of the canvas
        canvas.bind("<Configure>", lambda e: self.menu.configure(width=e.width))

        # Place the canvas and the scrollbar
        canvas.place(relx=relx, relwidth=relwidth, rely=(100+125)/screen_height, relheight=(screen_height-450)/screen_height, anchor='nw')
        scrollbar.pack(side="right", fill="y")

        # Add screen time in 00:00:00 format
        hours, remainder = divmod(screen_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        screen_time_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        print(screen_time_str)
        self.screen_time_frame = tk.Frame(self.root, bg='#303030')
        self.screen_time_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.screen_time_label = tk.Label(self.screen_time_frame, text=screen_time_str, bg='#303030', fg='white', font=('Cambria', 125), padx=15)
        self.screen_time_label.pack(anchor='center')
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
            e.widget.config(cursor="hand2", activebackground="#88d404", activeforeground="white")

        def on_leave(e):
            e.widget['background'] = '#424242'
            e.widget.config(cursor="", activebackground="#88d404", activeforeground="white")

        def frontend(event):
            self.root.destroy()
            FrontEnd.FrontEnd()

        def Activity(event):
            self.root.destroy()
            SessionActivity.SessionActivity()
        

        help_button = tk.Button(self.root, text="Cancel", bg="#424242", fg="white", font=("Cambria", 20, "bold"), bd=0)
        help_button.place(x=button_x1, y=button_y1, width=300, height=100)
        help_button.bind("<Enter>", on_enter)
        help_button.bind("<Leave>", on_leave)
        help_button.bind("<Button-1>", frontend)


        start_button = tk.Button(self.root, text="Start", bg="#424242", fg="white", font=("Cambria", 20, "bold"), bd=0)
        start_button.place(x=button_x2, y=button_y2, width=300, height=100)
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)
        start_button.bind("<Button-1>", Activity)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        self.root.mainloop()

    def on_closing(self):
        pass

    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)

        # Check if Control, Alt, L, O, C, K are pressed simultaneously
        if self.pressed_keys == {'Control_L', 'Alt_L', 'l', 'o', 'c', 'k'}:
            print("Window closed")
            sys.exit(0)
            
    def on_key_release(self, event):
        self.pressed_keys.discard(event.keysym)
