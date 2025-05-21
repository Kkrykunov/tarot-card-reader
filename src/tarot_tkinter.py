"""
Tarot Card Reading Desktop Application

A Tkinter-based desktop GUI application for tarot card readings.
Supports multiple reading types, save/load functionality, and card imagery.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
from typing import Optional, Dict
from tarot_core import TarotReading, TarotCard


class TarotApp:
    """Main Tarot Card Reading Desktop Application."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the Tarot application."""
        self.root = root
        self.root.title("Tarot Card Reader")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        self.tarot_reading = TarotReading()
        self.current_reading = None
        
        self.setup_ui()
        self.setup_menu()
    
    def setup_menu(self) -> None:
        """Set up the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Reading", command=self.save_reading)
        file_menu.add_command(label="Load Reading", command=self.load_reading)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Reading Menu
        reading_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reading", menu=reading_menu)
        reading_menu.add_command(label="Single Card", command=self.single_card_reading)
        reading_menu.add_command(label="Three Card", command=self.three_card_reading)
        reading_menu.add_command(label="Celtic Cross", command=self.celtic_cross_reading)
        reading_menu.add_separator()
        reading_menu.add_command(label="New Reading", command=self.new_reading)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_ui(self) -> None:
        """Set up the main user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Tarot Card Reader", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Reading type selection
        type_frame = ttk.LabelFrame(main_frame, text="Select Reading Type", padding="10")
        type_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.reading_type = tk.StringVar(value="Single Card")
        
        ttk.Radiobutton(type_frame, text="Single Card Reading", 
                       variable=self.reading_type, value="Single Card").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(type_frame, text="Three Card Reading (Past, Present, Future)", 
                       variable=self.reading_type, value="Three Card").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(type_frame, text="Celtic Cross Reading (10 cards)", 
                       variable=self.reading_type, value="Celtic Cross").grid(row=2, column=0, sticky=tk.W)
        
        # Draw button
        draw_button = ttk.Button(type_frame, text="Draw Cards", command=self.draw_cards)
        draw_button.grid(row=3, column=0, pady=(10, 0))
        
        # Results display
        results_frame = ttk.LabelFrame(main_frame, text="Reading Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80, 
                                                     font=("Arial", 11), wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save Reading", command=self.save_reading).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Load Reading", command=self.load_reading).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="New Reading", command=self.new_reading).grid(row=0, column=2, padx=(5, 0))
    
    def draw_cards(self) -> None:
        """Draw cards based on selected reading type."""
        reading_type = self.reading_type.get()
        
        try:
            if reading_type == "Single Card":
                self.current_reading = self.tarot_reading.single_card_reading()
            elif reading_type == "Three Card":
                self.current_reading = self.tarot_reading.three_card_reading()
            elif reading_type == "Celtic Cross":
                self.current_reading = self.tarot_reading.celtic_cross_reading()
            
            if "error" in self.current_reading:
                messagebox.showerror("Error", self.current_reading["error"])
                return
            
            self.display_reading(self.current_reading)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw cards: {str(e)}")
    
    def display_reading(self, reading: Dict) -> None:
        """Display the reading results."""
        self.results_text.delete(1.0, tk.END)
        
        # Reading header
        self.results_text.insert(tk.END, f"Reading Type: {reading['type']}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Cards drawn
        self.results_text.insert(tk.END, "Cards Drawn:\n")
        for i, card_data in enumerate(reading['cards'], 1):
            card = TarotCard.from_dict(card_data)
            self.results_text.insert(tk.END, f"{i}. {card.get_meaning()}\n")
        
        self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n\n")
        
        # Interpretation
        self.results_text.insert(tk.END, "Interpretation:\n")
        self.results_text.insert(tk.END, reading['interpretation'])
        
        # Scroll to top
        self.results_text.see(1.0)
    
    def save_reading(self) -> None:
        """Save the current reading to a file."""
        if not self.current_reading:
            messagebox.showwarning("Warning", "No reading to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".rdg",
            filetypes=[("Reading files", "*.rdg"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_reading, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Reading saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save reading: {str(e)}")
    
    def load_reading(self) -> None:
        """Load a reading from a file."""
        filename = filedialog.askopenfilename(
            filetypes=[("Reading files", "*.rdg"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.current_reading = json.load(f)
                self.display_reading(self.current_reading)
                messagebox.showinfo("Success", f"Reading loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load reading: {str(e)}")
    
    def new_reading(self) -> None:
        """Start a new reading session."""
        self.tarot_reading = TarotReading()
        self.current_reading = None
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Welcome to the Tarot Card Reader!\n\n")
        self.results_text.insert(tk.END, "Select a reading type and click 'Draw Cards' to begin.\n")
    
    def single_card_reading(self) -> None:
        """Perform a single card reading."""
        self.reading_type.set("Single Card")
        self.draw_cards()
    
    def three_card_reading(self) -> None:
        """Perform a three card reading."""
        self.reading_type.set("Three Card")
        self.draw_cards()
    
    def celtic_cross_reading(self) -> None:
        """Perform a Celtic Cross reading."""
        self.reading_type.set("Celtic Cross")
        self.draw_cards()
    
    def show_about(self) -> None:
        """Show about dialog."""
        about_text = """Tarot Card Reading Application

A desktop application for tarot card readings with support for:
- Single Card readings
- Three Card readings (Past, Present, Future)
- Celtic Cross readings (10 cards)
- Save and load functionality
- Complete 78-card tarot deck

Version: 1.0
Created with Python and Tkinter"""
        
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point for the Tarot desktop application."""
    root = tk.Tk()
    app = TarotApp(root)
    
    # Initialize with welcome message
    app.new_reading()
    
    root.mainloop()


if __name__ == "__main__":
    main()