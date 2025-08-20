import tkinter as tk
from tkinter import ttk
from multiprocessing import Process
from fer_pipeline import run_fer_loop
from settings import edit_settings, clear_logs
from process_emotion import visualize_logs
from multiprocessing import Process, Event

fer_process = None
stop_event = Event()

def start_detection():
    global fer_process, stop_event
    if fer_process is None or not fer_process.is_alive():
        stop_event.clear()
        fer_process = Process(target=run_fer_loop, args=(stop_event,))
        fer_process.start()
        print("FER process started.")
    else:
        print("FER is already running.")

def stop_detection():
    global fer_process, stop_event
    if fer_process is not None and fer_process.is_alive():
        print("Stopping FER process...")
        stop_event.set()
        fer_process.join()
        print("FER process terminated.")

def on_exit():
    stop_detection()
    root.destroy()

def main():
    global root
    root = tk.Tk()
    root.title("Emoji Cam")
    root.geometry("250x335")
    root.resizable(False, False)
    root.configure(bg="white")

    style = ttk.Style(root)
    style.theme_use('clam')

    button_width = 20

    tk.Button(root, text="Start Detection", command=start_detection,
              height=2, width=button_width, bg="white").pack(pady=7)

    tk.Button(root, text="Stop Detection", command=stop_detection,
              height=2, width=button_width, bg="white").pack(pady=7)

    tk.Button(root, text="Settings", command=lambda: edit_settings(root),
              height=2, width=button_width, bg="white").pack(pady=7)

    tk.Button(root, text="Visualize Logs", command=visualize_logs,
              height=2, width=button_width, bg="white").pack(pady=7)

    tk.Button(root, text="Clear Logs", command=clear_logs,
              height=2, width=button_width, bg="white").pack(pady=7)

    tk.Button(root, text="Exit", command=on_exit,
              height=2, width=button_width, bg="white").pack(pady=7)

    root.mainloop()

if __name__ == "__main__":
    main()