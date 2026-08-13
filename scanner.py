# Disclaimer
# This tool is provided for educational and authorized testing purposes only. The author assumes no liability and is not responsible for any misuse or damage caused by this program.
import socket
import sys
from datetime import datetime
import os
import concurrent.futures
import customtkinter

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')


def scanner(args):
    remoteServerIP, port = args
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    try:
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            return port
    except (socket.gaierror, socket.error):
        pass
    finally:
        sock.close()
    return None  # return None if port is closed


def button_callback():
    # enable textbox for writeing
    openportsoutputarea.configure(state="normal")
    openportsoutputarea.delete("1.0", "end")
    openportsoutputarea.insert("end", "Scanning started...\n")

    # user input
    remoteServer = textbox.get("1.0", "end-1c").strip()
    try:
        remoteServerIP = socket.gethostbyname(remoteServer)
    except socket.gaierror:
        openportsoutputarea.insert("end", "Invalid hostname or IP address.\n")
        openportsoutputarea.configure(state="disabled")
        return

    print(" ")
    print("Please wait, scanning remote host", remoteServerIP)
    print(" ")

    # get start tike
    time1 = datetime.now()

    # create tuples for worker pool
    tasks = [(remoteServerIP, port) for port in range(1, 2000)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as pool:
        results = pool.map(scanner, tasks)

    time2 = datetime.now()
    totaltime = time2 - time1

    print("Total time: ", totaltime)
    openportsoutputarea.insert("end", f"\n--- Scan finished in {totaltime} ---\n")

    for port in results:
        if port is not None:
            openportsoutputarea.insert("end", f"Port {port} is open\n")

    # lock it back up (read-only)
    openportsoutputarea.configure(state="disabled")


if __name__ == '__main__':
    app = customtkinter.CTk()
    app.geometry("700x500")

    # labels
    current_text = "Please enter the remote host:"
    label = customtkinter.CTkLabel(
        app,
        text=current_text,
        fg_color="transparent",
        font=("Arial", 20, "bold"),
        text_color="white",
    )
    label.place(x=0, y=70)

    button = customtkinter.CTkButton(
        app,
        text="Start_Scan",
        command=button_callback,
        width=280,
        height=50,
        font=("Arial", 20,),
        text_color="white",
    )
    button.place(x=400, y=100)

    textbox = customtkinter.CTkTextbox(
        app,
        width=280,
        height=50,
    )
    textbox.place(x=0, y=100)
    textbox.insert("0.0", "127.0.0.1")

    openportsoutputarea = customtkinter.CTkTextbox(
        app,
        width=700,
        height=270,
    )
    openportsoutputarea.place(x=0, y=200)

    app.mainloop()