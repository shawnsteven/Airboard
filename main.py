import sys
import os
from tkinter import *
import tkinter.font as font
import threading
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    window=Tk()

    window.title("Airboard")
    window.geometry('599x886')
    window.configure(bg="white")


    start = PhotoImage(file = "ButtonStart.png")
    button_quit = PhotoImage(file = "ButtonStop.png")
    logo = PhotoImage(file = "bg.png")
    myFont = font.Font(family='Helvetica')


    def run():
        os.system('airboard.py')

    def minimize():
        os.system("TASKKILL /F /IM python.exe")
        window.iconify()



    dispay_logo = Label(window, image = logo, border = 0)
    dispay_logo.place(x = 0, y = 0)


    #start_btn = Button(window, height= "7", width = "20", text="Click to Start", bg="white", fg="black", font = myFont, command=lambda:[threading.Thread(target=run).start(), threading.Thread(target=minimize).start()])
    start_btn = Button(window, bg="white", image = start, borderwidth = 0,highlightthickness = 0, border = 0, command=lambda:[threading.Thread(target=run).start()])
    start_btn.place(x=75, y=565) 
    #start_btn.grid(column=0, row=0)
    quit_btn = Button(window, borderwidth = 0,highlightthickness = 0, image = button_quit, border = 0, bg="white", command=minimize)
    quit_btn.place(x=75, y=650) 
    # stop_program = Button(window, height= "7", width = "20", border = "0", text="stop", bg="white", fg="blue",font = myFont, command=close_program)
    # stop_program.place(x=500, y=500) 

    window.mainloop()


else:
    
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)