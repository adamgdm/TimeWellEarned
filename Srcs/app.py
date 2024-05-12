import tkinter as tk
import sys
import ConnectToDatabase
import FrontEnd
import NewTask
import threading
import os

def main():

    # Run the main application
    with open('pid.txt', 'w') as f:
        f.write(str(os.getpid()))
    app = FrontEnd.FrontEnd()

main()