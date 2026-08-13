# Disclaimer
#This tool is provided for educational and authorized testing purposes only. The author assumes no liability and is not responsible for any misuse or damage caused by this program.
import socket
import sys
from datetime import datetime
import os
import concurrent.futures
import customtkinter

# Blank the screen
os.system('cls' if os.name == 'nt' else 'clear')


def scanner(args):
    remoteServerIP, i = args
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 0.1 should only be used in localhost, as to mitigate false negatives.
        sock.settimeout(0.5)
        result = sock.connect_ex((remoteServerIP, i))
        if result == 0:
            print("Port", i, "is open")
        sock.close()
    except KeyboardInterrupt:
        sys.exit()
    except socket.gaierror:
        sys.exit()
    except socket.error:
        sys.exit()
    return i


def button_callback():
    print("button clicked")
    # User input
    remoteServer = textbox.get("1.0", "end-1c")
    remoteServerIP = socket.gethostbyname(remoteServer)

    # Print a banner with information on which host we are about to scan
    print(" ")
    print("Please wait, scanning remote host", remoteServerIP)
    print(" ")

    # Check the date and time the scan was started
    time1 = datetime.now()

    # Create tuples containing both the IP and each port for the worker pool
    tasks = [(remoteServerIP, port) for port in range(1, 2000)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as pool:
        results = pool.map(scanner, tasks)

    # Checking time again
    time2 = datetime.now()

    # Calculate the difference in time to know how long the scan took
    totaltime = time2 - time1

    # Print the Information
    print("Total time: ", totaltime)



if __name__ == '__main__':

    app = customtkinter.CTk()
    app.geometry("800x800")


    label = customtkinter.CTkLabel(app, text="CTkLabel", fg_color="transparent")#
    label.pack(padx=20, pady=11)
    label.configure(text="Port-Scanner")
    text = label.cget("text")
    button = customtkinter.CTkButton(app, text="Start_Scan", command=button_callback)
    button.pack(padx=20, pady=20)
    textbox = customtkinter.CTkTextbox(app)
    textbox.pack(padx=20, pady=10, fill="both", expand=True)
    textbox.insert("0.0", "new text to insert")
    #textbox.configure(state="enabled")

    app.mainloop()
