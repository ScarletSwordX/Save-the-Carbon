import tkinter as tk
from tkinter import ttk, messagebox
from navigation_interface import NavigationInterface
from dragon_game import DragonGameInterface

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Save the Carbon")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Create main menu
        self.create_main_menu()
        
    def create_main_menu(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Welcome to Save the Carbon", 
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=30)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        # Navigation interface button
        nav_button = tk.Button(
            button_frame,
            text="🗺️ Navigation Interface",
            font=("Arial", 14),
            bg='#4CAF50',
            fg='white',
            width=25,
            height=3,
            command=self.open_navigation
        )
        nav_button.pack(pady=10)
        
        
        # Dragon game interface button
        game_button = tk.Button(
            button_frame,
            text="🐉 Slay the Dragon",
            font=("Arial", 14),
            bg='#FF9800',
            fg='white',
            width=25,
            height=3,
            command=self.open_dragon_game
        )
        game_button.pack(pady=10)
        
    def open_navigation(self):
        nav_window = tk.Toplevel(self.root)
        NavigationInterface(nav_window)
        
        
    def open_dragon_game(self):
        game_window = tk.Toplevel(self.root)
        DragonGameInterface(game_window)

if __name__ == '__main__':
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
