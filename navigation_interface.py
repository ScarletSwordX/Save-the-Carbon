import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
import math

class NavigationInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 Low-Carbon Navigation Interface")
        self.root.geometry("1200x800")
        self.root.configure(bg='#e8f5e8')
        
        # User data
        self.user_data = self.load_user_data()
        self.generated_routes = []
        self.selected_route = None
        
        # Create main framework
        self.create_widgets()
        self.update_progress_display()
        
    def load_user_data(self):
        """Load user data"""
        try:
            if os.path.exists('user_data.json'):
                with open('user_data.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        # Default user data
        return {
            'total_co2_saved': 0.0,  # Total CO₂ reduction (kg CO₂)
            'game_challenges': 0,    # Game challenge count
            'inventory': {           # Inventory items
                'potions': 0,        # HP potions
                'iron_sword': 0,     # Iron sword
                'iron_armor': 0      # Iron armor
            },
            'eco_routes_taken': 0    # Eco-friendly routes taken
        }
    
    def save_user_data(self):
        """Save user data"""
        try:
            with open('user_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except:
            pass
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="🌱 Low-Carbon Navigation System",
            font=("Arial", 24, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32'
        )
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#e8f5e8')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left input area
        left_frame = tk.Frame(main_frame, bg='#e8f5e8')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right progress and reward area
        right_frame = tk.Frame(main_frame, bg='#e8f5e8', width=300)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        right_frame.pack_propagate(False)
        
        self.create_input_area(left_frame)
        self.create_progress_area(right_frame)
        self.create_routes_area(left_frame)
        
    def create_input_area(self, parent):
        # Input area frame
        input_frame = tk.LabelFrame(
            parent,
            text="📍 Navigation Input",
            font=("Arial", 14, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32',
            padx=15,
            pady=10
        )
        input_frame.pack(fill='x', pady=(0, 15))
        
        # Start point input
        start_frame = tk.Frame(input_frame, bg='#e8f5e8')
        start_frame.pack(fill='x', pady=5)
        
        tk.Label(
            start_frame,
            text="🚀 Start:",
            font=("Arial", 12, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32'
        ).pack(side='left')
        
        self.start_entry = tk.Entry(
            start_frame,
            font=("Arial", 11),
            width=40,
            relief='solid',
            bd=1
        )
        self.start_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)
        self.start_entry.insert(0, "Please enter start address...")
        self.start_entry.bind('<FocusIn>', self.clear_start_placeholder)
        self.start_entry.bind('<FocusOut>', self.add_start_placeholder)
        
        # End point input
        end_frame = tk.Frame(input_frame, bg='#e8f5e8')
        end_frame.pack(fill='x', pady=5)
        
        tk.Label(
            end_frame,
            text="🎯 End:",
            font=("Arial", 12, "bold"),
            bg='#e8f5e8',
            fg='#d32f2f'
        ).pack(side='left')
        
        self.end_entry = tk.Entry(
            end_frame,
            font=("Arial", 11),
            width=40,
            relief='solid',
            bd=1
        )
        self.end_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)
        self.end_entry.insert(0, "Please enter end address...")
        self.end_entry.bind('<FocusIn>', self.clear_end_placeholder)
        self.end_entry.bind('<FocusOut>', self.add_end_placeholder)
        
        # Button area
        button_frame = tk.Frame(input_frame, bg='#e8f5e8')
        button_frame.pack(fill='x', pady=10)
        
        # Generate route button
        generate_button = tk.Button(
            button_frame,
            text="🌱 Generate Eco Route",
            font=("Arial", 12, "bold"),
            bg='#4caf50',
            fg='white',
            width=20,
            height=2,
            command=self.generate_routes
        )
        generate_button.pack(side='left', padx=(0, 10))
        
        # Clear button
        clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=("Arial", 12),
            bg='#ff5722',
            fg='white',
            width=15,
            height=2,
            command=self.clear_inputs
        )
        clear_button.pack(side='left')
        
    def create_progress_area(self, parent):
        # Progress area frame
        progress_frame = tk.LabelFrame(
            parent,
            text="📊 Eco Progress",
            font=("Arial", 14, "bold"),
            bg='#e8f5e8',
            fg='#1976d2',
            padx=15,
            pady=10
        )
        progress_frame.pack(fill='x', pady=(0, 15))
        
        # CO₂ reduction progress
        co2_frame = tk.Frame(progress_frame, bg='#e8f5e8')
        co2_frame.pack(fill='x', pady=5)
        
        tk.Label(
            co2_frame,
            text="🌍 CO₂ Reduction:",
            font=("Arial", 11, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32'
        ).pack(anchor='w')
        
        self.co2_label = tk.Label(
            co2_frame,
            text="0.0 kg CO₂",
            font=("Arial", 12, "bold"),
            bg='#e8f5e8',
            fg='#4caf50'
        )
        self.co2_label.pack(anchor='w')
        
        # Game challenge count
        challenge_frame = tk.Frame(progress_frame, bg='#e8f5e8')
        challenge_frame.pack(fill='x', pady=5)
        
        tk.Label(
            challenge_frame,
            text="⚔️ Challenges:",
            font=("Arial", 11, "bold"),
            bg='#e8f5e8',
            fg='#7b1fa2'
        ).pack(anchor='w')
        
        self.challenge_label = tk.Label(
            challenge_frame,
            text="0 times",
            font=("Arial", 12, "bold"),
            bg='#e8f5e8',
            fg='#9c27b0'
        )
        self.challenge_label.pack(anchor='w')
        
        # Exchange button
        exchange_button = tk.Button(
            progress_frame,
            text="🔄 Exchange Challenges\n(10 kg CO₂ = 1 time)",
            font=("Arial", 10, "bold"),
            bg='#9c27b0',
            fg='white',
            width=20,
            height=2,
            command=self.exchange_co2
        )
        exchange_button.pack(fill='x', pady=10)
        
        # Inventory area
        inventory_frame = tk.LabelFrame(
            parent,
            text="🎒 Inventory",
            font=("Arial", 14, "bold"),
            bg='#e8f5e8',
            fg='#ff9800',
            padx=15,
            pady=10
        )
        inventory_frame.pack(fill='x', pady=(0, 15))
        
        # Item display
        self.potion_label = tk.Label(
            inventory_frame,
            text="💊 HP Potions: 0",
            font=("Arial", 11),
            bg='#e8f5e8',
            fg='#4caf50'
        )
        self.potion_label.pack(anchor='w', pady=2)
        
        self.sword_label = tk.Label(
            inventory_frame,
            text="⚔️ Iron Sword: 0",
            font=("Arial", 11),
            bg='#e8f5e8',
            fg='#2196f3'
        )
        self.sword_label.pack(anchor='w', pady=2)
        
        self.armor_label = tk.Label(
            inventory_frame,
            text="🛡️ Iron Armor: 0",
            font=("Arial", 11),
            bg='#e8f5e8',
            fg='#ff5722'
        )
        self.armor_label.pack(anchor='w', pady=2)
        
        # Reward notification area
        reward_frame = tk.LabelFrame(
            parent,
            text="🎁 Reward Notifications",
            font=("Arial", 14, "bold"),
            bg='#e8f5e8',
            fg='#e91e63',
            padx=15,
            pady=10
        )
        reward_frame.pack(fill='both', expand=True)
        
        self.reward_text = tk.Text(
            reward_frame,
            font=("Arial", 10),
            height=8,
            wrap='word',
            bg='#fff3e0',
            fg='#e91e63',
            relief='solid',
            bd=1
        )
        self.reward_text.pack(fill='both', expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(reward_frame, orient="vertical", command=self.reward_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.reward_text.configure(yscrollcommand=scrollbar.set)
        
    def create_routes_area(self, parent):
        # Route display area
        routes_frame = tk.LabelFrame(
            parent,
            text="🛣️ Available Routes",
            font=("Arial", 14, "bold"),
            bg='#e8f5e8',
            fg='#1976d2',
            padx=15,
            pady=10
        )
        routes_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        # Create scrollable frame
        canvas = tk.Canvas(routes_frame, bg='white', height=300)
        scrollbar = tk.Scrollbar(routes_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.routes_frame = scrollable_frame
        
    def clear_start_placeholder(self, event):
        if self.start_entry.get() == "Please enter start address...":
            self.start_entry.delete(0, tk.END)
            self.start_entry.config(fg='black')
    
    def add_start_placeholder(self, event):
        if not self.start_entry.get():
            self.start_entry.insert(0, "Please enter start address...")
            self.start_entry.config(fg='gray')
    
    def clear_end_placeholder(self, event):
        if self.end_entry.get() == "Please enter end address...":
            self.end_entry.delete(0, tk.END)
            self.end_entry.config(fg='black')
    
    def add_end_placeholder(self, event):
        if not self.end_entry.get():
            self.end_entry.insert(0, "Please enter end address...")
            self.end_entry.config(fg='gray')
    
    def generate_routes(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        
        # Check input
        if start == "Please enter start address..." or not start.strip():
            messagebox.showwarning("Warning", "Please enter start address!")
            return
            
        if end == "Please enter end address..." or not end.strip():
            messagebox.showwarning("Warning", "Please enter end address!")
            return
        
        # Generate routes
        self.generate_route_options(start, end)
        
    def generate_route_options(self, start, end):
        # Clear existing routes
        for widget in self.routes_frame.winfo_children():
            widget.destroy()
        
        # Calculate base distance
        base_distance = random.randint(5, 50)  # kilometers
        
        # Generate different types of routes
        route_types = [
            {
                'name': '🚗 Driving Route',
                'type': 'driving',
                'eco': False,
                'distance': base_distance,
                'time': base_distance * 2,  # minutes
                'co2': base_distance * 0.2,  # kg CO₂
                'color': '#f44336',
                'rewards': [],
                'transfer_info': ''
            },
            {
                'name': '🚌 Bus Route',
                'type': 'bus',
                'eco': True,
                'distance': base_distance * 1.2,
                'time': base_distance * 3,
                'co2': base_distance * 0.05,
                'color': '#2196f3',
                'rewards': self.generate_eco_rewards(),
                'transfer_info': self.generate_bus_transfer()
            },
            {
                'name': '🚶 Bus + Walking Route A',
                'type': 'bus_walking_a',
                'eco': True,
                'distance': base_distance,
                'time': base_distance * 2.5 + 12,  # bus + walking last 1km
                'co2': base_distance * 0.05 - 0.2,  # CO₂ reduction vs driving
                'color': '#4caf50',
                'rewards': self.generate_eco_rewards(),
                'transfer_info': self.generate_bus_transfer_with_walking(1.0)
            },
            {
                'name': '🚶 Bus + Walking Route B',
                'type': 'bus_walking_b',
                'eco': True,
                'distance': base_distance,
                'time': base_distance * 2.3 + 18,  # bus + walking last 1.5km
                'co2': base_distance * 0.05 - 0.3,  # CO₂ reduction vs driving
                'color': '#4caf50',
                'rewards': self.generate_eco_rewards(),
                'transfer_info': self.generate_bus_transfer_with_walking(1.5)
            },
            {
                'name': '🚴 Bus + Cycling Route A',
                'type': 'bus_cycling_a',
                'eco': True,
                'distance': base_distance,
                'time': base_distance * 2.5 + 12,  # bus + cycling last 3km
                'co2': base_distance * 0.05 - 0.6,  # CO₂ reduction vs driving
                'color': '#ff9800',
                'rewards': self.generate_eco_rewards(),
                'transfer_info': self.generate_bus_transfer_with_cycling(3.0)
            },
            {
                'name': '🚴 Bus + Cycling Route B',
                'type': 'bus_cycling_b',
                'eco': True,
                'distance': base_distance,
                'time': base_distance * 2.2 + 20,  # bus + cycling last 5km
                'co2': base_distance * 0.05 - 1.0,  # CO₂ reduction vs driving
                'color': '#ff9800',
                'rewards': self.generate_eco_rewards(),
                'transfer_info': self.generate_bus_transfer_with_cycling(5.0)
            }
        ]
        
        self.generated_routes = route_types
        self.route_var = tk.StringVar()
        
        for i, route in enumerate(route_types):
            self.create_route_item(route, i)
    
    def generate_eco_rewards(self):
        """Generate eco-friendly route rewards"""
        rewards = []
        
        # 50% chance to get potion
        if random.random() < 0.5:
            rewards.append({'type': 'potion', 'name': '💊 HP Potion', 'count': 1})
        
        # 10% chance to get equipment
        if random.random() < 0.1:
            if random.random() < 0.5:
                rewards.append({'type': 'sword', 'name': '⚔️ Iron Sword', 'count': 1})
            else:
                rewards.append({'type': 'armor', 'name': '🛡️ Iron Armor', 'count': 1})
        
        return rewards
    
    def generate_bus_transfer(self):
        """Generate bus transfer information"""
        bus_routes = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 
                     'R101', 'R102', 'R103', 'R104', 'R105', 'R106', 'R107', 'R108', 'R109', 'R110']
        
        # Randomly select 2-4 bus routes
        transfer_count = random.randint(2, 4)
        selected_routes = random.sample(bus_routes, transfer_count)
        
        return ' -> '.join(selected_routes)
    
    def generate_bus_transfer_with_walking(self, final_walk_distance):
        """Generate bus transfer with walking information"""
        bus_routes = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 
                     'R101', 'R102', 'R103', 'R104', 'R105', 'R106', 'R107', 'R108', 'R109', 'R110']
        
        # Randomly select 2-4 bus routes
        transfer_count = random.randint(2, 4)
        selected_routes = random.sample(bus_routes, transfer_count)
        
        # Randomly select 1-2 transfer points that require walking
        walk_transfers = random.randint(1, min(2, transfer_count-1))
        walk_indices = random.sample(range(transfer_count-1), walk_transfers)
        
        transfer_parts = []
        for i, route in enumerate(selected_routes):
            transfer_parts.append(route)
            if i in walk_indices:
                walk_distance = random.uniform(0.2, 0.8)
                transfer_parts.append(f"(walk {walk_distance:.1f}km)")
        
        transfer_text = ' -> '.join(transfer_parts)
        transfer_text += f" -> walk {final_walk_distance:.1f}km to destination"
        
        return transfer_text
    
    def generate_bus_transfer_with_cycling(self, final_cycle_distance):
        """Generate bus transfer with cycling information"""
        bus_routes = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 
                     'R101', 'R102', 'R103', 'R104', 'R105', 'R106', 'R107', 'R108', 'R109', 'R110']
        
        # Randomly select 2-4 bus routes
        transfer_count = random.randint(2, 4)
        selected_routes = random.sample(bus_routes, transfer_count)
        
        # Randomly select 1-2 transfer points that require cycling
        cycle_transfers = random.randint(1, min(2, transfer_count-1))
        cycle_indices = random.sample(range(transfer_count-1), cycle_transfers)
        
        transfer_parts = []
        for i, route in enumerate(selected_routes):
            transfer_parts.append(route)
            if i in cycle_indices:
                cycle_distance = random.uniform(0.5, 2.0)
                transfer_parts.append(f"(cycle {cycle_distance:.1f}km)")
        
        transfer_text = ' -> '.join(transfer_parts)
        transfer_text += f" -> cycle {final_cycle_distance:.1f}km to destination"
        
        return transfer_text
    
    def show_route_popups(self, route):
        """Show popups for each segment of the route"""
        if not route['eco']:
            return
            
        # Parse transfer info to show popups
        transfer_info = route['transfer_info']
        if not transfer_info:
            return
            
        # Split transfer info into segments
        segments = transfer_info.split(' -> ')
        
        for i, segment in enumerate(segments):
            if segment.startswith('R'):  # Bus route
                self.show_bus_popup(segment, i == len(segments) - 1)
            elif 'walk' in segment.lower():  # Walking segment
                distance = self.extract_distance(segment)
                self.show_walking_popup(distance)
            elif 'cycle' in segment.lower():  # Cycling segment
                distance = self.extract_distance(segment)
                self.show_cycling_popup(distance)
    
    def extract_distance(self, segment):
        """Extract distance from segment text"""
        import re
        match = re.search(r'(\d+\.?\d*)', segment)
        return float(match.group(1)) if match else 1.0
    
    def show_bus_popup(self, route_number, is_last=False):
        """Show bus route popup"""
        popup = tk.Toplevel(self.root)
        popup.title("🚌 Bus Route")
        popup.geometry("400x300")
        popup.configure(bg='#e3f2fd')
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Bus route info
        info_frame = tk.Frame(popup, bg='#e3f2fd')
        info_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(
            info_frame,
            text=f"🚌 Bus Route {route_number}",
            font=("Arial", 16, "bold"),
            bg='#e3f2fd',
            fg='#1976d2'
        ).pack(pady=10)
        
        if is_last:
            tk.Label(
                info_frame,
                text="📍 Please get off at your destination",
                font=("Arial", 12),
                bg='#e3f2fd',
                fg='#d32f2f'
            ).pack(pady=10)
        else:
            tk.Label(
                info_frame,
                text="🔄 Please transfer to next route",
                font=("Arial", 12),
                bg='#e3f2fd',
                fg='#388e3c'
            ).pack(pady=10)
        
        # Continue button
        continue_button = tk.Button(
            info_frame,
            text="✅ Continue Journey",
            font=("Arial", 12, "bold"),
            bg='#4caf50',
            fg='white',
            width=20,
            height=2,
            command=popup.destroy
        )
        continue_button.pack(pady=20)
    
    def show_walking_popup(self, distance):
        """Show walking popup with ASCII art"""
        popup = tk.Toplevel(self.root)
        popup.title("🚶 Walking Segment")
        popup.geometry("500x400")
        popup.configure(bg='#e8f5e8')
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Walking ASCII art
        walking_art = """
        🚶‍♂️     🚶‍♀️
           \\   /
            \\ /
             🚶
            / \\
           /   \\
        🚶‍♂️     🚶‍♀️
        """
        
        art_frame = tk.Frame(popup, bg='#e8f5e8')
        art_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(
            art_frame,
            text="🚶 Walking Segment",
            font=("Arial", 16, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32'
        ).pack(pady=10)
        
        tk.Label(
            art_frame,
            text=f"Distance: {distance:.1f} km",
            font=("Arial", 12),
            bg='#e8f5e8',
            fg='#388e3c'
        ).pack(pady=5)
        
        # ASCII art
        art_label = tk.Label(
            art_frame,
            text=walking_art,
            font=("Courier", 12),
            bg='#e8f5e8',
            fg='#2e7d32'
        )
        art_label.pack(pady=20)
        
        # Complete button
        complete_button = tk.Button(
            art_frame,
            text="I've completed this segment using a wearable device",
            font=("Arial", 12, "bold"),
            bg='#4caf50',
            fg='white',
            width=40,
            height=4,
            command=popup.destroy
        )
        complete_button.pack(pady=20)
    
    def show_cycling_popup(self, distance):
        """Show cycling popup with ASCII art"""
        popup = tk.Toplevel(self.root)
        popup.title("🚴 Cycling Segment")
        popup.geometry("500x400")
        popup.configure(bg='#fff3e0')
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Cycling ASCII art
        cycling_art = """
        🚴‍♂️     🚴‍♀️
           \\   /
            \\ /
             🚴
            / \\
           /   \\
        🚴‍♂️     🚴‍♀️
        """
        
        art_frame = tk.Frame(popup, bg='#fff3e0')
        art_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(
            art_frame,
            text="🚴 Cycling Segment",
            font=("Arial", 16, "bold"),
            bg='#fff3e0',
            fg='#f57c00'
        ).pack(pady=10)
        
        tk.Label(
            art_frame,
            text=f"Distance: {distance:.1f} km",
            font=("Arial", 12),
            bg='#fff3e0',
            fg='#ef6c00'
        ).pack(pady=5)
        
        # ASCII art
        art_label = tk.Label(
            art_frame,
            text=cycling_art,
            font=("Courier", 12),
            bg='#fff3e0',
            fg='#f57c00'
        )
        art_label.pack(pady=20)
        
        # Complete button
        complete_button = tk.Button(
            art_frame,
            text="I've completed this segment using a wearable device",
            font=("Arial", 12, "bold"),
            bg='#ff9800',
            fg='white',
            width=40,
            height=4,
            command=popup.destroy
        )
        complete_button.pack(pady=20)
    
    def create_route_item(self, route, index):
        # Route container
        route_container = tk.Frame(
            self.routes_frame,
            bg='white',
            relief='solid',
            bd=2
        )
        route_container.pack(fill='x', padx=10, pady=5)
        
        # If it's an eco-friendly route, add special border
        if route['eco']:
            route_container.config(bg='#e8f5e8', relief='solid', bd=3)
        
        # Selection button
        radio_button = tk.Radiobutton(
            route_container,
            variable=self.route_var,
            value=index,
            bg='white' if not route['eco'] else '#e8f5e8',
            command=lambda: self.select_route(index)
        )
        radio_button.pack(side='left', padx=10, pady=10)
        
        # Route info frame
        info_frame = tk.Frame(route_container, bg='white' if not route['eco'] else '#e8f5e8')
        info_frame.pack(side='left', fill='x', expand=True, padx=(0, 10), pady=10)
        
        # Route name and icon
        name_frame = tk.Frame(info_frame, bg='white' if not route['eco'] else '#e8f5e8')
        name_frame.pack(fill='x')
        
        name_label = tk.Label(
            name_frame,
            text=route['name'],
            font=("Arial", 14, "bold"),
            bg='white' if not route['eco'] else '#e8f5e8',
            fg=route['color']
        )
        name_label.pack(side='left')
        
        # Eco-friendly label
        if route['eco']:
            eco_label = tk.Label(
                name_frame,
                text="🌱 Eco Route",
                font=("Arial", 10, "bold"),
                bg='#e8f5e8',
                fg='#2e7d32'
            )
            eco_label.pack(side='left', padx=(10, 0))
        
        # Route details
        details_frame = tk.Frame(info_frame, bg='white' if not route['eco'] else '#e8f5e8')
        details_frame.pack(fill='x', pady=(5, 0))
        
        # Distance
        distance_label = tk.Label(
            details_frame,
            text=f"📏 {route['distance']:.1f} km",
            font=("Arial", 11),
            bg='white' if not route['eco'] else '#e8f5e8',
            fg='#1976d2'
        )
        distance_label.pack(side='left', padx=(0, 15))
        
        # Time
        time_label = tk.Label(
            details_frame,
            text=f"⏱️ {route['time']:.0f} min",
            font=("Arial", 11),
            bg='white' if not route['eco'] else '#e8f5e8',
            fg='#388e3c'
        )
        time_label.pack(side='left', padx=(0, 15))
        
        # CO₂ emission
        if route['eco']:
            # Calculate CO₂ reduction compared to driving
            driving_co2 = route['distance'] * 0.2  # Driving route CO₂ emission
            co2_saved = driving_co2 - route['co2']
            co2_label = tk.Label(
                details_frame,
                text=f"🌍 Reduced {co2_saved:.2f} kg CO₂",
                font=("Arial", 11, "bold"),
                bg='#e8f5e8',
                fg='#2e7d32'
            )
            co2_label.pack(side='left', padx=(0, 15))
        else:
            co2_label = tk.Label(
                details_frame,
                text=f"🌍 Emitted {route['co2']:.2f} kg CO₂",
                font=("Arial", 11),
                bg='white',
                fg='#f44336'
            )
            co2_label.pack(side='left', padx=(0, 15))
        
        # Bus transfer info display
        if route['transfer_info']:
            transfer_label = tk.Label(
                details_frame,
                text=f"🚌 Transfer: {route['transfer_info']}",
                font=("Arial", 10),
                bg='white' if not route['eco'] else '#e8f5e8',
                fg='#1976d2'
            )
            transfer_label.pack(side='left', padx=(15, 0))
        
        # Reward display
        if route['rewards']:
            rewards_text = "🎁 Rewards: " + ", ".join([reward['name'] for reward in route['rewards']])
            rewards_label = tk.Label(
                details_frame,
                text=rewards_text,
                font=("Arial", 10, "bold"),
                bg='white' if not route['eco'] else '#e8f5e8',
                fg='#e91e63'
            )
            rewards_label.pack(side='left', padx=(15, 0))
        
        # Select button
        select_button = tk.Button(
            route_container,
            text="✅ Select",
            font=("Arial", 10, "bold"),
            bg='#4caf50' if route['eco'] else '#2196f3',
            fg='white',
            width=8,
            height=1,
            command=lambda: self.select_route(index)
        )
        select_button.pack(side='right', padx=10, pady=10)
    
    def select_route(self, index):
        self.selected_route = self.generated_routes[index]
        self.route_var.set(index)
        
        # If it's an eco-friendly route, show popups and process rewards
        if self.selected_route['eco']:
            self.show_route_popups(self.selected_route)
            self.process_route_rewards()
        
        # Update user data
        self.update_user_data()
        self.update_progress_display()
        
        # Show selection result
        self.show_route_selection()
    
    def process_route_rewards(self):
        """Process route rewards"""
        self.user_data['eco_routes_taken'] += 1
        
        # Process pre-generated rewards
        for reward in self.selected_route['rewards']:
            if reward['type'] == 'potion':
                self.user_data['inventory']['potions'] += reward['count']
                self.add_reward_message(f"🎉 Got {reward['name']} x{reward['count']}!")
            elif reward['type'] == 'sword':
                self.user_data['inventory']['iron_sword'] += reward['count']
                self.add_reward_message(f"⚔️ Got {reward['name']} x{reward['count']}!")
            elif reward['type'] == 'armor':
                self.user_data['inventory']['iron_armor'] += reward['count']
                self.add_reward_message(f"🛡️ Got {reward['name']} x{reward['count']}!")
        
        self.save_user_data()
    
    def add_reward_message(self, message):
        """Add reward message"""
        self.reward_text.insert(tk.END, message + "\n")
        self.reward_text.see(tk.END)
    
    def update_user_data(self):
        """Update user data"""
        if self.selected_route:
            # Update CO₂ reduction
            if self.selected_route['eco']:
                # Calculate CO₂ reduction compared to driving
                driving_co2 = self.selected_route['distance'] * 0.2
                co2_saved = driving_co2 - self.selected_route['co2']
                self.user_data['total_co2_saved'] += co2_saved
            
            
            self.save_user_data()
    
    def update_progress_display(self):
        """Update progress display"""
        # Update CO₂ reduction display
        self.co2_label.config(text=f"{self.user_data['total_co2_saved']:.2f} kg CO₂")
        
        
        # Update challenge count display
        self.challenge_label.config(text=f"{self.user_data['game_challenges']} times")
        
        # Update inventory display
        self.potion_label.config(text=f"💊 HP Potions: {self.user_data['inventory']['potions']}")
        self.sword_label.config(text=f"⚔️ Iron Sword: {self.user_data['inventory']['iron_sword']}")
        self.armor_label.config(text=f"🛡️ Iron Armor: {self.user_data['inventory']['iron_armor']}")
    
    def exchange_co2(self):
        """Exchange CO₂ reduction for game challenges"""
        if self.user_data['total_co2_saved'] >= 10:
            exchange_count = int(self.user_data['total_co2_saved'] // 10)
            self.user_data['total_co2_saved'] -= exchange_count * 10
            self.user_data['game_challenges'] += exchange_count
            
            self.save_user_data()
            self.update_progress_display()
            
            messagebox.showinfo(
                "Exchange Successful", 
                f"Successfully exchanged {exchange_count} game challenges!\nRemaining CO₂ reduction: {self.user_data['total_co2_saved']:.1f} kg CO₂"
            )
        else:
            messagebox.showwarning("Exchange Failed", "Insufficient CO₂ reduction! Need at least 10 kg CO₂ to exchange for 1 challenge.")
    
    def show_route_selection(self):
        """Show route selection result"""
        if not self.selected_route:
            return
        
        route = self.selected_route
        message = f"""✅ Selected Route: {route['name']}

📋 Route Details:
• Distance: {route['distance']:.1f} km
• Estimated Time: {route['time']:.0f} minutes
• CO₂ Emission: {route['co2']:.2f} kg CO₂

"""
        
        if route['eco']:
            message += "🌱 Thank you for choosing an eco-friendly route!\nContributing to environmental protection!"
            if route['rewards']:
                message += "\n\n🎁 Rewards Received:\n"
                for reward in route['rewards']:
                    message += f"• {reward['name']} x{reward['count']}\n"
        else:
            message += "💡 Try eco-friendly routes next time to contribute to environmental protection!"
        
        messagebox.showinfo("Route Selection", message)
    
    def clear_inputs(self):
        """Clear inputs"""
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, "Please enter start address...")
        self.start_entry.config(fg='gray')
        
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, "Please enter end address...")
        self.end_entry.config(fg='gray')
        
        # Clear route display
        for widget in self.routes_frame.winfo_children():
            widget.destroy()
        
        self.generated_routes = []
        self.selected_route = None