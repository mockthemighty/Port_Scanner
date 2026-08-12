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


if __name__ == '__main__':
    app = customtkinter.CTk()
    app.geometry("400x150")

    button = customtkinter.CTkButton(app, text="my button", command=button_callback)
    button.pack(padx=20, pady=20)
    textbox = customtkinter.CTkTextbox(app)
    textbox.pack(padx=20, pady=10, fill="both", expand=True)
    textbox.insert("0.0", "new text to insert")
    textbox.configure(state="disabled")
    app.mainloop()
