import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class DragonGameInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("🐉 Dragon Battle Game")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1a1a2e')
        
        # Load user data
        self.user_data = self.load_user_data()
        
        # Game state
        player_data = self.user_data.get('player', {})
        self.player = {
            'name': 'Hero',
            'hp': player_data.get('max_hp', 100),
            'max_hp': player_data.get('max_hp', 100),
            'attack': player_data.get('attack', 20),
            'defense': player_data.get('defense', 10),
            'level': player_data.get('level', 1),
            'exp': player_data.get('exp', 0),
            'inventory': player_data.get('inventory', {
                'potions': 0,
                'iron_sword': 0,
                'iron_armor': 0
            })
        }

        # Dragon theme configurations
        self.dragon_themes = {
            'flame': {
                'name': 'Flame',
                'emoji': '🔥',
                'color': '#ff6b6b',
                'bg_color': '#2c1810',
                'hp': 150,
                'max_hp': 150,
                'attack': 25,
                'defense': 15,
                'level': 3,
                'difficulty': 'hard'
            },
            'desert': {
                'name': 'Desert',
                'emoji': '🏜️',
                'color': '#ffa726',
                'bg_color': '#2c2c1a',
                'hp': 120,
                'max_hp': 120,
                'attack': 20,
                'defense': 12,
                'level': 2,
                'difficulty': 'medium'
            },
            'wasteland': {
                'name': 'Wasteland',
                'emoji': '🌫️',
                'color': '#9e9e9e',
                'bg_color': '#1a1a1a',
                'hp': 100,
                'max_hp': 100,
                'attack': 18,
                'defense': 10,
                'level': 1,
                'difficulty': 'easy'
            }
        }
        
        self.current_theme = 'flame'  # Default flame theme
        self.dragon = self.dragon_themes[self.current_theme].copy()
        
        self.game_state = 'menu'  # menu, battle, victory, defeat
        self.battle_log = []
        self.challenges_used = 0
        
        # Create interface
        self.create_widgets()
        self.update_display()
        
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
            'total_co2_saved': 0.0,
            'total_calories': 0.0,
            'game_challenges': 0,
            'inventory': {
                'potions': 0,
                'iron_sword': 0,
                'iron_armor': 0
            },
            'eco_routes_taken': 0
        }
    
    def save_user_data(self):
        """Save user data (including character status)"""
        try:
            self.user_data['player'] = {
                'level': self.player['level'],
                'exp': self.player['exp'],
                'attack': self.player['attack'],
                'defense': self.player['defense'],
                'max_hp': self.player['max_hp'],
                'inventory': self.player['inventory']
            }
            with open('user_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except:
            pass

        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="🐉 Dragon Battle Game",
            font=("Arial", 24, "bold"),
            bg='#1a1a2e',
            fg='#ff6b6b'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left area
        left_frame = tk.Frame(main_frame, bg='#1a1a2e')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right area
        right_frame = tk.Frame(main_frame, bg='#1a1a2e', width=250)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Theme selection area
        self.create_theme_selection(left_frame)
        
        # Character info area
        self.create_character_info(left_frame)
        
        # Battle area
        self.create_battle_area(left_frame)
        
        # Control buttons area
        self.create_control_buttons(left_frame)
        
        # Battle log area
        self.create_battle_log(left_frame)
        
        # Right side info area
        self.create_side_info(right_frame)
        
    def create_theme_selection(self, parent):
        # Theme selection frame
        theme_frame = tk.LabelFrame(
            parent,
            text="🎭 Dragon Theme Selection",
            font=("Arial", 14, "bold"),
            bg='#1a1a2e',
            fg='#ffd93d',
            padx=15,
            pady=10
        )
        theme_frame.pack(fill='x', pady=(0, 15))
        
        # Theme buttons frame
        theme_buttons_frame = tk.Frame(theme_frame, bg='#1a1a2e')
        theme_buttons_frame.pack(fill='x')
        
        # Flame theme button
        self.flame_button = tk.Button(
            theme_buttons_frame,
            text="🔥 Flame Theme\n(Hard)",
            font=("Arial", 11, "bold"),
            bg='#ff6b6b',
            fg='white',
            width=12,
            height=2,
            command=lambda: self.select_theme('flame')
        )
        self.flame_button.pack(side='left', padx=5)
        
        # Desert theme button
        self.desert_button = tk.Button(
            theme_buttons_frame,
            text="🏜️ Desert Theme\n(Medium)",
            font=("Arial", 11, "bold"),
            bg='#ffa726',
            fg='white',
            width=12,
            height=2,
            command=lambda: self.select_theme('desert')
        )
        self.desert_button.pack(side='left', padx=5)
        
        # Wasteland theme button
        self.wasteland_button = tk.Button(
            theme_buttons_frame,
            text="🌫️ Wasteland Theme\n(Easy)",
            font=("Arial", 11, "bold"),
            bg='#9e9e9e',
            fg='white',
            width=12,
            height=2,
            command=lambda: self.select_theme('wasteland')
        )
        self.wasteland_button.pack(side='left', padx=5)
        
        # Update button states
        self.update_theme_buttons()
        
    def select_theme(self, theme):
        """Select dragon theme"""
        self.current_theme = theme
        self.dragon = self.dragon_themes[theme].copy()
        self.update_theme_buttons()
        self.update_display()
        self.add_log(f"🎭 Selected {self.dragon['name']} theme! Difficulty: {self.dragon['difficulty']}")
        
    def update_theme_buttons(self):
        """Update theme button states"""
        # Reset all button styles
        self.flame_button.config(bg='#ff6b6b', relief='raised')
        self.desert_button.config(bg='#ffa726', relief='raised')
        self.wasteland_button.config(bg='#9e9e9e', relief='raised')
        
        # Highlight currently selected theme
        if self.current_theme == 'flame':
            self.flame_button.config(bg='#d32f2f', relief='sunken')
        elif self.current_theme == 'desert':
            self.desert_button.config(bg='#f57c00', relief='sunken')
        elif self.current_theme == 'wasteland':
            self.wasteland_button.config(bg='#616161', relief='sunken')
        
    def create_character_info(self, parent):
        # Character info frame
        char_frame = tk.LabelFrame(
            parent,
            text="⚔️ Character Info",
            font=("Arial", 14, "bold"),
            bg='#1a1a2e',
            fg='#4ecdc4',
            padx=15,
            pady=10
        )
        char_frame.pack(fill='x', pady=(0, 15))
        
        # Player info
        player_frame = tk.Frame(char_frame, bg='#1a1a2e')
        player_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        self.player_info = tk.Label(
            player_frame,
            text="",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#4ecdc4',
            justify='left'
        )
        self.player_info.pack(anchor='w')
        
        # Dragon info
        dragon_frame = tk.Frame(char_frame, bg='#1a1a2e')
        dragon_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        self.dragon_info = tk.Label(
            dragon_frame,
            text="",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#ff6b6b',
            justify='left'
        )
        self.dragon_info.pack(anchor='w')
        
    def create_battle_area(self, parent):
        # Battle area frame
        battle_frame = tk.LabelFrame(
            parent,
            text="⚔️ Battle Area",
            font=("Arial", 14, "bold"),
            bg='#1a1a2e',
            fg='#ffd93d',
            padx=15,
            pady=10
        )
        battle_frame.pack(fill='x', pady=(0, 15))
        
        # Battle status display
        self.battle_status = tk.Label(
            battle_frame,
            text="🎮 Welcome to Dragon Battle Game!\nClick 'Start Battle' to begin your adventure!",
            font=("Arial", 12),
            bg='#1a1a2e',
            fg='#ffd93d',
            justify='center',
            height=4
        )
        self.battle_status.pack(fill='x', pady=10)
        
    def create_control_buttons(self, parent):
        # Control buttons frame
        control_frame = tk.Frame(parent, bg='#1a1a2e')
        control_frame.pack(fill='x', pady=(0, 15))
        
        # Battle buttons
        self.attack_button = tk.Button(
            control_frame,
            text="⚔️ Attack",
            font=("Arial", 12, "bold"),
            bg='#ff6b6b',
            fg='white',
            width=12,
            height=2,
            command=self.player_attack,
            state='disabled'
        )
        self.attack_button.pack(side='left', padx=(0, 10))
        
        self.defend_button = tk.Button(
            control_frame,
            text="🛡️ Defend",
            font=("Arial", 12, "bold"),
            bg='#4ecdc4',
            fg='white',
            width=12,
            height=2,
            command=self.player_defend,
            state='disabled'
        )
        self.defend_button.pack(side='left', padx=10)
        
        
        self.use_potion_button = tk.Button(
            control_frame,
            text="🧪 Use Potion",
            font=("Arial", 12, "bold"),
            bg='#9c27b0',
            fg='white',
            width=12,
            height=2,
            command=self.use_potion,
            state='disabled'
        )
        self.use_potion_button.pack(side='left', padx=10)
        
        self.start_button = tk.Button(
            control_frame,
            text="🚀 Start Battle",
            font=("Arial", 12, "bold"),
            bg='#96ceb4',
            fg='white',
            width=12,
            height=2,
            command=self.start_battle
        )
        self.start_button.pack(side='left', padx=10)
        
    def create_battle_log(self, parent):
        # Battle log frame
        log_frame = tk.LabelFrame(
            parent,
            text="📜 Battle Log",
            font=("Arial", 14, "bold"),
            bg='#1a1a2e',
            fg='#a8e6cf',
            padx=15,
            pady=10
        )
        log_frame.pack(fill='both', expand=True)
        
        # Log text box
        self.log_text = tk.Text(
            log_frame,
            font=("Arial", 10),
            bg='#2c2c54',
            fg='#a8e6cf',
            wrap='word',
            height=8,
            relief='solid',
            bd=1
        )
        self.log_text.pack(fill='both', expand=True, pady=5)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scrollbar.set)
    
    def create_side_info(self, parent):
        # Challenge count info
        challenge_frame = tk.LabelFrame(
            parent,
            text="⚔️ Challenge Info",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#4ecdc4',
            padx=10,
            pady=8
        )
        challenge_frame.pack(fill='x', pady=(0, 10))
        
        self.challenge_label = tk.Label(
            challenge_frame,
            text=f"Remaining Challenges: {self.user_data.get('game_challenges', 0)} times",
            font=("Arial", 11, "bold"),
            bg='#1a1a2e',
            fg='#4ecdc4'
        )
        self.challenge_label.pack(pady=5)
        
        # Inventory info
        inventory_frame = tk.LabelFrame(
            parent,
            text="🎒 Inventory",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#ffd93d',
            padx=10,
            pady=8
        )
        inventory_frame.pack(fill='x', pady=(0, 10))
        
        self.potion_count_label = tk.Label(
            inventory_frame,
            text=f"💊 HP Potions: {self.player['inventory']['potions']}",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#4caf50'
        )
        self.potion_count_label.pack(anchor='w', pady=2)
        
        self.sword_count_label = tk.Label(
            inventory_frame,
            text=f"⚔️ Iron Sword: {self.player['inventory']['iron_sword']}",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#2196f3'
        )
        self.sword_count_label.pack(anchor='w', pady=2)
        
        self.armor_count_label = tk.Label(
            inventory_frame,
            text=f"🛡️ Iron Armor: {self.player['inventory']['iron_armor']}",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#ff5722'
        )
        self.armor_count_label.pack(anchor='w', pady=2)
        
        # Equipment buttons
        equip_frame = tk.LabelFrame(
            parent,
            text="⚔️ Equipment",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#ff6b6b',
            padx=10,
            pady=8
        )
        equip_frame.pack(fill='x', pady=(0, 10))
        
        self.equip_sword_button = tk.Button(
            equip_frame,
            text="⚔️ Equip Iron Sword",
            font=("Arial", 10),
            bg='#2196f3',
            fg='white',
            width=15,
            command=self.equip_sword,
            state='disabled'
        )
        self.equip_sword_button.pack(fill='x', pady=2)
        
        self.equip_armor_button = tk.Button(
            equip_frame,
            text="🛡️ Equip Iron Armor",
            font=("Arial", 10),
            bg='#ff5722',
            fg='white',
            width=15,
            command=self.equip_armor,
            state='disabled'
        )
        self.equip_armor_button.pack(fill='x', pady=2)
        
        # Eco statistics
        eco_frame = tk.LabelFrame(
            parent,
            text="🌱 Eco Statistics",
            font=("Arial", 12, "bold"),
            bg='#1a1a2e',
            fg='#4caf50',
            padx=10,
            pady=8
        )
        eco_frame.pack(fill='x', pady=(0, 10))
        
        self.eco_routes_label = tk.Label(
            eco_frame,
            text=f"🌍 Eco Routes: {self.user_data.get('eco_routes_taken', 0)} times",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#4caf50'
        )
        self.eco_routes_label.pack(anchor='w', pady=2)
        
        self.co2_saved_label = tk.Label(
            eco_frame,
            text=f"🌱 CO₂ Reduced: {self.user_data.get('total_co2_saved', 0):.1f} kg",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#4caf50'
        )
        self.co2_saved_label.pack(anchor='w', pady=2)
        
    def update_display(self):
        # Update player info
        player_text = f"""👤 {self.player['name']} (Lv.{self.player['level']})
❤️ HP: {self.player['hp']}/{self.player['max_hp']}
⚔️ Attack: {self.player['attack']}
🛡️ Defense: {self.player['defense']}
⭐ Experience: {self.player['exp']}"""
        
        self.player_info.config(text=player_text)
        
        # Update dragon info
        dragon_text = f"""{self.dragon['emoji']} {self.dragon['name']} (Lv.{self.dragon['level']})
❤️ HP: {self.dragon['hp']}/{self.dragon['max_hp']}
⚔️ Attack: {self.dragon['attack']}
🛡️ Defense: {self.dragon['defense']}
🎯 Difficulty: {self.dragon['difficulty']}"""
        
        self.dragon_info.config(text=dragon_text)
        
        # Update right side info
        self.challenge_label.config(text=f"Remaining Challenges: {self.user_data.get('game_challenges', 0)} times")
        self.potion_count_label.config(text=f"💊 HP Potions: {self.player['inventory']['potions']}")
        self.sword_count_label.config(text=f"⚔️ Iron Sword: {self.player['inventory']['iron_sword']}")
        self.armor_count_label.config(text=f"🛡️ Iron Armor: {self.player['inventory']['iron_armor']}")
        self.eco_routes_label.config(text=f"🌍 Eco Routes: {self.user_data.get('eco_routes_taken', 0)} times")
        self.co2_saved_label.config(text=f"🌱 CO₂ Reduced: {self.user_data.get('total_co2_saved', 0):.1f} kg")
        
        # Update equipment button states
        if self.player['inventory']['iron_sword'] > 0:
            self.equip_sword_button.config(state='normal')
        else:
            self.equip_sword_button.config(state='disabled')
            
        if self.player['inventory']['iron_armor'] > 0:
            self.equip_armor_button.config(state='normal')
        else:
            self.equip_armor_button.config(state='disabled')
        
    def add_log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        
    def start_battle(self):
        # Check challenge count
        if self.user_data.get('game_challenges', 0) <= 0:
            messagebox.showwarning("Insufficient Challenges", "No remaining challenges!\nPlease exchange CO₂ reduction for challenges by choosing eco-friendly routes.")
            return
        
        # Consume challenge count
        self.user_data['game_challenges'] -= 1
        self.challenges_used += 1
        self.save_user_data()
        
        self.game_state = 'battle'
        self.battle_log = []
        self.log_text.delete(1.0, tk.END)
        # Auto heal (restore HP when restarting after save)
        self.player['hp'] = self.player['max_hp']

        
        # Enable battle buttons
        self.attack_button.config(state='normal')
        self.defend_button.config(state='normal')
        self.use_potion_button.config(state='normal')
        self.start_button.config(state='disabled')
        
        self.battle_status.config(text="⚔️ Battle Started!\nChoose your action!")
        self.add_log(f"{self.dragon['emoji']} {self.dragon['name']} appeared!")
        self.add_log("⚔️ Battle started!")
        self.add_log(f"Remaining challenges: {self.user_data.get('game_challenges', 0)}")
        
        self.update_display()
        
    def player_attack(self):
        if self.game_state != 'battle':
            return
            
        # Calculate damage
        base_damage = self.player['attack']
        damage_variation = random.randint(-5, 5)
        actual_damage = max(1, base_damage + damage_variation - self.dragon['defense'])
        
        self.dragon['hp'] -= actual_damage
        self.add_log(f"⚔️ {self.player['name']} dealt {actual_damage} damage to {self.dragon['name']}!")
        
        if self.dragon['hp'] <= 0:
            self.dragon['hp'] = 0
            self.victory()
            return
            
        self.update_display()
        self.dragon_attack()
        
    def player_defend(self):
        if self.game_state != 'battle':
            return
            
        self.add_log(f"🛡️ {self.player['name']} entered defense stance!")
        self.dragon_attack(defense_bonus=5)
        
    def dragon_attack(self, defense_bonus=0):
        if self.game_state != 'battle':
            return
            
        # Calculate damage
        base_damage = self.dragon['attack']
        damage_variation = random.randint(-3, 3)
        actual_damage = max(1, base_damage + damage_variation - self.player['defense'] - defense_bonus)
        
        self.player['hp'] -= actual_damage
        self.add_log(f"🔥 {self.dragon['name']} dealt {actual_damage} damage to {self.player['name']}!")
        
        if self.player['hp'] <= 0:
            self.player['hp'] = 0
            self.defeat()
            return
            
        self.update_display()
        
    def victory(self):
        self.game_state = 'victory'
        
        # Calculate rewards
        exp_gain = random.randint(50, 80)
        
        self.player['exp'] += exp_gain
        
        # Check for level up
        level_up = False
        while self.player['exp'] >= 100:
            self.player['level'] += 1
            self.player['exp'] -= 100
            level_up = True
            
            # Random attribute boost
            if random.random() < 0.5:
                attack_bonus = random.randint(2, 4)
                self.player['attack'] += attack_bonus
                self.add_log(f"🌟 Level up! Attack +{attack_bonus}")
            else:
                defense_bonus = random.randint(2, 4)
                self.player['defense'] += defense_bonus
                self.add_log(f"🌟 Level up! Defense +{defense_bonus}")
            
            # Restore HP on level up
            self.player['max_hp'] += 15
            self.player['hp'] = self.player['max_hp']
            
        self.battle_status.config(text="🎉 Victory!\nYou defeated the dragon!")
        self.add_log(f"🎉 Congratulations! You defeated {self.dragon['name']}!")
        self.add_log(f"⭐ Gained experience: {exp_gain}")
        
        if level_up:
            self.add_log(f"🌟 Level up! Now Lv.{self.player['level']}!")
            
        # Show eco action popup
        self.show_eco_action_popup()
        
        # Disable battle buttons, enable restart button
        self.attack_button.config(state='disabled')
        self.defend_button.config(state='disabled')
        self.use_potion_button.config(state='disabled')
        self.start_button.config(state='normal')
        
        self.update_display()
    
    def show_eco_action_popup(self):
        """Show eco action popup based on dragon theme"""
        popup = tk.Toplevel(self.root)
        popup.title("🌱 Environmental Action")
        popup.geometry("600x500")
        popup.configure(bg='#e8f5e8')
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Main frame
        main_frame = tk.Frame(popup, bg='#e8f5e8')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🌱 Environmental Action Completed!",
            font=("Arial", 18, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32'
        )
        title_label.pack(pady=10)
        
        # Get coordinates and action based on theme
        if self.current_theme == 'wasteland':
            coordinates = "25.2744°S, 133.7751°E"
            action_text = "Grass Grid Deployed"
            ascii_art = """
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
        🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
            """
        elif self.current_theme == 'desert':
            coordinates = "25.2744°S, 133.7751°E"
            action_text = "Atriplex nummularia (Old Man Saltbush) Planted"
            ascii_art = """
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
        🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿
            """
        else:  # flame
            coordinates = "25.2744°S, 133.7751°E"
            action_text = "Eucalyptus microtheca Planted"
            ascii_art = """
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
        🌳🌳🌳🌳🌳🌳🌳🌳🌳🌳
            """
        
        # Location info
        location_label = tk.Label(
            main_frame,
            text=f"📍 Location: Central Australia\n{coordinates}",
            font=("Arial", 12, "bold"),
            bg='#e8f5e8',
            fg='#1976d2'
        )
        location_label.pack(pady=10)
        
        # Action info
        action_label = tk.Label(
            main_frame,
            text=f"🌱 Action: {action_text}",
            font=("Arial", 14, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32'
        )
        action_label.pack(pady=10)
        
        # ASCII art
        art_label = tk.Label(
            main_frame,
            text=ascii_art,
            font=("Courier", 8),
            bg='#e8f5e8',
            fg='#2e7d32'
        )
        art_label.pack(pady=20)
        
        # Close button
        close_button = tk.Button(
            main_frame,
            text="✅ Continue",
            font=("Arial", 12, "bold"),
            bg='#4caf50',
            fg='white',
            width=15,
            height=2,
            command=popup.destroy
        )
        close_button.pack(pady=20)
        
            
    def defeat(self):
        self.game_state = 'defeat'
        
        # Calculate experience gained on defeat (based on damage dealt to dragon)
        damage_dealt = self.dragon['max_hp'] - self.dragon['hp']
        exp_gain = max(10, damage_dealt // 2)  # At least 10 exp, 1 exp per 2 damage
        
        self.player['exp'] += exp_gain
        
        # Check for level up
        level_up = False
        while self.player['exp'] >= 100:
            self.player['level'] += 1
            self.player['exp'] -= 100
            level_up = True
            
            if random.random() < 0.5:
                attack_bonus = random.randint(2, 4)
                self.player['attack'] += attack_bonus
                self.add_log(f"🌟 Level up! Attack +{attack_bonus}")
            else:
                defense_bonus = random.randint(2, 4)
                self.player['defense'] += defense_bonus
                self.add_log(f"🌟 Level up! Defense +{defense_bonus}")
            
            self.player['max_hp'] += 15

        # Auto heal and save
        self.player['hp'] = self.player['max_hp']
        self.save_user_data()
        
        self.battle_status.config(text="💀 Defeat!\nYou were defeated by the dragon, but experience and equipment are saved!")
        self.add_log(f"💀 You were defeated by {self.dragon['name']}... but your experience and equipment are saved!")
        self.add_log(f"⭐ Gained experience: {exp_gain}")
        
        if level_up:
            self.add_log(f"🌟 Level up! Now Lv.{self.player['level']}!")
        
        self.add_log("💾 Progress automatically saved. Click 'Start Battle' to continue!")

        # Disable battle buttons, restore "Start Battle"
        self.attack_button.config(state='disabled')
        self.defend_button.config(state='disabled')
        self.use_potion_button.config(state='disabled')
        self.start_button.config(state='normal')

        # Reset dragon status
        self.dragon['hp'] = self.dragon['max_hp']

        self.update_display()

        
    def restart_game(self):
        # Reset game state
        self.player = {
            'name': 'Hero',
            'hp': 100,
            'max_hp': 100,
            'attack': 20,
            'defense': 10,
            'level': 1,
            'exp': 0,
            'inventory': {
                'potions': self.user_data.get('inventory', {}).get('potions', 0),
                'iron_sword': self.user_data.get('inventory', {}).get('iron_sword', 0),
                'iron_armor': self.user_data.get('inventory', {}).get('iron_armor', 0)
            }
        }
        
        self.dragon = self.dragon_themes[self.current_theme].copy()
        
        self.game_state = 'menu'
        self.battle_log = []
        
        # Reset interface
        self.battle_status.config(text="🎮 Welcome to Dragon Battle Game!\nClick 'Start Battle' to begin your adventure!")
        self.log_text.delete(1.0, tk.END)
        
        # Reset button states
        self.attack_button.config(state='disabled')
        self.defend_button.config(state='disabled')
        self.use_potion_button.config(state='disabled')
        self.start_button.config(state='normal')
        self.restart_button.config(state='disabled')
        
        self.update_display()
        self.add_log("🎮 Game restarted!")
        self.add_log(f"{self.dragon['emoji']} Ready to face {self.dragon['name']}?")
    
    def use_potion(self):
        """Use HP potion"""
        if self.game_state != 'battle':
            return
            
        if self.player['inventory']['potions'] <= 0:
            self.add_log("❌ No HP potions left!")
            return
        
        # Use potion
        self.player['inventory']['potions'] -= 1
        heal_amount = random.randint(30, 50)
        self.player['hp'] = min(self.player['max_hp'], self.player['hp'] + heal_amount)
        
        self.add_log(f"🧪 Used HP potion, restored {heal_amount} HP!")
        self.add_log(f"Remaining potions: {self.player['inventory']['potions']}")
        
        self.save_user_data()
        self.update_display()
        self.dragon_attack()
    
    def equip_sword(self):
        """Equip iron sword"""
        if self.player['inventory']['iron_sword'] <= 0:
            messagebox.showwarning("Insufficient Equipment", "No iron sword to equip!")
            return
        
        # Equip iron sword, increase attack
        self.player['inventory']['iron_sword'] -= 1
        self.player['attack'] += 10
        
        self.add_log("⚔️ Equipped iron sword! Attack +10")
        self.update_display()
        self.save_user_data()
        
        messagebox.showinfo("Equipment Success", "Successfully equipped iron sword!\nAttack +10")
    
    def equip_armor(self):
        """Equip iron armor"""
        if self.player['inventory']['iron_armor'] <= 0:
            messagebox.showwarning("Insufficient Equipment", "No iron armor to equip!")
            return
        
        # Equip iron armor, increase defense
        self.player['inventory']['iron_armor'] -= 1
        self.player['defense'] += 8
        
        self.add_log("🛡️ Equipped iron armor! Defense +8")
        self.update_display()
        self.save_user_data()
        
        messagebox.showinfo("Equipment Success", "Successfully equipped iron armor!\nDefense +8")