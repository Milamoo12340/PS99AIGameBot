"""
Native Desktop Application for AI Game Bot
Cross-platform desktop interface using Tkinter
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import logging

class AIGameBotDesktop:
    """Native desktop application for AI Game Bot"""
    
    def __init__(self):
        self.logger = logging.getLogger('DesktopApp')
        self.root = tk.Tk()
        self.root.title("AI Game Bot - Desktop")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
        self.logger.info("Desktop application initialized")
    
    def setup_ui(self):
        """Setup the user interface"""
        title_label = ttk.Label(self.root, text="AI Game Bot Dashboard", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, fill=tk.X, padx=20)
        
        ttk.Label(control_frame, text="Command:").pack(side=tk.LEFT, padx=5)
        
        self.command_entry = ttk.Entry(control_frame, width=40)
        self.command_entry.pack(side=tk.LEFT, padx=5)
        
        execute_btn = ttk.Button(control_frame, text="Execute", command=self.execute_command)
        execute_btn.pack(side=tk.LEFT, padx=5)
        
        self.output_text = scrolledtext.ScrolledText(self.root, height=20, width=80)
        self.output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Open Chests", command=lambda: self.quick_command("open chests")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Hatch Eggs", command=lambda: self.quick_command("hatch eggs")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Analyze Screen", command=lambda: self.quick_command("analyze screen")).pack(side=tk.LEFT, padx=5)
        
        self.log("AI Game Bot Desktop Application Ready")
        self.log("Use web interface (--web flag) for full functionality")
    
    def execute_command(self):
        """Execute command from entry field"""
        command = self.command_entry.get().strip()
        if command:
            self.log(f"> {command}")
            self.command_entry.delete(0, tk.END)
    
    def quick_command(self, command):
        """Execute a quick command"""
        self.log(f"> {command}")
    
    def log(self, message):
        """Log message to output text"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
