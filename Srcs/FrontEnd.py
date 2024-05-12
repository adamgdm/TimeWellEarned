import datetime
import tkinter as tk
import FetchInfo
import NewTask
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import ConnectToDatabase
import StartScreenTime

global tasks

class FrontEnd:
    def __init__(self):
        tasks = FetchInfo.fetch_info()
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
        
        if current_time >= '00:03:00' and current_time < '12:00:00':
            self.header = tk.Label(self.root, text="Bonjour!", bg='#303030', fg='white', font=('Cambria', 50), anchor='w', padx=20)
        elif current_time >= '12:00:00' and current_time < '18:00:00':
            self.header = tk.Label(self.root, text="Bon après-midi!", bg='#303030', fg='white', font=('Cambria', 50), anchor='w', padx=20)
        else:
            self.header = tk.Label(self.root, text="Bonsoir!", bg='#303030', fg='white', font=('Cambria', 50), anchor='w', padx=20)
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

        # Menu items
        tasks_id = [None] * len(tasks)
        # for each item in the tasks list, create a new frame with a label and a button
        for i in range(len(tasks)):
            tasks_id[i] = tasks[i]['ID']
            item = tk.Frame(self.menu, bg='#303030')
            item.pack(fill='both', expand=True)

            id_label = tk.Label(item, text=str(i+1), bg='#303030', fg='white', font=('Cambria', 25))
            id_label.pack(side='left', padx=40, pady=12.5)

            # Calculate the width of the task_label
            canvas_width = canvas.winfo_width()
            id_label_width = id_label.winfo_reqwidth()
            button_width = 50 + 2 * 10  # Button width plus padding
            task_label_width = canvas_width - id_label_width - button_width + 152

            task_label = tk.Label(item, text=f"{tasks[i]['DESCRIPTION']}", bg='#303030', fg='white', font=('Cambria', 25), anchor='w', width=task_label_width)
            task_label.pack(side='left', fill='both', expand=True)

            def on_button_click(i=i):  # Capture the current value of i
                # Connect to the database
                mydb = ConnectToDatabase.contodb()
                mycursor = mydb.cursor()

                # Update the status of the task to 'DONE'
                sql = "UPDATE TASKS SET STATUS = 'DONE' WHERE ID = %s"
                val = (tasks_id[i],)  # Make sure val is a tuple
                mycursor.execute(sql, val)

                # Commit the changes
                mydb.commit()
                # refresh tasks 

                global tasks
                tasks = FetchInfo.fetch_info()
                self.root.destroy()
                FrontEnd()
            
            # Open the image file
            img = Image.open("Srcs\\Media\\icon.png")
            # Resize the image
            img = img.resize((64, 64))
            # Convert the image to a PhotoImage
            image = ImageTk.PhotoImage(img)

            img2 = Image.open("Srcs\\Media\\iconS.png")
            img2 = img2.resize((64, 64))
            image2 = ImageTk.PhotoImage(img2)

            # Create a new style
            style = ttk.Style()
            style.configure("TButton", background="#303030")

            # Create the button with the new style
            if (tasks[i]['STATUS'] == 'TODO'):
                button = ttk.Button(item, image=image2, style="TButton")
                button.image = image2 
            else:
                button = ttk.Button(item, image=image, style="TButton")
                button.image = image # Keep a reference to the image object to prevent it from being garbage collected
            button.pack(side='right', padx=15, pady=10)

            # Bind the button click event to the function and refresh the tasks right after
            if (tasks[i]['STATUS'] == 'TODO'):
                button.bind("<Button-1>", lambda e, i=i: on_button_click(i))

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

        help_button = tk.Button(self.root, text="Help", bg="#424242", fg="white", font=("Cambria", 20, "bold"), bd=0)
        help_button.place(x=button_x1, y=button_y1, width=300, height=100)
        help_button.bind("<Enter>", on_enter)
        help_button.bind("<Leave>", on_leave)

        def screentime():
            screen_time = FetchInfo.do_i_get_screen_time()
            if screen_time > 0:
                self.root.destroy()
                new_task = StartScreenTime.StartScreenTime()
                new_task.root.mainloop()
            else:
                self.root.destroy()
                FrontEnd()

        start_button = tk.Button(self.root, text="Start", bg="#424242", fg="white", font=("Cambria", 20, "bold"), bd=0, command=screentime)
        start_button.place(x=button_x2, y=button_y2, width=300, height=100)
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        self.root.mainloop()

    def on_closing(self):
        pass

    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)

        # Check if Control, Alt, L, O, C, K are pressed simultaneously

        if self.pressed_keys == {'n'}:
            self.root.destroy()
            new_task = NewTask.NewTask()
            new_task.root.mainloop()    
    
        if self.pressed_keys == {'a', '5'}:
            self.root.destroy()
            self.root.quit()
        

    def on_key_release(self, event):
        self.pressed_keys.discard(event.keysym)
