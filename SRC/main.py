#main

from gui_interface import BusinessReportGUI
from terminal_interface import run_terminal_interface
import tkinter as tk

# --- APPLICATION ENTRY POINT ---

def main():
    """
    Main function to run the Business Report Generator application.

    It prompts the user to choose between a terminal interface (CLI)
    and a graphical user interface (GUI) and then launches the
    selected interface.
    """
    print("Welcome to the Business Report Generator!")
    interface_choice = input("Enter 1 for Terminal Interface or 2 for Graphical Interface: ").strip()
    while interface_choice not in ["1", "2"]:
        print("Invalid choice. Please try again.")
        interface_choice = input("Enter 1 for Terminal Interface or 2 for Graphical Interface: ").strip()
    if interface_choice == "1":
        run_terminal_interface()
    else:
        root = tk.Tk()
        BusinessReportGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()